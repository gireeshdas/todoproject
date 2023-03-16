from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from todoapp.decorators import signin_required
from django.utils.decorators import method_decorator

# Create your views here.
from todoapp.models import Todos


class SignUpView(CreateView):
    # def get(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm()
    #     return render(request,"registration.html",{"form":form})
    model=User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request, "your account has been created")
        return super().form_valid(form)


    # def post(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"your account has been created")
    #         return redirect("signin")
    #     else:
    #         messages.error(request,"Registration is failed")
    #         return render(request,"registration.html",{"form":form})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("login success")
                return redirect("index")
            else:
                messages.error(request,"invalid username and password")
                print("login failed")
                return render(request,"login.html",{"form":form})
        return render(request,"login.html")

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    # def get(self,request,*args,**kwargs):
    #     return render(request,"home.html")
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["todos"]=Todos.objects.filter(user=self.request.user,status=False)
        return context


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class TodoAddView(CreateView):
    # def get(self,request,*args,**kwargs):
    #     form=forms.TodoForm()
    #     return render(request,"add-todo.html",{"form":form})
    model=Todos
    form_class =forms.TodoForm
    template_name = "add-todo.html"
    success_url = reverse_lazy("todos-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo has been added")
        return super().form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     form=forms.TodoForm(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(request,"todo has been added")
    #         return redirect("index")
    #     else:
    #         messages.error(request,"failed")
    #         return render(request,"add-todo.html",{"form":form})


@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    # def get(self,request,*args,**kwargs):
    #     all_todos=Todos.objects.filter(user=request.user)
    #     return render(request,"todolist.html",{"todos":all_todos})
    model=Todos
    context_object_name="todos"
    template_name="todolist.html"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
@signin_required
def delete_todos(request,*args,**kwargs):
    print(request.user.is_authenticated)
    id=kwargs.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("todos-list")


@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":todo})
    model=Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"


@method_decorator(signin_required,name="dispatch")
class TodoEditView(UpdateView):
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo = Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(instance=todo)
    #     return render(request,"todo_edit.html",{"form":form})
    model = Todos
    form_class = forms.TodoChangeForm
    template_name = "todo_edit.html"
    success_url = reverse_lazy("todos-list")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        messages.success(self.request,"todo has been changed")
        return super().form_valid(form)



    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(request.POST,instance=todo)
    #     if form.is_valid():
    #         form.save()
    #         msg="todo has been changed"
    #         messages.success(request,msg)
    #         return redirect("todos-list")
    #     else:
    #         msg="todo update failed"
    #         messages.error(request, msg)
    #         return render(request,"todo_edit.html",{"form":form})