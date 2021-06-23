import smtplib

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("planetsedn@gmail.com", "Sedn@planet7")

message = "Message_you_need_to_send"

# sending the mail
s.sendmail("sender_email_id", "receiver_email_id", message)

# terminating the session
s.quit()