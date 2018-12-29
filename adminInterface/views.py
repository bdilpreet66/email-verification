from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DeleteView,UpdateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import AskAnyThing,CreateNewForm,EditForm,QuestionForm,UserForm,ReportForm
from .models import Articles, Questions, Report
# Create your views here.


class TopicListView(ListView):
    models = Articles
    context_object_name = 'topics'
    template_name = 'admin_interface/topics_list.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Articles.objects.order_by('-date_added')
        return queryset
    

def ArticleDisplay(request,pk):
    topic = get_object_or_404(Articles, pk=pk)
    return render(request,'admin_interface/article.html',{'topic':topic})

@login_required
def CreateNewArticle(request):
    
    if request.method == 'POST':
        form = CreateNewForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('site:topic_list')
    else:
        form = CreateNewForm()
    return render(request,'admin_interface/new_article.html',{'form':form})   

@login_required
def ArtileUpdateView(request,pk):
    topic = get_object_or_404(Articles, pk=pk)

    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            topic.author = request.user
            topic.content = article.content
            topic.pics = article.pics
            topic.date_added = timezone.now()
            topic.save()
            return redirect('site:topic_list')
    else:
        form = EditForm()
    return render(request,'admin_interface/edit_article.html',{'form':form,'topic':topic})

@method_decorator(login_required, name='dispatch')
class AuthorDelete(DeleteView):
    model = Articles
    template_name = 'admin_interface/delete_post.html'
    success_url = reverse_lazy('site:topic_list')

@login_required
def AnswerView(request,pk):
    question = get_object_or_404(Questions, pk=pk)

    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            question.answered_by = request.user
            question.answered = True
            question.answer = answer.answer
            question.save()
        return redirect('site:ques_list')

    else:
        form = QuestionForm()

    return render(request,'admin_interface/question_answer.html',{'form':form,'question':question})

@method_decorator(login_required, name='dispatch')
class QuestionsListView(ListView):
    models = Articles
    context_object_name = 'questions'
    template_name = 'admin_interface/question_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Questions.objects.filter(answered=False)
        return queryset

@login_required
def update_profile(request,pk):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            user = get_object_or_404(User, pk=pk)
            user.first_name = data.first_name
            user.last_name = data.first_name
            user.email = data.email
            user.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'admin_interface/profile.html', {'form':form})

def ReportView(request):
    reports = Report.objects.filter(resolved=False).order_by("-date_added")
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"you report has been submitted. We will try to resolve it as soon as possible")

        return redirect('site:report')

    else:
        form = ReportForm()
    return render(request,'admin_interface/report.html',{'form':form,'reports':reports})

def CustomerCare(request):
    questions = Questions.objects.all().order_by("-date_added")
    if request.method == 'POST':
        form = AskAnyThing(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"you question has been submitted. We will try to get to you as soon as possible")

        return redirect('site:ask')

    else:
        form = AskAnyThing()
    return render(request,'admin_interface/q&a.html',{'form':form,'questions':questions})