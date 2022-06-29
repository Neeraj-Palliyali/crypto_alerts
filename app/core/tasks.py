from celery import shared_task
from utils.get_live_price import get_live_price_btc
from utils.mail_helper import send_mails
from .models import UserAlert

@shared_task
def check_price(*args):
    data = []
    price = get_live_price_btc()
    alerts = UserAlert.objects.filter(status = "A", alert_on = "L", limit__gt = price) 
    if alerts:
        data.append(check_and_trigger(alerts))
    
    alerts = UserAlert.objects.filter(status = "A", alert_on = "LE", limit__gte = price) 
    if alerts:
        data.append(check_and_trigger(alerts))
    
    alerts = UserAlert.objects.filter(status = "A", alert_on = "E", limit = price) 
    if alerts:
        data.append(check_and_trigger(alerts))
    
    alerts = UserAlert.objects.filter(status = "A", alert_on = "G", limit__lt = price) 
    if alerts:
        data.append(check_and_trigger(alerts))

    alerts = UserAlert.objects.filter(status = "A", alert_on = "GE", limit__lte = price) 
    if alerts:
       data.append(check_and_trigger(alerts))

    return {"response" : data}

def check_and_trigger(alerts):
    data = []
    for alert in alerts:
            alert.status = "T"
            alert.save()
            if alert.user.email:
                sub = f"The price limit set {alert.limit} has been reached"
                email = alert.user.email
                message = f"The price limit set {alert.limit} has been reached. The requested price has been reached!!"
                status = send_mails(subject= sub, user_email= email, message= message)
                data.append(
                        {
                        "user":alert.user.username,
                        "status": str(status),
                        "message":"Send the mail"
                        }
                    )
            else: 
                data.append(
                        {
                        "user":alert.user.username,
                        "message": "User has not set a mail-id"
                        }
                    )
    return data