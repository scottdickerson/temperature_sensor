import imaplib
import email

def parse_subject(subject):
    print("msg subject: %s" % msg_subject)
    desired_temperature = msg_subject.split("TEMP:")
    desired_action = msg_subject.split("ACTION:")
    if len(desired_temperature) == 2:
        new_temperature = int(desired_temperature[1].strip())
        print("new_temperature: %s" % new_temperature)
    if len(desired_action) == 2:
        new_action = desired_action[1].strip()
        print("new_action: %s" % new_action)
    
def check_for_new_control_messages:
    M=imaplib.IMAP4_SSL(host="imap.gmail.com", port=993)
    M.login("ssd.temperaturesensor@gmail.com","qasp jahh abta sdkf")
    M.select()
    # Look for new emails to set the temperature
    typ, data = M.search(None, "(UNSEEN)", "(FROM {0})".format("dickerson.sd@gmail.com"))
    if len(data[0]) == 0:
        print("No new messages")
    for num in data[0].split():
            typ, data = M.fetch(num, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    print("email message: %s" % response_part[1].decode("utf-8"))
                    msg = email.message_from_string(response_part[1].decode("utf-8"))
                    msg_subject = msg["subject"]
                    parse_subject(subject=msg_subject)
                    
            # print("newTemperatureConstraint %s" % 
            
    M.close()
    M.logout()

