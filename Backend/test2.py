# from tensorflow.keras.layers import TextVectorization
# import pandas as pd 
# import os
# import tensorflow as tf

# df = pd.read_csv(os.path.join('jigsaw-toxic-comment-classification-challenge','train.csv', 'train.csv'))

# X = df['comment_text']
# y = df[df.columns[2:]].values

# MAX_FEATURES = 200000 # number of words in the vocab

# vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
#                                output_sequence_length=1800,
#                                output_mode='int')

# vectorizer.adapt(X.values)
# vectorized_text = vectorizer(X.values)

# model = tf.keras.models.load_model('toxicity.h5')

# def score_comment(comment):
#     vectorized_comment = vectorizer([comment])
#     results = model.predict(vectorized_comment)
    
#     text = ''
#     for idx, col in enumerate(df.columns[2:]):
#         text += '{}: {}\n'.format(col, results[0][idx]>0.5)
    
#     print(text)
#     return text

# score_comment('you are a fucking fat ass')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, APIRouter
from mongoengine import connect, DoesNotExist
from models import User, NewUser, test, QuestionRequest, AddQuestionRequest, UserSummary
import json
from datetime import timedelta
from pass_hash import get_password_hash
from user_auth import authenticate_user
from accese_token import create_access_token, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import jwt
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.layers import TextVectorization
import pandas as pd 
import os
import tensorflow as tf

app = FastAPI()

connect("Toxic", host="localhost", port=27017) #connecting to the database

# Load the model and text vectorizer
model = tf.keras.models.load_model('toxicity.h5')

MAX_FEATURES = 200000  # number of words in the vocab
vectorizer = TextVectorization(
    max_tokens=MAX_FEATURES,
    output_sequence_length=1800,
    output_mode='int'
)

# Assuming 'train.csv' is in the same directory as the script
df = pd.read_csv(os.path.join('jigsaw-toxic-comment-classification-challenge', 'train.csv','train.csv'))

X = df['comment_text']
y = df[df.columns[2:]].values

vectorizer.adapt(X.values)

# Define request body model
class Comment(BaseModel):
    comment_text: str

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#route to signup
@app.post("/signup")
def sign_up(new_user: NewUser):
    if(User.objects.filter(username=new_user.username).count() > 0):
      return {"message": "User already exists"}
    user = User(username=new_user.username, password=get_password_hash(new_user.password), total_score=new_user.total_score,mental_health=new_user.mental_health)
    user.save()
    return {"message": "Signup successful"}
# Define scoring endpoint


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if authenticate_user(username, password):
        # Fetch the user from the database
        user = User.objects(username=username).first()

        # Check if the user exists and if their total_score is less than or equal to 3
        if user and (not user.total_score or user.total_score <= 3):
            access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(days=20))
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=403, detail="User not allowed to log in due to high total_score")
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

         # return {"message": "Incorrect username or password"
    # return {"message": "Login successful"}
    
# @app.post("/score_comment/")
# async def score_comment(comment: Comment):
#     vectorized_comment = vectorizer([comment.comment_text])
#     results = model.predict(vectorized_comment)

#     scores = {}
#     for idx, col in enumerate(df.columns[2:]):
#         scores[col] = bool(results[0][idx] > 0.5)

#     return scores

@app.post("/score_comment/")
async def score_comment(comment: Comment, token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token to extract the username
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("sub")

        vectorized_comment = vectorizer([comment.comment_text])
        results = model.predict(vectorized_comment)

        count = 0  # Initialize count to 0
        scores = {}
        for idx, col in enumerate(df.columns[2:]):
            score = bool(results[0][idx] > 0.5)
            scores[col] = score
            if score:  # If the value is True
                count = 0  # Set count to 1 and break the loop
                break

        # Check if there are more true values and increment count by 1 if so
        if any(scores.values()):
            count += 1

        user = User.objects(username=username).first()

        if user:
            # Update the total score
            user.total_score += count
            user.save()
            return {"message": "Total score updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating total score: {str(e)}")



# @app.put("/update_total_score")
# def update_total_score(new_total_score: int, token: str = Depends(oauth2_scheme)):
#     try:
#         # Decode the JWT token to extract the username
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = decoded_token.get("sub")

#         # Retrieve the user from the database
#         user = User.objects(username=username).first()

#         if user:
#             # Update the total score
#             user.total_score = new_total_score
#             user.save()
#             return {"message": "Total score updated successfully"}
#         else:
#             raise HTTPException(status_code=404, detail="User not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating total score: {str(e)}")
    
@app.get("/count")
def get_total_score(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token to extract the username
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("sub")

        # Retrieve the user from the databasse
        user = User.objects(username=username).first()

        if user:
            return {"total_score": user.total_score}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving total score: {str(e)}")