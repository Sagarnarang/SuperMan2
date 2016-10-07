# Do Lower everything
# Correct decoded_body_message = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'])
# DB Dolower Case in Applciationregex
#mathworks application compelte
from __future__ import print_function
import httplib2
import os, base64
import nltk

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import re
from pymongo import MongoClient

#nltk.download()




# Use a database already created on mongolab
server = 'ds041939.mongolab.com'
port = 41939
db_name = 'user_name'
username = 'sagar'
password = 'sagar'

# connect to server
conn = MongoClient(server, port)

# Get the database
print('\nGetting database ...')
db = conn[db_name]

# Have to authenticate to get access
print('\nAuthenticating ...')
db.authenticate(username, password)

# Get the documents
posts = db.traffic
print(posts)
print('\nNumber of posts', posts.find().count())

# cursor = db.traffic.find()
# for document in cursor:
#     # print(document)

all_regex = ''
# find
cursor = db.applicationRegex.find()
# print(cursor)

# trigger = False;
regex_pos_array = []
regex_neg_array=[]
for document in cursor:
        if(document['key'] == 'positive'):
            regex_pos_array.append(document['regex'])
        if(document['key'] == 'negative'):
            regex_neg_array.append(document['regex'])
print("POS---->",regex_pos_array)
print("NEG---->",regex_neg_array)



#regex_text="\b|".join(regex_array)
#regex_text='We will review your application\b|\bThank you for applying to\b|\bRegarding your application for\b'
# regex_text = '\bThank\b \byou\b \bfor\b \bapplying\b'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    #
    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])

    ListMessagesWithLabels(service, 'me', ['INBOX'])
def main1():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])
    return labels

    #ListMessagesWithLabels(service, 'me', ['INBOX'])


def GetAttachments(service, user_id, msg_id, store_dir):
    """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                file_data = base64.urlsafe_b64decode(part['body']['data']
                                                     .encode('UTF-8'))

                path = ''.join([store_dir, part['filename']])

                f = open(path, 'w')
                f.write(file_data)
                f.close()

    except:
        print('An error occurred: %s')

def parts_of_speech(corpus):
    "returns named entity chunks in a given text"
    sentences = nltk.sent_tokenize(corpus)
    tokenized = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = [nltk.pos_tag(sentence) for sentence in tokenized]
    chunked_sents = nltk.ne_chunk_sents(pos_tags)
    return chunked_sents


def find_entities(chunks):
    "given list of tagged parts of speech, returns unique named entities"

    def traverse(tree):
        "recursively traverses an nltk.tree.Tree to find named entities"

        entity_names = []

        if hasattr(tree, 'label') and tree.label:
            #print(tree.label())
            if tree.label() == 'ORGANIZATION':
                entity_names.append(' '.join([child[0] for child in tree]))
            else:
                for child in tree:
                    entity_names.extend(traverse(child))

        return entity_names

    named_entities = []

    for chunk in chunks:

        entities = sorted(list(set([word for tree in chunk
                                    for word in traverse(tree)])))
        for e in entities:
            if e not in named_entities:
                named_entities.append(e)
    return named_entities

def GetMessage(service, user_id, msg_id):
    #print("vguchxjk")
    """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """




    from_val = ""
    subject_val = ""
    curr_date = ""
    decoded_body_message = ""


    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        # print(message)

        # print(message)
        for t in message['payload']['headers']:
            # print(t['name'])
            # if t['name'] == 'Received':
            #     print('aaaaaaaaaaa',t['value'])
            if t['name'] == 'From':
                from_val = t['value']
            if t['name'] == 'Subject':
                subject_val = t['value']
            if t['name'] == 'Date':
                curr_date = t['value']
            # print(encoded_body_message.strip())

        #print("aaaa")
        print(subject_val)

        # tokens = nltk.word_tokenize(subject_val)
        # pos_tags = nltk.pos_tag(tokens)
        # tree=nltk.ne_chunk(pos_tags)
        named_entities=[]
        entity_chunks = parts_of_speech(subject_val)
        named_entities.append(find_entities(entity_chunks))
        #print(named_entities)

        for t in message['payload']:
            if t=='parts':
                #print("hello")
                decoded_body_message = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'])
                print("1")
            if t=='partId':
                decoded_body_message = (base64.urlsafe_b64decode(message['payload']['body']['data']))
                print("2")
        # if message['payload']['partId'] == "":
        #     print("in if")
        #     decoded_body_message = (base64.urlsafe_b64decode(message['payload']['body']['data']))
        # if message['payload']['parts'] != "":
        #     print("elseeeeeeeeee")
        #     decoded_body_message = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'])
        #print(decoded_body_message)
        decoded_body_utf_8 = decoded_body_message.decode("utf-8")
        #t = re.sub('<.*>', ' ', decoded_body_utf_8)
        t1 = re.sub('[^A-Za-z0-9\']+', ' ', decoded_body_utf_8)
        ne_from_email=[]
        f1=from_val.split('@')
        for u in f1:
            k=re.sub("<|>","",u)
            entity_chunks2 = parts_of_speech(k)
            named_entities1 = find_entities(entity_chunks2)
            if named_entities1:
               named_entities.append(named_entities1)

        print(named_entities)



        # result = db.shubhamTest.insert_one(
        #     {
        #         "from": from_val,
        #         "subject": subject_val,
        #         "date": curr_date,
        #         "body": t1,
        #         "status": "Applied",
        #         "company_name": named_entities
        #     }
        # )

        #print(re.search('.*' + '\bThank\b' + '.*', t))
        toggle = False;
        for regex_elem in regex_pos_array:
            if re.search(('.*'+ regex_elem+ '.*').lower(), t1.lower()) or re.search(('.*'+ regex_elem+ '.*').lower(), subject_val.lower()):
                print("POS MATCH FOUND")
                #print(subject_val)
                #print(decoded_body_utf_8)
                toggle = True
                result = db.pos.insert_one(
                    {
                        "from": from_val,
                        "subject": subject_val,
                        "date": curr_date,
                        "body": t1,
                        "status": "Applied",
                        "company_name": named_entities
                    }
                )
                break
        for regex_elem in regex_neg_array:
            if re.search(('.*' + regex_elem + '.*').lower(), t1.lower()) or re.search(('.*'+ regex_elem+ '.*').lower(), subject_val.lower()):
                print("NEG MATCH FOUND")
                #print(subject_val)
                #print(decoded_body_utf_8)
                toggle = True
                result = db.neg.insert_one(
                    {
                            "from": from_val,
                            "subject": subject_val,
                            "date": curr_date,
                            "body": t1,
                            "status": "Reject",
                            "company_name": named_entities
                        }
                    )
            break





        # //To decode the strign and remove 'B'
        # ahsubh = decoded_body_message.decode("utf-8")
        # print(ahsubh)

        # print(message['payload']['parts'])
        # str = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'])
        # print(str.strip())
        print("_______________________")
        # print(base64.urlsafe_b64decode(message['raw'].encode('ASCII')))



        return message

    except:
        print('Cant get text')




def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        # print(messages)
        for m in messages:
            # print(m['threadId'])
            # print(m['raw'])
            GetMessage(service, 'me', m['threadId'])
            # GetAttachments(service,'me',m['threadId'],'~/t')
            # print('______')
            # return messages
    except:
        print("dsd")


if __name__ == '__main__':
    main()
