from django.db import models
from django.core.validators import EmailValidator,FileExtensionValidator

# Create your models here.


class Documents(models.Model):
    email = models.CharField(max_length = 60,validators=[EmailValidator])
    doc_name = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __Str__(self):
        return self.doc_name

class IPUsers(models.Model):
    ip_address = models.CharField(max_length=120, default='ABC')
    visted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    def __str__(self):
        return self.ip_address