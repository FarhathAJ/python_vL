#models.py
from django.db import models

class chkboxoption(models.Model):
    optionvalue=models.CharField(max_length=100)