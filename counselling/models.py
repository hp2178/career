from django.db import models
from jsonfield import JSONField
# Create your models here.
class RegisterLogin(models.Model):
	username = models.CharField(max_length=30)
	email = models.EmailField()
	password = models.CharField(max_length=50,null=True)
	activated = models.BooleanField(default=False)

	def __str__(self):
		return self.username

class UserOTP(models.Model):
	username = models.CharField(max_length=30)
	email = models.EmailField()
	otp = models.CharField(max_length=5)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()

	def __str__(self):
		return self.username



class studentTable(models.Model):
	email = models.EmailField(null=True)
	name = models.CharField(max_length=50)
	scu = models.CharField(max_length=50)
	course = models.CharField(max_length=20)
	sem = models.DecimalField(max_digits=1,decimal_places=0)
	bday = models.DateField()
	gender = models.BooleanField()
	testGiven = models.BooleanField()
	EI = models.CharField(max_length=50,null=True, blank=True)
	SN = models.CharField(max_length=50,null=True, blank=True)
	TF = models.CharField(max_length=50,null=True, blank=True)
	JP = models.CharField(max_length=50,null=True,blank=True)
	json = JSONField(default={},null=True,blank=True)

	def __str__(self):
		return self.name