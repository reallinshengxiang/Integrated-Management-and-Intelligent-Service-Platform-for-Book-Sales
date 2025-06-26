import axios from "axios";
import store from "@/store";
import router from "@/router"


console.log(import.meta.env.VITE_APP_BASE_API)

const DEFAULT_HEADER = {
    "Content-Type": 'application/json',
    "Authorization": "",
}

const http = axios.create({
    baseURL:import.meta.env.VITE_APP_BASE_API,
    timeout:60*1000,
    withCredentials:true,
})

http.interceptors.request.use(opt=>{
    DEFAULT_HEADER.Authorization = `Bearer ${store.state.token}`;
    Object.assign(opt.headers,DEFAULT_HEADER);
    return opt;
})

http.interceptors.response.use(opt=>{
    if (opt.data.code === -666){
        console.log(store)
        store.dispatch('reset')
        router.go(0)
    }else{
        return opt
    }

})

const createRestfulAPI = (url)=>{
    return {
        get(params, header){
            return http.get(url,{
                params: params,
                headers: header
            })
        },
        post(params, data, header){
            return http.post(url,data,{
                params: params,
                headers: header
            })
        },
        patch(params, data, header) {
            return http.patch(url,data,{
                params: params,
                headers: header
            })
        },
        put(params, data, header) {
            return http.put(url,data,{
                params: params,
                headers: header
            })
        },
        delete(params, data, header){
            return http.delete(url,{
                params: params,
                data: data,
                headers: header
            })
        }
    }
}

export const auth = {
    login(data){
        return http.post("/auth/login",data,{})
    },
    register(data){
        return http.post("/auth/register",data,{})
    }
}

export const bookList = createRestfulAPI("/books");
export const getBookDetail = (bookId) => createRestfulAPI(`/books/${bookId}`);

export const userList = createRestfulAPI("/users");
export const userDetail = (userId) => createRestfulAPI(`/users/${userId}`);

export const userRecommendation = (userId) => {
    return createRestfulAPI(`/user/recommendation/${userId}`);
};


export const orderList = createRestfulAPI("/orders");
export const orderDetail = (orderId) => createRestfulAPI(`/orders/${orderId}`);
export const adminBookList = createRestfulAPI("/admin/books");
export const adminBookStock = (bookId) => createRestfulAPI(`/admin/books/${bookId}/stock`);
export const deepseek = (userInput) => createRestfulAPI(`/user/deepseek/${userInput}`);

export const searchBooksByTitle = (titleSubstring) => {
    return http.post('/books/search/title', { title_substring: titleSubstring });
};

export const searchBooksByISBN = (isbnSubstring) => {
    return http.post('/books/search/isbn', { isbn_substring: isbnSubstring });
};

export const upload_url = "/api/uploads"

export const createOrder = (data) => {
  return http.post('/orders/create', data);
};


export const getUsersPaginated = (page = 1, perPage = 20) => {
  return http.post('/users/paginated', {'page':page, 'per_page':perPage});
};

export const getBooksPaginated = (page = 1, perPage = 20) => {
  return http.post('/books/paginated', {'page':page, 'per_page':perPage});
};
export const getOrdersPaginated = (page = 1, perPage = 20) => {
  return http.post('/orders/paginated', {'page':page, 'per_page':perPage});
};

 export const updateUser = (data) => {
    return http.post('/users/update', data);
};

export const getReviewRatingStats = (bookId) => createRestfulAPI(`/bookreviews/${bookId}`);
export const getReviewListPaginated = (bookId) => createRestfulAPI(`/bookreviewscontent/${bookId}`);
export const createReview = (data) => http.post('/bookreviews/create', data);
