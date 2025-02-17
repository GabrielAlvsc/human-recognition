import psycopg2
from twilio.rest import Client
import subprocess
import datetime

# Substitua com suas credenciais do Twilio

class Keys:
    def __init__(self,sid='',auth='',phone='',twi=''):
        self.account_sid = sid
        self.auth_token = auth
        self.phone_number = phone
        self.twilio_number = twi

p1 = Keys('AC181d5aa4483d49b433293e0ecd022abf','70faadb9a1cb0ccf799daf05000eeb56','+5534999062849','+12512701223')

client = Client(p1.account_sid, p1.auth_token)

def send_sms(phone_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=p1.twilio_number,
            to=phone_number
        )
        print(f"Message sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

def send_sms_curl(p, camera):
        
        date = str(datetime.datetime.now()).split(":")[:2]
        message=f"Ei tem humano aqui na {camera}, em {date[0]}:{date[1]}"
        apiurl = "https://api.twilio.com/2010-04-01/Accounts/AC181d5aa4483d49b433293e0ecd022abf/Messages.json"
        method = "POST"
        to = f"--data-urlencode To={p.phone_number}"
        from_ = f"--data-urlencode From={p.twilio_number}"
        access = f"-u {p.account_sid}:{p.auth_token}"
        msgbody = f"--data-urlencode Body=\"{message}\""
        sender = f"curl {apiurl} -X {method} {to} {from_} {msgbody} {access}"
        try:
            m = subprocess.Popen(sender, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            print(f"Message sent to {p.phone_number}")
        except Exception as e:
            print(f"Failed to send message to {p.phone_number}: {e}")  


def fetch_and_send_messages(Camera_Name):
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="engcomp1413",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT telefone FROM telefones LIMIT 1")

    """
    
    Aqui o Sistema deveria pegar todos os números celulares cadastrados no banco de dados,
    como estamos usando a versão trial do Twilio, apenas um número pode ser verificado, 
    logo, não há necessidade para o uso de banco de dados nesta versão, apenas com a versão
    paga do twilio faria sentido o seu uso, podendo enviar sms para vários telefones 
    simultaneamente
    
    
    """
    
    
    #phone_number = cursor.fetchone()
    # if phone_number:
        #send_sms(phone_number[0], "Ei tem humano aqui " + Camera_Name)
    send_sms_curl(p1, Camera_Name)

    # conn.close()


