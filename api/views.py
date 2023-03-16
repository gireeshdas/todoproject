from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api.serializers import TodoSeralizer
from todoapp.models import Todos
from rest_framework import authentication,permissions

# Create your views here.
class TodoView(ModelViewSet):
    queryset = Todos.objects.all()
    serializer_class = TodoSeralizer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    # def list(self,request,*args,**kwargs):
    #     todos=Todos.object.filter(user=request.user)
    #     seralizer=TodoSeralizer(todos,many=True)
    #     return Response(data=seralizer.data)
    #

    def create(self, request, *args, **kwargs):
        serializer=TodoSeralizer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)