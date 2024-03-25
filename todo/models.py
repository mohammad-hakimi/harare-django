from django.db import models
from django.db.models import CharField, BooleanField, AutoField, Model



class Todo(models.Model):
    id = AutoField(primary_key=True, unique=True)
    name = CharField(max_length=200)
    is_done = BooleanField(default=False)
