import imaplib
import credentials
from bs4 import BeautifulSoup
import quopri
import pyttsx3

host = 'imap.gmail.com'
port = 993
user = credentials.user
password = credentials.password

server = imaplib.IMAP4_SSL(host,port)
server.login(user,password)
server.select("Deschamps")
status, data = server.search(None,"(UNSEEN)")

for num in data[0].split():
    status, data = server.fetch(num, "(RFC822)")
    email_msg = data[0][1]

    soup = BeautifulSoup(markup=email_msg,features="lxml")
    news = soup.find_all("td")[0].text

    utf = quopri.decodestring(news)
    text = utf.decode('utf-8')

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[2].id)
    engine.setProperty("rate", 250)
    engine.say(text)
    engine.runAndWait()