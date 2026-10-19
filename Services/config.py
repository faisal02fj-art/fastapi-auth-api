import os
from dotenv import load_dotenv

load_dotenv()




class Setting:
    db_url = os.getenv("DB_url")
    secret_kay = os.getenv("secret_key")
    algorithem = os.getenv("Algorithem")
    access_token_exp_time = os.getenv("access_token_expire_time")
    



setting = Setting()