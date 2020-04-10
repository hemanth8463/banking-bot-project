import main
import sys
if sys.version_info[0] >= 3:
    unicode = str
while True:
    message = unicode("User: "+input())
    if message == unicode("User: Thankyou") or message ==  unicode("User: Thanks") or message ==  unicode("User: thankyou") or message ==  unicode("User: thanks"):
        print("Bot: Welcome, I am exiting")
        break
    main.response(message)
    
    
#INSTALL THESE FILES

# pip install -U spacy

# pip install rasa_nlu

# python -m spacy download en_core_web_sm

# pip install sklearn-crfsuite