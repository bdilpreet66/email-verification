from celery import shared_task
from django.utils.timezone import datetime,timedelta,now
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import csv,io
from django.conf import settings

# imports from app
from .models import Documents
from .VerifyEmailAddress import verify_email

@shared_task
def DeleteData():
    time_24_hours_ago = datetime.now() - timedelta(days=1)
    doc = Documents.objects.filter(uploaded_at__gte=time_24_hours_ago).delete()



@shared_task
def VerificationDone(url):
    email = Documents.objects.get(doc_name=url)
    subject, from_email, to = 'Download Link [no reply]' , settings.EMAIL_HOST_USER , [email.email,]

    with open(settings.BASE_DIR+"/templates/verifier/download_list_email.html") as f:
        message = f.read()
    message = EmailMultiAlternatives(subject=subject,body=message,from_email=from_email,to=to)
    html_template = get_template("verifier/download_list_email.html").render({'email':email})
    message.attach_alternative(html_template,"text/html")
    message.send()



@shared_task
def verify_list(url):
    File = Documents.objects.get(doc_name=url)
    myfile = []
    emails = []
    with open(f'media/{File.doc_name}','r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        count = 0
        for line in csv_reader:
            if count == 0:
                coloum_names = line
                for num in range(0,len(coloum_names)):
                    if 'email' == coloum_names[num].lower():
                        pos = num
                        count = count + 1
                        myfile.append(line)
            else:
                emails.append(line[pos])
                myfile.append(line)

    
    result = []
    user = []
    domain = []
    reason = []
    
    for email in emails:
        
        data = verify_email(email)
        
        if data['code'] == 250:
            result.append('Deliverable')
            user.append(data['user'])
            domain.append(data['domain'])
            reason.append(data['message'])
        elif data['code'] == 550:
            result.append('Undeliverable')
            user.append(data['user'])
            domain.append(data['domain'])
            reason.append(data['message'])
        else:
            user.append('unknown')
            domain.append('unknown')
            result.append('unknown')
            reason.append('unknown')


    for num in range(0,len(myfile)):
        if num == 0:
            myfile[num].append('user')
            myfile[num].append('domain')
            myfile[num].append('result')
            myfile[num].append('reason')
        else:
            myfile[num].append(user[num-1])
            myfile[num].append(domain[num-1])
            myfile[num].append(result[num-1])
            myfile[num].append(reason[num-1])
    
    with open(f'media/{File.doc_name}','w') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',')

        for line in myfile:
            csv_writer.writerow(line)
    
    File.verified = True
    File.uploaded_at = now()

    VerificationDone.delay(str(File.doc_name))

        
    
    
    
    
    





    