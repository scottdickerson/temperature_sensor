import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email

def sendEmail(to, subject, body):
    email_user = "ssd.temperaturesensor@gmail.com"
    email_password = "yekd jbte ggpb cqgm"
    print("sending email subject %s, body %s" % (subject, body))
    
    try:
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body,"plain"))
            
        text = msg.as_string()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_password)
        
        server.sendmail(email_user, to, text)
        
        server.quit()
    except:
       print("error sending email")
    

def sendEmailTemperatureWarning(temperature, desired_temperature, humidity, desired_humidity):
    subject = "Temperature/Humidity warning"
    body = "Too Cold! %sF, Desired Temp: %sF or Too Humid: %s%%, Desired Humidity: %s%%" % (temperature, desired_temperature, humidity, desired_humidity)
    email_send="dickerson.sd@gmail.com"
    sendEmail(to=email_send, subject=subject, body=body)
        
def send_acknowledgement(temperature, humidity, action):
    body = "Acknowledging message, desired temperature %s, desired humidity %s, desired action %s" % (temperature, humidity, action)
    subject = "Acknowledge"
    email_send="dickerson.sd@gmail.com"
    sendEmail(to=email_send, subject=subject, body=body)
    
    
def parse_subject(subject):
    print("msg subject: %s" % subject)
    new_temperature, new_humidity, new_action = None, None, None
    desired_temperature = subject.split("TEMP:")
    desired_action = subject.split("ACTION:")
    desired_humidity = subject.split("HUM:")
    if len(desired_temperature) == 2:
        new_temperature = int(desired_temperature[1].strip())
        print("new_temperature: %s" % new_temperature)
    if len(desired_action) == 2:
        new_action = desired_action[1].strip()
        print("new_action: %s" % new_action)
    if len(desired_humidity) == 2:
        new_humidity = int(desired_humidity[1].strip())
        print("new_humidity: %s" % new_humidity)
    return (new_temperature, new_humidity, new_action)
    
def check_for_new_control_messages():
    M=imaplib.IMAP4_SSL(host="imap.gmail.com", port=993)
    M.login("ssd.temperaturesensor@gmail.com","qasp jahh abta sdkf")
    M.select()
    temperature, humidity, action = None, None, None
    # Look for new emails to set the temperature
    typ, data = M.search(None, "(UNSEEN)", "(FROM {0})".format("dickerson.sd@gmail.com"))
    if len(data[0]) == 0:
        print("No new messages")
    for num in data[0].split():
            typ, data = M.fetch(num, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode("utf-8"))
                    msg_subject = msg["subject"]
                    temperature, humidity, action = parse_subject(subject=msg_subject)
                    
            # print("newTemperatureConstraint %s" % 
            
    M.close()
    M.logout()
    if temperature != None or humidity != None or action != None:
        send_acknowledgement(temperature=temperature, humidity=humidity, action=action)
        return (temperature, humidity, action)
    return (None, None, None)

# print("new messages", check_for_new_control_messages())


