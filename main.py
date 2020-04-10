import spacy
import json

import random

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer

import sqlite3

import warnings
warnings.filterwarnings("ignore")

nlp = spacy.load("en_core_web_sm")

strings = [ u'What is my current balance',
            u'What is my balance',
            u'Tell me my balance',
            u'How much balance do I have',
            u'How much money I have',
            u'Check balance',
            u'Give my last transactions details',
            u'Give my account statement',
            u'Give me my mini statement',
            u'Generate my mini statement',
            u'Generate my account statement',
            u'Tell me my last transactions details']

def train():
    pipeline = "tensorflow_embedding"

    args = {"pipeline":pipeline}
    config = RasaNLUModelConfig(args)
    trainer = Trainer(config)

    training_data = load_data("training_data2.json")
    interpreter = trainer.train(training_data)
    return interpreter

interpreter = train()

conn = sqlite3.connect('banks.db')
c = conn.cursor()

def response(message):
    data = interpreter.parse(message)
    if(len(data["entities"])==0):
        Class = data["intent"]["name"]
  
        if Class == 'check_balance':
            query = "SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1"
            c.execute(query)
            responses = ["Your balance is Rs.{}" ,"You have Rs.{} in your account"]
            results = c.fetchall()
        
            print("Bot: "+random.choice(responses).format(list(*results)[0]))

        if Class == 'account_statement':
            query = "SELECT TimeStamp,Type,Amount,Location,Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 5"
            c.execute(query)
            results = c.fetchall()
            balance = results[0][4]
            n = len(results)
            for i in range(n):
                print (str(results[i][0])+" "+str(results[i][1])+" "+str(results[i][2])+" "+str(results[i][3]))
            print ("Current balance is Rs.",balance)
        if Class == 'about_bot':
            print ("Bot: " + random.choice(["My name is Intelligent Bot","You can call me Intelligent Bot"]))

        if Class == 'work_bot':
            print ("Bot: " + random.choice(["I am here to help you. I can fetch your account and transaction details","I am here to assist you by providing easier access to your account details"]))

        if Class == 'greet':
            print ("Bot: " + random.choice(["Hi! there","Hello! There","Hi","Hello"]))

    else:
        dic = data["entities"][0]
        if(dic["confidence"]<0.5):
            print("Sorry, I didn't understand the question :(")
        else:
            Class = dic["entity"]
            if Class == 'money':
                query = "SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1"
                c.execute(query)
                responses = ["Your balance is Rs.{}" ,"You have Rs.{} in your account"]
                results = c.fetchall()
                index = min(len(results),len(responses)-1)
                print("Bot: "+random.choice(responses).format(list(*results)[0]))
            elif Class == 'statement':
                query = "SELECT TimeStamp,Type,Amount,Location,Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 5"
                c.execute(query)
                results = c.fetchall()
                balance = results[0][4]
                n = len(results)
                for i in range(n):
                    print (str(results[i][0])+" "+str(results[i][1])+" "+str(results[i][2])+" "+str(results[i][3]))
                print ("Current balance is Rs.",balance)
  
            elif Class == 'about_bot':
                print ("Bot: " + random.choice(["My name is Giannini-The Bank Bot","You can call me Giannini-The Bank Bot"]))
            elif Class == 'work_bot':
                print ("Bot: " + random.choice(["I am here to help you. I can fetch your account and transaction details","I am here to assist you by providing easier access to your account details"]))
            elif Class == 'greet':
                print ("Bot: " + random.choice(["Hi! there","Hello! There","Hi","Hello"]))
            else:
                print ("Bot: " + random.choice(["Sorry, I didn't understand the question :(","I don't know the answer for this"]))
