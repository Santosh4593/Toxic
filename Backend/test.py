from mongoengine import connect, Document, StringField, ListField, IntField, EmbeddedDocument, EmbeddedDocumentField

connect("Language", host="localhost", port=27017)

class test(Document):
    no = IntField()
    language = StringField()
    questions = ListField()
no = 5
print(test.objects.get(no=1).questions[no])
# print(check.questions[0])