# Integrated-Management-and-Intelligent-Service-Platform-for-Book-Sales   

Deepseek-V3 token获取方式：进入https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3-0324，点击Use this model，即可获取token，然后在BookStoreSystem/book_store_backend/app/service/user_service.py里面的
```shell
def deepseek_response(user_input):
    os.environ["GITHUB_TOKEN"] = "*"
    token = os.environ["GITHUB_TOKEN"] 
```    
将"*"换成获取的token即可