import requests
from main.models import OTP
from random  import *
import smtplib

#Sending Emails
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("planetsedn@gmail.com", "Sedn@planet7")


def sendotp(user):
    try:
        otp = OTP.objects.filter(receiver = user)
    except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
        otp = None
    if otp is not None:
        otp.delete()
    otp = randint(1000, 9999)
    data= OTP.objects.create(otp = otp, receiver = user)
    data.save

    YOUR_AUTH_KEY= "XxFiIJKC59ramYcLePpbtWQwMORlhnuv3VZdsHf682GU0AgzjyZovRucsp5VACU9M1KXlgiTQBHaISLD"
    url = "https://www.fast2sms.com/dev/bulkV2"
    messagesent = "Hello {}, Your OTP for Wofo24 is {}".format(user.name, otp)
    payload = "sender_id=TXTIND&message=" + str(messagesent)+"&route=v3&numbers=" +str(user.phone_number)
    headers = {
        'authorization': YOUR_AUTH_KEY,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    s.sendmail("sender_email_id", "ashutoshtitori@gmail.com", messagesent)

    # terminating the session
    s.quit()