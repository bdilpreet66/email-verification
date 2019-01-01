from django.urls import path, re_path
from . import views

app_name = 'verify'

urlpatterns = [
    path('list/',views.ListUpload,name='list'),
    path('single/',views.SingleEmail,name='single'),
    re_path(r'^download/(?P<pk>\d+)/$',views.Download,name='download')
]

