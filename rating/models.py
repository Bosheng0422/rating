from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length=50)
    # unique need
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return u'%s %s' %(self.code,self.name)

class Module(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    professor = models.ManyToManyField(Professor)

    def __str__(self):
        return u'%s %s %i %i' %(self.code,self.name,self.year,self.semester)


class Rate(models.Model):
    #  1-5-> rate range
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    professor = models.ForeignKey(Professor,on_delete=models.DO_NOTHING)
    module = models.ForeignKey(Module,on_delete=models.DO_NOTHING)
    fromw = models.CharField(max_length=30)

    def __str__(self):
        return u'%s %s %i' %(self.professor,self.module,self.rate)





