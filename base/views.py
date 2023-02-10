from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "base/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-bar') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__istartswith=search_input)

        context['search_input'] = search_input
        return context
   


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"

    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task 
    fields = ['title','description','complete']
    success_url = reverse_lazy("tasks")


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task 
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
   

#register 
class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args: str, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPage,self).get(*args,**kwargs)

#user login
class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True 

    def get_success_url(self) -> str:
        return reverse_lazy('tasks')








# #create a registeration page using function based view
# def register_user(request):
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#     context = {'form':form}
#     return render(request,'base/register.html',context)

# def user_login(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request,username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 return redirect("tasks")
#             else:
#                 messages.info(request,'username or password is incorrect')

#         return render(request,'base/login.html')

# #logout login
# def logout_user(request):
#     logout(request)
#     return redirect("login")


