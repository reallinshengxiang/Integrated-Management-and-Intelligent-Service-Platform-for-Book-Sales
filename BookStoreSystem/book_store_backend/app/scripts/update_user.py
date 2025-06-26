import psycopg2
from werkzeug.security import generate_password_hash

conn = None

# 获取数据库配置
db_config = {
    'user': 'linshengxiang',
    'password': 'Password!2025',
    'host': 'localhost',
    'port': '5433',
    'database': 'bookstoredb'
}

# 尝试从环境变量获取数据库 URL 并解析

try:
    # 建立数据库连接
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # 检查 root 用户是否存在
    cursor.execute("SELECT id FROM users WHERE username = 'root'")
    root_user = cursor.fetchone()

    if not root_user:
        # 如果 root 用户不存在，则创建 root 用户
        password_hash = generate_password_hash('root')
        cursor.execute(
            "INSERT INTO users (username, password_hash, user_type) VALUES (%s, %s, %s)",
            ('root', password_hash, 'admin')
        )
        print("Root 用户创建成功！")
    else:
        print("Root 用户已存在。")

    # 获取所有用户
    cursor.execute("SELECT id, username FROM users WHERE username != 'root'")
    users = cursor.fetchall()

    for user_id, username in users:
        # 修改其他用户的密码为其用户名
        password_hash = generate_password_hash(username)
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )

    # 提交更改
    conn.commit()
    print("所有用户的密码已更新。")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
finally:
    # 关闭数据库连接
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL 连接已关闭。")