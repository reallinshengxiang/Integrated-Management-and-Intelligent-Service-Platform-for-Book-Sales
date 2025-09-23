<h1 align="center">
Integrated Management and Intelligent Service Platform for Book Sales   <a href="https://www.producthunt.com/products/github-187?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-github&#0045;a41a339b&#0045;8021&#0045;445f&#0045;99a8&#0045;52daa25145ef" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1018217&theme=dark&t=1758628116694" alt="GitHub - Efficient&#0032;book&#0032;sales&#0032;platform&#0032;powered&#0032;by&#0032;Flask&#0032;&#0038;&#0032;PostgreSQL | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>   
</h1>

<div align="center">
[![](https://img.shields.io/github/stars/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/forks/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/license/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales/blob/main/LICENSE)
</div>

This project is a Flask-based framework for small and medium-sized book sales enterprises or online bookstore book management system , the user scale covers from a few hundred to thousands of customer groups , it has a user management , book management , order management , review management and other functions . The system uses SQLAlchemy to interact with PostgreSQL database, builds RESTful API with the help of Flask-RESTful, and uses Flask-JWT-Extended to realize authentication.       
The system adopts a layered architecture design, which is mainly divided into the following levels: 
- The presentation layer (API layer) is responsible for receiving requests from the client and returning the processing results to the client. The Flask-RESTful framework is used to build the RESTful API, providing interfaces for user authentication, book management, order management, etc.    
- The business logic layer (service layer) handles user authentication, book management, order management, and so on. The business logic layer (service layer) handles specific business logic, such as the creation, update and deletion of books, and the creation, update and deletion of orders. The service layer calls the interface of the data access layer to realize data persistence.    
- The data access layer (model layer) is responsible for interacting with the database, including data addition, deletion, modification and retrieval operations. SQLAlchemy is used as an ORM tool to map database tables to Python classes to facilitate database operations.    
- Database layer Stores all the data of the system and uses PostgreSQL as the database management system. The database contains several tables such as user information, book information, order information, comment information and so on.    
## Quick start
### Deepseek-V3 token fetch
Go to [Github Marketplace](https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3-0324) and click Use this model to fetch the token, then add the token to BookStoreSystem/.env
```shell
SECRET_KEY=get_your_SECRET_KEY
JWT_SECRET_KEY=get_your_JWT_SECRET_KEY
DATABASE_URL=get_your_postgresql_DATABASE_URL
UPLOAD_FOLDER=uploads
GITHUB_TOKEN=get_your_Deepseek-V3_token
```     
Just replace get_your_Deepseek-V3_token with the fetched token   
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
bookreviews_processed.csv derived from Kaggle platform [Douban dataset(rating+review+side information)](https://www.kaggle.com/datasets/fengzhujoey/douban-datasetratingreviewside-information)  
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
npm run dev
``` 
Just open the link ([default](http://127.0.0.1:3000/#/auth/login)) to the browser      
If the following situations were encountered   
```shell 
linshengxiang@sxLin:~/Integrated Management and Intelligent Service Platform for Book Sales/BookStoreSystem/book_store_frontend$ npm run dev

> fontend@0.0.0 dev
> vite

sh: 1: vite: not found
```    
run  
```shell 
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --force --unsafe-perm
```   
Run again and it will run successfully!    
```shell 
npm run dev 
``` 
