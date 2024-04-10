
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
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware

from fastapi import status
import cv2
import base64
import io
from detect_expression import detect_emotion
import numpy as np
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
global emotion 
questionnaire = {
    'happy': ['How often do you experience feelings of happiness or joy?', 'Can you identify specific activities or situations that consistently make you happy?', 'On a scale of 0 to 3, how would you rate your current level of happiness?', 'Are there some goals or aspirations that bring you a sense of happiness?', 'In the past week, how often did you engage in activities you find genuinely enjoyable?', 'Do you share your happiness with others, if at all?'],
    'neutral': ['How often you feel emotionally neutral or balanced?', 'Are there specific circumstances where you tend to feel emotionally neutral?', 'On a scale of 0 to 3, how would you rate your current emotional neutrality?', 'How do you typically react when faced with a neutral or uneventful situation?', 'Can you recall a recent experience where you felt emotionally neutral, and how did you handle it?', 'Do you prefer to maintain emotional neutrality?'],
    'sad': ['How often do you experience feelings of sadness or hopelessness?', 'Can you identify specific triggers for feelings of sadness in your life?', 'On a scale of 0 to 3, how would you rate your current level of sadness?', 'How do you typically cope with feelings of sadness or despair?', 'How did you manage a situation that made you feel sad in the past?', 'Are there certain environments or people that tend to amplify your feelings of sadness?'],
    'angry': ['How do you typically handle feelings of anger or frustration?', 'Are there specific situations that consistently make you feel angry?', 'On a scale of 0 to 3, how would you rate your current level of anger?', 'What level of healthy outlets you use to release or manage anger?', 'How do you communicate your anger to others, if at all?', 'Are there patterns or triggers in your daily life that contribute to feelings of anger?'],
}

score_mapping = {
    'Rarely or never': 0,
    'Occasionally': 1,
    'Often': 2,
    'Almost always': 3,
    'No': 0,
    'Sometimes': 1,
    'Frequently': 2,
    'Always': 3,
    'Not at all': 0,
    'Slightly': 1,
    'Moderately': 2,
    'Very': 3,
    'None': 0,
    'A few': 1,
    'Several': 2,
    'Many': 3,
    'Not handled': 0,
    'Handled poorly': 1,
    'Handled moderately': 2,
    'Handled well': 3,
    'React strongly': 0,
    'Mild reaction': 1,
    'Neutral reaction': 2,
    'No reaction': 3,
    'Not neutral at all': 0,
    'Slightly neutral': 1,
    'Moderately neutral': 2,
    'Very neutral': 3,
    'Not applicable': 0,
    'Handled well': 1,
    'Handled moderately': 2,
    'Handled properly': 3,
    'Ineffective coping': 0,
    'Somewhat effective': 1,
    'Moderately effective': 2,
    'Highly effective': 3,
    'No outlets': 3,
    'Mild outlets': 2,
    'Moderate outlets': 1,
    'Effective outlets': 0,
    'Not communicated': 3,
    'Mild communication': 2,
    'Moderate communication': 1,
    'Direct communication': 0,
    'Not handled at all': 3,
    'Poorly handled': 2,
    'Moderately handled':1 ,
    'Well handled': 0,

}




app = FastAPI()  #creating the app


#make sure to change the database name and the port number
connect("Language", host="localhost", port=27017) #connecting to the database



#to allow the frontend to access the backend CORS is used
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

async def calculate_total_score(responses):
    total_score = 0
    for response in responses:
        total_score += score_mapping.get(response, 0)
    return total_score

@app.get("/")
def read_root():
    return {"message": "The Endpoint is working and implemented by @atharva-malode in fast api"}

#route to signup
# @app.post("/signup")
# def sign_up(new_user: NewUser):
#     if(User.objects.filter(username=new_user.username).count() > 0):
#       return {"message": "User already exists"}
#     user = User(username=new_user.username, password=get_password_hash(new_user.password), total_score=new_user.total_score,mental_health=new_user.mental_health)
#     user.save()
#     return {"message": "Signup successful"}

@app.post("/signup")
def sign_up(new_user: NewUser):
    if(User.objects.filter(username=new_user.username).count() > 0):
      return {"message": "User already exists"}
    user = User(username=new_user.username, password=get_password_hash(new_user.password), total_score=new_user.total_score,mental_health=new_user.mental_health)
    user.save()
    
    # Your code to save the new user to the database
    
    # Send confirmation email
    sender_email = "rahulbeast5162@gmail.com"  # Your Gmail address
    sender_password = "juse vxzn nguz fyuh"  # Your Gmail password
    receiver_email = new_user.email  # Email of the user who signed up

    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to our platform"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the HTML version of the email
    html = f"""\
    <html>
      <body>
        <p>Hi {new_user.username},</p>
        <p>Thank you for signing up!</p>
        <p>Best regards,</p>
        <p>Your Platform Team</p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print(f"Error sending email: {e}")
    
    return {"message": "Signup successful. Confirmation email sent."}

#route to login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends() ):
    
    username = form_data.username
    password = form_data.password

    if authenticate_user(username, password):
       accese_token = create_access_token(data={"sub": username},expires_delta=timedelta(days=20))
       return {"access_token": accese_token, "token_type": "bearer"}
    else:
         raise HTTPException(status_code=400, detail="Incorrect username or password")
         # return {"message": "Incorrect username or password"
    # return {"message": "Login successful"}


#route to get the user data
@app.get("/user_data")
def get_user_data(token: str = Depends(oauth2_scheme)):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_token.get("sub")

    try:
        user_data = json.loads(User.objects.filter(username=username).to_json())
        if user_data:
            return {"username": username, "data": user_data}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")
    

@app.post("/detect_emotion")
async def analyze_emotion(file: UploadFile = File(...)):
    contents = await file.read()
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)

    # Perform emotion detection
    result_img, emotion = await detect_emotion(image)

    # Convert the result image to base64 format
    _, img_encoded = cv2.imencode(".jpg", result_img)
    img_base64 = base64.b64encode(img_encoded).decode("utf-8")

    return {"emotion": emotion, "result_image_base64": img_base64}

@app.post("/detect_emotion_and_questionnaire")
async def analyze_emotion_and_questionnaire(emotion):
    if not emotion:
        return {"error": "Please provide responses for the questionnaire."}

    questions = questionnaire.get(emotion, [])
    
    # Create options for each question (you can customize these options)
    options = {
        'rarely_options': ['Rarely or never', 'Occasionally', 'Often', 'Almost always'],
        'frequency_options': ['No', 'Sometimes', 'Frequently', 'Always'],
        'scale_options': ['Not at all', 'Slightly', 'Moderately', 'Very'],
        'handling_options': ['Not handled','Handled poorly' ,'Handled moderately','Handled well' ],
        'handling_angry_options': [ 'Well handled','Moderately handled', 'Poorly handled', 'Not handled at all',],
        'many_options': ['None', 'A few', 'Several','Many'],
        'react_options': ['React strongly', 'Mild reaction', 'Neutral reaction', 'No reaction'],
        'neutral_options': ['Not neutral at all', 'Slightly neutral', 'Moderately neutral', 'Very neutral'],
        'coping_options': ['Ineffective coping', 'Somewhat effective', 'Moderately effective', 'Highly effective'],
        'outlets_options': [ 'Effective outlets', 'Moderate outlets','Mild outlets','No outlets', ],
        'communication_options': ['Direct communication', 'Moderate communication', 'Mild communication','Not communicated', ]
    }

    # Combine questions and options
    question_options = []
    for question in questions:
        if 'How often do you experience feelings of happiness or joy?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['rarely_options']})
        elif 'Can you identify specific activities or situations that consistently make you happy?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})
        elif 'On a scale of 0 to 3, how would you rate your current level of happiness?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['scale_options']})
        elif 'Are there some goals or aspirations that bring you a sense of happiness?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['many_options']})
        elif 'In the past week, how often did you engage in activities you find genuinely enjoyable?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['rarely_options']})
        elif 'Do you share your happiness with others, if at all?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['rarely_options']})

        # Neutral questions
        elif 'How often you feel emotionally neutral or balanced?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['rarely_options']})
        elif 'Are there specific circumstances where you tend to feel emotionally neutral?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})
        elif 'On a scale of 0 to 3, how would you rate your current emotional neutrality?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['scale_options']})
        elif 'How do you typically react when faced with a neutral or uneventful situation?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['react_options']})
        elif 'Can you recall a recent experience where you felt emotionally neutral, and how did you handle it?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['handling_options']})
        elif 'Do you prefer to maintain emotional neutrality?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})

        # Sadness questions
        elif 'How often do you experience feelings of sadness or hopelessness?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['rarely_options']})
        elif 'Can you identify specific triggers for feelings of sadness in your life?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})
        elif 'On a scale of 0 to 3, how would you rate your current level of sadness?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['scale_options']})
        elif 'How do you typically cope with feelings of sadness or despair?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['coping_options']})
        elif 'How did you manage a situation that made you feel sad in the past?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['handling_options']})
        elif 'Are there certain environments or people that tend to amplify your feelings of sadness?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})

        # Anger questions
        elif 'How do you typically handle feelings of anger or frustration?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['handling_angry_options']})
        elif 'Are there specific situations that consistently make you feel angry?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})
        elif 'On a scale of 0 to 3, how would you rate your current level of anger?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['scale_options']})
        elif 'What level of healthy outlets you use to release or manage anger?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['outlets_options']})
        elif 'How do you communicate your anger to others, if at all?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['communication_options']})
        elif 'Are there patterns or triggers in your daily life that contribute to feelings of anger?' in question:
            question_options.append({'emotion': emotion, 'question': question, 'options': options['frequency_options']})
    # result_img = await result_img
    return { "questions": question_options, "total_score": 0}




@app.post("/save_user_data", response_model=UserSummary)

def save_user_data(user_data: UserSummary, token: str = Depends(oauth2_scheme),):
    # Decode the token to get the username
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_token.get("sub")

    try:
        # Find the user in the database
        user = User.objects.get(username=username)
        # Update the user data
        print("Total score:", user_data.total_score)
        print("Mental health: ", user_data.mental_health)
        user.total_score = user_data.total_score
        user.mental_health = user_data.mental_health
        
        user.save()
        # Return the saved data
        return user_data
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving user data: {str(e)}")
