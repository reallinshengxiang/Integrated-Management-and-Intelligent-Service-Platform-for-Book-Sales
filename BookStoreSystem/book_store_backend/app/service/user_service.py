# book_store_backend/app/service/user_service.py

from sklearn.metrics.pairwise import cosine_similarity
from app.models import User, Book, Order, Review, db
from werkzeug.security import generate_password_hash
from collections import defaultdict
from sqlalchemy import func, desc


from app.config import Config
from app.models import User, UserType

import random
import jieba
import math

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential




def user_login(user_id, password_hash):
    return True

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(data):
    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        user_type=data.get('user_type', 'customer')
    )
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_user(user_id, data):
    user = User.query.get(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.user_type = data.get('user_type', user.user_type)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return user
    return None

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def recommend_by_collaborative_filtering(user_id, user_ratings, excluded_book_ids):
    """基于协同过滤的推荐：使用用户-用户相似度"""
    similar_users = find_similar_users(user_id, user_ratings, k=5)
    book_scores = defaultdict(float)
    similarity_sum = defaultdict(float)
    for similar_user_id, similarity in similar_users:
        similar_user_reviews = Review.query.filter_by(user_id=similar_user_id).all()
        similar_user_ratings = {review.book_id: review.rating for review in similar_user_reviews}
        for book_id, rating in similar_user_ratings.items():
            if book_id not in excluded_book_ids:
                book_scores[book_id] += similarity * rating
                similarity_sum[book_id] += similarity
    normalized_scores = [
        (book_id, score / similarity_sum[book_id]) 
        for book_id, score in book_scores.items() 
        if similarity_sum[book_id] > 0
    ]
    return sorted(normalized_scores, key=lambda x: x[1], reverse=True)

def find_similar_users(target_user_id, target_user_ratings, k=5):
    """找到与目标用户最相似的K个用户"""
    all_users = User.query.join(Review).group_by(User.id).having(func.count(Review.id) > 0).all()
    user_similarities = []
    for user in all_users:
        if user.id == target_user_id:
            continue
        user_reviews = Review.query.filter_by(user_id=user.id).all()
        user_ratings = {review.book_id: review.rating for review in user_reviews}
        common_books = set(target_user_ratings.keys()) & set(user_ratings.keys())
        if len(common_books) < 3:
            continue
        dot_product = sum(target_user_ratings[book_id] * user_ratings[book_id] for book_id in common_books)
        target_norm = math.sqrt(sum(rating ** 2 for book_id, rating in target_user_ratings.items() if book_id in common_books))
        user_norm = math.sqrt(sum(rating ** 2 for book_id, rating in user_ratings.items() if book_id in common_books))
        if target_norm == 0 or user_norm == 0:
            continue
        similarity = dot_product / (target_norm * user_norm)
        if similarity > 0:
            user_similarities.append((user.id, similarity))
    return sorted(user_similarities, key=lambda x: x[1], reverse=True)[:k]

def recommend_by_content(user_id, user_ratings, excluded_book_ids):
    """基于内容的推荐：使用title, price, rating"""
    liked_books = []
    for book_id, rating in user_ratings.items():
        if rating >= 4:
            book = Book.query.get(book_id)
            if book:
                liked_books.append(book)
    if not liked_books:
        return []
    book_scores = []
    all_books = Book.query.all()
    for book in all_books:
        if book.id in excluded_book_ids:
            continue
        max_similarity = max(content_similarity(book, liked_book) for liked_book in liked_books)
        
        if max_similarity > 0:
            book_scores.append((book.id, max_similarity))
    return sorted(book_scores, key=lambda x: x[1], reverse=True)

def content_similarity(book1, book2):
    """计算两本书之间的内容相似度（title, price, rating）"""
    title_sim = title_similarity(book1.title, book2.title)
    price_sim = price_similarity(book1.price, book2.price)
    rating_sim = rating_similarity(book1.rating, book2.rating)
    return 0.5 * title_sim + 0.3 * price_sim + 0.2 * rating_sim

def title_similarity(title1, title2):
    """计算标题相似度（基于关键词匹配）"""
    words1 = set(jieba.cut(title1))
    words2 = set(jieba.cut(title2))
    words1 = {word for word in words1 if len(word) > 1}
    words2 = {word for word in words2 if len(word) > 1}
    if not words1 or not words2:
        return 0
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union

def price_similarity(price1, price2):
    """计算价格相似度（归一化差异）"""
    price1 = float(price1) if price1 is not None else 0.0
    price2 = float(price2) if price2 is not None else 0.0
    if not price1 or not price2:
        return 0.5
    max_price = max(price1, price2)
    min_price = min(price1, price2)
    diff_percent = 1 - (min_price / max_price)
    return 1 - diff_percent

def rating_similarity(rating1, rating2):
    """计算评分相似度（归一化差异）"""
    rating1 = float(rating1) if rating1 is not None else 0.0
    rating2 = float(rating2) if rating2 is not None else 0.0
    if not rating1 or not rating2:
        return 0.5
    max_diff = 5.0
    actual_diff = abs(rating1 - rating2)
    return 1 - (actual_diff / max_diff)

def hybrid_recommendations(content_recs, collaborative_recs, content_weight=0.6):
    """混合两种推荐结果"""
    hybrid_scores = defaultdict(float)
    for book_id, score in content_recs:
        hybrid_scores[book_id] += score * content_weight
    for book_id, score in collaborative_recs:
        hybrid_scores[book_id] += score * (1 - content_weight)
    return sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)

def get_top_rated_books_randomly(limit=5):
    """获取评分最高的100本书并随机返回其中五本的ID"""
    top_books = Book.query \
        .join(Review, Book.id == Review.book_id) \
        .group_by(Book.id) \
        .having(func.count(Review.id) >= 3) \
        .order_by(desc(func.avg(Review.rating))) \
        .limit(100) \
        .all()
    top_book_ids = [book.id for book in top_books]
    if len(top_book_ids) >= limit:
        return random.sample(top_book_ids, limit)
    else:
        return top_book_ids
    
def book_recommendation(user_id, limit=5):
    """
    混合推荐系统：结合基于内容和协同过滤的推荐方法
    """
    print(user_id)
    user = get_user_by_id(user_id)
    
    if not user:
        print('----not user-----')
        recommended_book_ids = get_top_rated_books_randomly()
        return recommended_book_ids
    orders = Order.query.filter_by(user_id=user_id).all()
    print('----orders-----')
    reviews = Review.query.filter_by(user_id=user_id).all()
    print('----reviews-----')
    reviews_book_ids = [review.book_id for review in reviews]
    print('----reviewedbook_ids-----')
    purchased_book_ids = [item.book_id for order in orders for item in order.items]
    print('----purchased_book_ids-----')
    all_browsed_book_ids = list(dict.fromkeys([*reviews_book_ids, *purchased_book_ids]))
    print('----all_browsed_book_ids-----')
    user_ratings = {review.book_id: review.rating for review in reviews}
    print('----user_ratings-----')
    content_recommendations = recommend_by_content(user_id, user_ratings, all_browsed_book_ids)
    print('----content_recommendations-----')
    #collaborative_recommendations = recommend_by_collaborative_filtering(user_id, user_ratings, all_browsed_book_ids)
    #print('----collaborative_recs-----')
    combined_recommendations = content_recommendations
    #combined_recommendations = hybrid_recommendations(content_recommendations, collaborative_recommendations)
    print('----combined_recs-----')
    recommended_book_ids = [book_id for book_id, _ in combined_recommendations[:limit]]
    recommended_books = Book.query.filter(Book.id.in_(recommended_book_ids)).all()
    if len(recommended_book_ids) < 5 :
         return get_top_rated_books_randomly()
    print(recommended_books)
    return recommended_book_ids

def deepseek_response(user_input):
    token = Config.GITHUB_TOKEN
    print('token:',token)
    endpoint = "https://models.github.ai/inference"
    model = "deepseek/DeepSeek-V3-0324"
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )
    response = client.complete(
        messages=[
            SystemMessage("你是图书销售综合管理与智能服务平台小助手，书籍信息基于豆瓣平台，回复写成一段话的形式，简洁明了"),
            UserMessage(user_input),
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
    
def get_user_count():
    admin_count = User.query.filter_by(user_type=UserType.admin).count()
    customer_count = User.query.filter_by(user_type=UserType.customer).count()
    return {'admin_count': admin_count, 'customer_count': customer_count}