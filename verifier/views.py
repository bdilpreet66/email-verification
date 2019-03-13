from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
import csv
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


from . import forms
from . import models
from .tasks import verify_list
from .VerifyEmailAddress import verify_email
# Create your views here.


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def Index(request):
    return render(request,'Index.html',{'form':forms.ListForm()})

def SingleEmail(request):
    data = []
    cur_email = "none"
    
    if request.method == 'POST':
        form = forms.SingleForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            cur_email = email.email
            datadict = verify_email(email.email)

            data.append(datadict['user'])
            data.append(datadict['domain'])
            data.append(datadict['code'])
            
            if datadict['code'] == 250:
                data.append('deliverable')
                data.append(datadict['message'])
                data.append('True')
            elif datadict['code'] == 550:
                data.append('undeliverable')
                data.append(datadict['message'])
                data.append('True')
            else:
                data.append('Unknown')
                data.append(datadict['message'])
                data.append('False')

        form = forms.SingleForm()
        return render(request,'verifier/Single_email.html',{'form':form,'data':data,'email':cur_email})
    else:
        form = forms.SingleForm()

    return render(request,'verifier/Single_email.html',{'form':form,'data':data,'email':cur_email})

def ListUpload(request):
    my_ip = get_ip(request)
    ip = models.IPUsers.objects.get(ip_address=my_ip)
    
    if request.method == "POST":
        form = forms.ListForm(request.POST,request.FILES)
        if form.is_valid():
            email_list = form.save(commit=True)
            with open(f'media/{email_list.doc_name}','r') as csv_file:
                csv_reader = csv.reader(csv_file,delimiter=',')
                count = 0
                for column in csv_reader:
                    if count == 0:
                        for col_names in column:
                            if col_names == 'email':
                                count = count + 1
                        if count == 1:
                            url = str(email_list.doc_name)
                            verify_list.delay(url)
                            ip,created = models.IPUsers.objects.get_or_create(ip_address=my_ip)
                            ip.visted = True
                            ip.timestamp = timezone.now()
                            ip.save()
                            messages.success(request,"The File has been submitted Successfully. You will recieve an email when your file has been verified")
                        else:
                            messages.error(request,"This csv file doesn't contain the emails column or there are 2 columns named 'email' ")
                        count = count + 1
                    else:
                        break
        else:
            messages.error(request,'No csv file detected')            
            
        return redirect('verify:list')

    else:
        form = forms.ListForm

    return render(request,'verifier/List_upload.html',{'ip':ip,'form':form})

def Download(request,pk):
    File = get_object_or_404(models.Documents, pk=pk)

    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="Verified_Emails_list.csv"'

    with open(f'media/{File.doc_name}','r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')

        writer = csv.writer(response, delimiter=',')

        for obj in csv_reader:
            writer.writerow(obj)

    return response