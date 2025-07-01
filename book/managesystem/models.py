from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model
# Create your models here.

class User(AbstractUser):
    pass


class booksmanage(models.Model):
      name =  models.CharField(max_length=256)
      content = models.CharField(max_length=256)
      img = models.CharField(max_length=512)
      is_active= models.BooleanField(default=True)
      borrow = models.ForeignKey(User,on_delete= CASCADE,null=True,blank=True,related_name="borrowed")
      def _str_(self):
          return f"{self.name} {self.content} {self.is_active} {self.borrow}"
