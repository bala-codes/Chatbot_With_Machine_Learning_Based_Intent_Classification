import pickle, json, random
import numpy as np
import smtplib

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)
    
with open("pac_chatbot_classifier.pkl","rb") as fin:
    vectorizer, PA_classifier = pickle.load(fin)

with open("sgd_chatbot_classifier.pkl","rb") as fin:
    vectorizer, SGD_classifier = pickle.load(fin)

# Required Functions to predict the News
def prediction(text):
    test = vectorizer.transform(text)
    output, probs = ensemble(test)
    return output, probs

def ensemble(x):
    pred1 = PA_classifier._predict_proba_lr(x)
    pred2 = SGD_classifier.predict_proba(x)
    
    test_pred_prob = np.mean([pred1, pred2], axis=0)
    pred = np.argmax(test_pred_prob, axis=1)
    return pred, test_pred_prob

def send_reset_email_smtp(user_email, context, send_mail=False):
    if send_mail:
        import smtplib
        from email.message import EmailMessage
        import re
        docname = (re.findall(r'\bDr.[a-zA-Z]+\b', mail_list))[0]
        day = (re.findall(r'\b[a-zA-Z]+day\b', mail_list))[0]
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        gmail_user="PROVIDE FROM EMAIL ADDRESS HERE"
        gmail_password=r"PROVIDE FROM EMAIL ADDRESS'S PASSWORD HERE"
        Server=smtplib.SMTP_SSL('smtp.gmail.com')
        Server.login(gmail_user,gmail_password) #Kal-El@12"
        text="Hello, we have confirmed your appointment with {} on {}. Thanks".format(docname, day)
        msg = MIMEText(text)
        msg["Subject"] = "Doctor Appointment - Confirmation Email "
        Server.sendmail(gmail_user,str(user_email),msg.as_string().encode('utf-8'))
        Server.quit()

actual = ['appointment', 'confirm', 'goodbye', 'greeting', 'payments', 'thanks', 'unknown']
print("Let's chat! (type 'quit' to exit)")
while True:
    x = input("You : ")
    if x == "quit":
        break
    x=[x,]
    pred, probs = prediction(x)
    tag = str(actual[pred[0]])
    if probs[0][pred[0]] > 0.10:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = str(random.choice(intent['responses']))
                print("{} : {}".format("ALTRA", response))
                if tag == "appointment":
                    mail_list = response
                if tag == "confirm":
                	# SET IT TO TRUE TO START SENDING EMAILS
                    send_reset_email_smtp(user_email="PROVIDE SENDER EMAIL HERE", context = str(mail_list), send_mail=False) # SET IT TO TRUE TO START SENDING EMAILS
            
    else:
        print("{} : {}".format("ALTRA",  "I do not understand..."))