from django.contrib import admin
from counselling.models import RegisterLogin,UserOTP,studentTable
# Register your models here.
admin.site.register(RegisterLogin)
admin.site.register(UserOTP)
admin.site.register(studentTable)