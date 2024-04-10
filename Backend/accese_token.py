# from datetime import datetime, timedelta
# from jose import jwt
# # from Crypto.Hash import HMAC, SHA256, SHA384, SHA512


# SECRET_KEY = "f4eea8b977aad528bd410a66010cae2d44ae58dd5f38d1180bb6ef449b8ee2b5"
# ALGORITHM = "HS256"

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode =  data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
    
#     encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

from datetime import datetime, timedelta
import jwt

SECRET_KEY = "f4eea8b977aad528bd410a66010cae2d44ae58dd5f38d1180bb6ef449b8ee2b5"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
