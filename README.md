<h1 align="center">
Integrated Management and Intelligent Service Platform for Book Sales    
</h1>

<div align="center">

[![](https://img.shields.io/github/stars/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/forks/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/license/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales/blob/main/LICENSE)
</div>

This project is a Flask-based framework for small and medium-sized book sales enterprises or online bookstore book management system , the user scale covers from a few hundred to thousands of customer groups , it has a user management , book management , order management , review management and other functions . The system uses SQLAlchemy to interact with PostgreSQL database, builds RESTful API with the help of Flask-RESTful, and uses Flask-JWT-Extended to realize authentication.     
The system adopts a layered architecture design, which is mainly divided into the following levels: the presentation layer (API layer) is responsible for receiving requests from the client and returning the processing results to the client. The Flask-RESTful framework is used to build the RESTful API, providing interfaces for user authentication, book management, order management, etc. The business logic layer (service layer) handles user authentication, book management, order management, and so on. The business logic layer (service layer) handles specific business logic, such as the creation, update and deletion of books, and the creation, update and deletion of orders. The service layer calls the interface of the data access layer to realize data persistence. The data access layer (model layer) is responsible for interacting with the database, including data addition, deletion, modification and retrieval operations. SQLAlchemy is used as an ORM tool to map database tables to Python classes to facilitate database operations. Database layer Stores all the data of the system and uses PostgreSQL as the database management system. The database contains several tables such as user information, book information, order information, comment information and so on.    
## Quick start
### Deepseek-V3 token fetch
Go to https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3-0324 and click Use this model to fetch the token, then add the token to BookStoreSystem/book_store_backend/app/service/user_service.py 
```shell
def deepseek_response(user_input):
    os.environ["GITHUB_TOKEN"] = "*"
    token = os.environ["GITHUB_TOKEN"] 
```     
Just replace "*" with the fetched token   
### Local database environment configuration   
#### PostgreSQL Installation 
Go to the [Download page](https://www.postgresql.org/download/) of postgsql official website, choose the appropriate version to download and install    
PgAdmin 4 is the open source management tool of Postgres, [Installation link](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v9.4/windows/)    
#### Runtime environment configuration  
Based on python3, download the corresponding installation package can be, will not be repeated here   
### Run   
#### Clone repository to local    
```shell
git clone https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales.git
```     
#### Data set fetch (This step can be omitted, douban_books.csv and bookreviews_processed.csv are already in the Import_Data folder)     
Go to the Crawling file path and run   
```shell
python3 run1.py
```  
```shell
python3 run2.py
```  
At the end of the run there is the douban_books.csv    
bookreviews_processed.csv derived from [Kaggle platform public dataset](https://www.kaggle.com/datasets/fengzhujoey/douban-datasetratingreviewside-information)  
#### Starting the postgres database
```shell 
sudo service postgresql start    
sudo -i -u postgres
```
#### Data processing (Based on douban_books.csv and bookreviews_processed.csv) 
Go to Import_Data file path and run 
```shell 
python3 import.py 
```
#### Run the backend 
Go to book_store_backend file path, run 
```shell 
python3 run.py 
```
#### Run the frontend 
Go to book_store_frontend file path, run 
```shell 
python3 run.py 
``` 
Just open the link to the browser      