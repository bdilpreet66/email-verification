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

