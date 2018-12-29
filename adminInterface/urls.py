from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'site'

urlpatterns = [
    path('topics_list/',views.TopicListView.as_view(),name='topic_list'),
    re_path(r'^author/u(?P<pk>\d+)/profile/$',views.update_profile,name='profile'),
    re_path(r'^article/(?P<pk>\d+)/$',views.ArticleDisplay,name='display_article'),
    re_path(r'^article/(?P<pk>\d+)/delete/$',views.AuthorDelete.as_view(),name='delete'),
    re_path(r'^article/(?P<pk>\d+)/edit/$',views.ArtileUpdateView,name='edit'),
    re_path(r'^q&a/(?P<pk>\d+)/edit/$',views.AnswerView,name='reply'),
    re_path(r'^q&a/list/$',views.QuestionsListView.as_view(),name='ques_list'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='admin_interface/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(),name='logout'),
    path('article/new/',views.CreateNewArticle,name='new'),
    path('report/',views.ReportView,name="report"),
    path('q&a/',views.CustomerCare,name='ask'),
]
