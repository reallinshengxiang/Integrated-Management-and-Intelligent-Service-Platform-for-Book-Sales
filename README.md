<h1 align="center">
Integrated Management and Intelligent Service Platform for Book Sales    
</h1>

<div align="center">

[![](https://img.shields.io/github/stars/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/forks/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)
[![](https://img.shields.io/github/license/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales)](https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales/blob/main/LICENSE)
</div>

## Deepseek-V3 token fetch
Go to https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3-0324 and click Use this model to fetch the token, then add the token to BookStoreSystem/book_store_backend/app/service/user_service.py 
```shell
def deepseek_response(user_input):
    os.environ["GITHUB_TOKEN"] = "*"
    token = os.environ["GITHUB_TOKEN"] 
```     
Just replace "*" with the fetched token   
## Local database environment configuration   
### PostgreSQL Installation 
Go to the [Download page](https://www.postgresql.org/download/) of postgsql official website, choose the appropriate version to download and install    
PgAdmin 4 is the open source management tool of Postgres, [Installation link](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v9.4/windows/)    
### Runtime environment configuration  
Based on python3, download the corresponding installation package can be, will not be repeated here   
## Run   
### Clone repository to local    
```shell
git clone https://github.com/reallinshengxiang/Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales.git
```     
### Data set fetch (this step can be omitted, douban_books.csv and bookreviews_processed.csv are already in the Import_Data folder)     
Go to the Crawling file path and run   
```shell
python3 run1.py
```  
```shell
python3 run2.py
```  
At the end of the run there is the douban_books.csv    
bookreviews_processed.csv derived from [Kaggle platform public dataset](https://www.kaggle.com/datasets/fengzhujoey/douban-datasetratingreviewside-information)  
### Starting the postgres database
```shell 
sudo service postgresql start    
sudo -i -u postgres
```
### Data processing (based on douban_books.csv and bookreviews_processed.csv) 
Go to Import_Data file path and run 
```shell 
python3 import.py 
```
### Run the backend 
Go to book_store_backend file path, run 
```shell 
python3 run.py 
```
### Run the frontend 
Go to book_store_frontend file path, run 
```shell 
python3 run.py 
``` 
Just open the link to the browser      