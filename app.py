import imaplib
import re
import credentials
import quopri
import pyttsx3

host = 'imap.gmail.com'
port = 993
user = credentials.user
password = credentials.password

server = imaplib.IMAP4_SSL(host,port)
server.login(user,password)
server.select()
status, data = server.search(None,'(FROM "newsletter@filipedeschamps.com.br" UNSEEN)')

if data[0]:
    d = data[0].split()
    ind = d[-1]
    btext = server.fetch(ind, "(BODY[1] BODY[HEADER.FIELDS (SUBJECT FROM)])")
    email_msg = btext[1][1][1]

    utf = quopri.decodestring(email_msg)
    text = utf.decode('utf-8')
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = text.replace('\r\n\r\n', '###').replace('\r\n', ' ').replace('###', '\r\n\r\n') #pode melhorar
    print(text)

    engine = pyttsx3.init()
    engine.setProperty("voice", engine.getProperty('voices')[0].id)
    engine.setProperty("rate", 250)
    engine.say(text)
    engine.runAndWait()
