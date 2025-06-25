# Integrated Management and Intelligent Service Platform for Book Sales   

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