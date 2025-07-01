from django.urls import  path

from . import  views

urlpatterns = [
    path("",views.index, name ="index"),
    path("login",views.login_view ,name= "login"),
    path("logout", views.logout_view , name= "logout"),
    path("register", views.register, name="register"),
    path("select",views.select, name ="select"),
    path("borrowbook",views.borrowbook,name="borrowbook"),
    path ("back",views.back, name="back")
]