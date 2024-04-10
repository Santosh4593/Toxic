from mongoengine import Document, StringField, ListField, IntField, EmbeddedDocument, EmbeddedDocumentField, FloatField
from typing import Optional
from pydantic import BaseModel

#list of questionsin the user document wich user has attempted weather it is wrong or right
class Question(EmbeddedDocument):
    question = StringField()
    answer = StringField()
    time_taken = StringField()
    points = IntField()

#the User class is used to manipulate the data of the user in the database
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    # questions = ListField(StringField())
    # answers = ListField(StringField())
    total_score = IntField()
    mental_health = StringField()
    email = StringField()


class UserSummary(BaseModel):
    total_score: int
    mental_health: str
# class User(Document):
#     username = StringField(unique=True)
#     password = StringField()

#request data for adding a new user  : used in sign up
    


class NewUser(BaseModel):
    username: str
    password: str
    # questions: Optional[list[list]] = None
    # answers: Optional[list[list]] = None
    total_score: Optional[int] = 0
    mental_health: Optional[str] = None
    email: Optional[str]=None
    # language: Optional[list] = None

#used to retrive questions 
class test(Document):
    no = IntField()
    language = StringField()
    questions = ListField()    

#request data for adding a new question : used in add_question
class QuestionRequest(BaseModel):
    question_no: int
    old_answer: bool 
    old_level: str
    language: str

#add the users answer for a question in users collection
class AddQuestionRequest(BaseModel):
    question: str
    answer: str
    time_seconds: Optional[str] = "15 seconds"
    excercise_no : Optional[int] = 1
    points: int