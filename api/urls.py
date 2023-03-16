
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api.views import TodoView
router=DefaultRouter()
router.register("todos",TodoView,basename="todos")

urlpatterns=[

]+router.urls