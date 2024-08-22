from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import joblib
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


def read_blacklist():
    with open("blacklist.pkl", "rb") as f:
        blacklist = pickle.load(f)
    return blacklist


def read_whitelist():
    with open("whitelist.pkl", "rb") as f:
        whitelist = pickle.load(f)
    return whitelist


def checkDomain(email):
    for i in range(len(email)):
        if email[i] == '@':
            return email[i + 1:]


def preprocess(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    clean = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return clean


df = pd.read_csv("spam_ham_dataset.csv", encoding="latin-1")

df['label'] = df['label'].map({'ham': 0, 'spam': 1})
X = df['text']

cv = CountVectorizer(analyzer=preprocess)
X = cv.fit_transform(X)

model = open('Spam_Model_NB.pkl', 'rb')
clf = joblib.load(model)

SCOPES = ['https://mail.google.com/']


def emailID(email_message: str):
    index1 = email_message.index('<')
    index2 = email_message.index('>')
    emailId = email_message[index1 + 1: index2]
    return emailId


def parse_msg(msg):
    if msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode(
            "utf-8")
    return msg.get("snippet")


def categorize(filetype: str):
    spam_java = 'Label_8258242173550416670'
    spam_xml = 'Label_4565116085086163832'
    spam_c = 'Label_7329977587918988189'
    spam_cpp = 'Label_4456113970713848893'
    uncategorized = "Label_7989813089040811452"
    if filetype == 'java':
        return 1, spam_java
    elif filetype == 'xml':
        return 1, spam_xml
    elif filetype == 'c':
        return 1, spam_c
    elif filetype == 'cpp':
        return 1, spam_cpp
    else:
        return 1, uncategorized


def getEmails():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'
    while True:
        result = service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()
        messages = result.get('messages')

        if messages is not None:
            for msg in messages:
                m_id = msg['id']
                txt = service.users().messages().get(userId='me', id=m_id).execute()
                mail = service.users().messages().get(userId='me', id=m_id, format="full").execute()
                payload = txt['payload']
                headers = payload['headers']
                sender = ''
                for d in headers:
                    if d['name'] == 'From':
                        sender = d['value']

                emailId: str = emailID(sender)
                strin = parse_msg(mail)
                strin = strin.replace('\n', ' ').replace('\r', '')
                isUrl= bool(re.search(r"http\S+", strin))
                strin = re.sub(r"http\S+", "", strin)
                print(str(strin))

                blacklist = read_blacklist()
                whitelist = read_whitelist()
                validDomain = ["gmail.com", "outlook.com"]
                if checkDomain(emailId) not in validDomain:
                    service.users().messages().modify(userId='me', id=m_id,
                                                      body={'addLabelIds': [
                                                          'Label_7304197249788543017']}).execute()
                    my_prediction = [2]
                elif emailId in blacklist:
                    my_prediction = [1]
                elif emailId in whitelist:
                    my_prediction = [0]
                else:
                    data = [strin]
                    vect = cv.transform(data).toarray()
                    my_prediction = clf.predict(vect)

                categorized = 0
                list_categorised = []
                for part in txt['payload']['parts']:
                    if part['filename']:
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:
                            att_id = part['body']['attachmentId']
                            att = service.users().messages().attachments().get(userId='me', messageId=m_id,
                                                                               id=att_id).execute()

                        path = part['filename']
                        explode = path.split('.')
                        filetype = explode[-1]

                        ext = categorize(filetype)
                        categorized: int = ext[0]

                        list_categorised.append(ext[1])

                if my_prediction[0] == 1:
                    if emailId not in blacklist:
                        blacklist.append(emailId)
                        with open("blacklist.pkl", "wb") as f:
                            pickle.dump(blacklist, f)
                    if len(list_categorised) != 0:
                        for i in list_categorised:
                            service.users().messages().modify(userId='me', id=m_id,
                                                              body={'removeLabelIds': ['UNREAD'], 'addLabelIds': [
                                                                  i]}).execute()
                            if isUrl:
                                service.users().messages().modify(userId='me', id=m_id,
                                                                  body={'addLabelIds': [
                                                                      'Label_5104572477944027038'],
                                                                      'removeLabelIds': ['UNREAD']}).execute()
                    if categorized == 0 and not isUrl:
                        service.users().messages().modify(userId='me', id=m_id,
                                                          body={'addLabelIds': ['Label_7989813089040811452'],
                                                                'removeLabelIds': ['UNREAD']}).execute()

                    elif isUrl:
                        service.users().messages().modify(userId='me', id=m_id,
                                                          body={'addLabelIds': ['Label_5104572477944027038'],
                                                                'removeLabelIds': ['UNREAD']}).execute()
                elif my_prediction[0] == 0:
                    if emailId not in whitelist:
                        if categorized != 0 or isUrl:
                            service.users().messages().modify(userId='me', id=m_id,
                                                          body={'addLabelIds': ['Label_2194034260334748011']}).execute()
                    service.users().messages().modify(userId='me', id=m_id,
                                                      body={'removeLabelIds': ['UNREAD']}).execute()
                    print("HAM")

                else:
                    service.users().messages().modify(userId='me', id=m_id,
                                                      body={'removeLabelIds': ['UNREAD']}).execute()


if __name__ == '__main__':
    getEmails()
