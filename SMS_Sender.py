from twilio.rest import Client
import SMS_Keys as keys
import datetime


#Teste para sender de Sms

class Keys:
    def __init__(self,sid='',auth='',phone='',twi=''):
        self.account_sid = sid
        self.auth_token = auth
        self.phone_number = phone
        self.twilio_number = twi

p1 = Keys('AC181d5aa4483d49b433293e0ecd022abf','70faadb9a1cb0ccf799daf05000eeb56','+5534999062849','+12512701223')
p2 = Keys('AC0029589ef042a554df4ab8b701d4ddd8','0c39ad69c4e34d9145a1cbb3e327e818','+5534988315291','+12513019853')

# def messageSender():

#     client = Client(keys.account_sid,keys.auth_token)

#     message = client.messages.create(
#         body="TEST MESSAGE",
#         from_=keys.twilio_number,
#         to=keys.target_number
#     )

#     return message

# print(messageSender().body)

import subprocess
def sendmessage(p):
    """Sender com curl e POO"""
    date = str(datetime.datetime.now()).split(":")[:2]
    message=f"TESTE {date[0]}:{date[1]}"
    apiurl = "https://api.twilio.com/2010-04-01/Accounts/AC181d5aa4483d49b433293e0ecd022abf/Messages.json"
    method = "POST"
    to = f"--data-urlencode To={p.phone_number}"
    from_ = f"--data-urlencode From={p.twilio_number}"
    access = f"-u {p.account_sid}:{p.auth_token}"
    msgbody = f"--data-urlencode Body=\"{message}\""
    sender = f"curl {apiurl} -X {method} {to} {from_} {msgbody} {access}"


    print(f"send to {p.phone_number}")
    z = subprocess.Popen(sender, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)

    print(z)

sendmessage(p1)
sendmessage(p2)