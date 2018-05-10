from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
#from AiHiring.scratch_10 import *
from django.http import FileResponse
#from openpyxl import Workbook
from django.conf import settings
#import nltk
#from nltk.corpus import stopwords 
#import re
#import difflib
import hashlib
from counselling.models import RegisterLogin,UserOTP,studentTable
from social.apps.django_app.default.models import UserSocialAuth
from django.core.exceptions import ObjectDoesNotExist
import smtplib
import datetime as dt
from datetime import timedelta
from random import randint
from email.mime.text import MIMEText
#import pytz
#import os
#from wsgiref.util import FileWrapper
import mimetypes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from social_core.pipeline.partial import partial
from django.contrib.sessions.models import Session
'''
from datetime import datetime
from django.http import HttpResponseRedirect

class SessionExpiredMiddleware:
    def process_request(request):
        last_activity = request.session['last_activity']
        now = datetime.now()
        print(now,"%s" % (now.minute),last_activity,"%s" % (last_activity.minute)) 
        last_activity1 = int(last_activity.minute)
        now1 = int(now.minute)
        
        if now1 - last_activity1 > 1:
            # Do logout / expire session
            # and then...
            return HttpResponseRedirect("LOGIN_PAGE_URL")

        if not request.is_ajax():
            # don't set this for ajax requests or else your
            # expired session checks will keep the session from
            # expiring :)
            request.session['last_activity'] = now

'''
@csrf_exempt
def index(request):
	return render(request,'counselling/index.html')

@csrf_exempt
def pp(request):
	return render(request,'counselling/pp.html')

@csrf_exempt
def pf(request):
	return render(request,'counselling/pf.html')

@csrf_exempt
def au(request):
	return render(request,'counselling/au.html')








@csrf_exempt
def handler404(request):
	print('i M IN handler404.......................................................')
	return render(request, 'counselling/404.html', status=404)

@csrf_exempt
def handler403(request):
	print('i M IN handler403.......................................................')
	return render(request, 'counselling/403.html', status=403)

@csrf_exempt
def handler500(request):
	print('i M IN handler500.......................................................')
	return render(request, 'counselling/500.html', status=500)


@csrf_exempt
def handler400(request):
	print('i M IN handler400.......................................................')
	return render(request, 'counselling/400.html', status=400)



@csrf_exempt
def home(request):
	if request.method == 'POST' and (request.POST.get('buy1')=='100' or request.POST.get('buy2')=='200' or request.POST.get('buy3')=='300' or request.POST.get('buy4')=='400' or request.POST.get('buy5')=='500' or request.POST.get('buy6')=='600'):
		return redirect(reverse('payment:process'))
	return render(request,'counselling/home.html')




@csrf_exempt
def contact(request):
	return render(request,'counselling/contact.html')



@csrf_exempt
def help(request):
	return render(request,'counselling/help.html')

@csrf_exempt
def aboutTest(request):
	return render(request,'counselling/aboutTest.html')







@csrf_exempt
def dashboard(request):
	if request.method == 'POST' and request.POST.get('pswdCHNG')=='pswdCHNG':
		#username=request.POST['username2']
		newpswd=request.POST['newpass']
		renewpswd=request.POST.get('renewpass')
		change=RegisterLogin.objects.get(username=request.session['username'])
		#print(newpswd,"NEWWWWWW")
		#####hash_object = hashlib.md5(newpswd.encode('utf-8')).hexdigest()
		#print(hash_object.hexdigest())
		######RegisterLogin.objects.create(companyname=tem[0],username=tem[1],email=tem[2],password=hash_object.hexdigest())
		change.password = hashlib.md5(newpswd.encode('utf-8')).hexdigest()
		change.username = request.session['username']
		change.email = request.session["email"]
		change.companyname = "harsh"
		#print("halellujahhhhhhhhhhhhhhhhhhhh")
		change.save()
		return render(request, 'counselling/dashboard.html')
	else:
		return render(request, 'counselling/dashboard.html')

@csrf_exempt
def loggedin(request):
	print(request.user.username)
	print(request.user.id)
	#if request.user.is_anonymous:
	#	print("jjjjjjjj")
	#if request.user.is_authenticated:
	#	print("yes")
	#else:
	#	print('no')
	#print(request.COOKIES)
	#print('session')
	#print(request.session)
	#user = User.objects.get(username='HarshPatel')
	#print(user.email)
	#print(request.user.email)
	request.session['currUser']=request.user.email

	#request.session.set_expiry(45)
	#request.session['last_activity'] = datetime.now()
	#SessionExpiredMiddleware.process_request(request)
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	print(request.user.email)
	try:
		RegisterLogin.objects.get(email=request.user.email)
		try:
			st=studentTable.objects.get(email=request.user.email)
			print(st.email,st.name,st.gender,st.scu,st.bday)
			try:
				leng=len(st.json)
			except:
				leng=0
			return render(request, 'counselling/taby.html',{'ls1dd':leng})
		except:
			return render(request, 'counselling/loggedin.html')
		#return render(request,'counselling/loggedin.html',{'impmsg':'This email is already registered. Thank You.'})
	except:
		RegisterLogin.objects.create(username=request.user.username,email=request.user.email,activated=True)
		try:
			st=studentTable.objects.get(email=request.user.email)
			print(st.email,st.name,st.gender,st.scu,st.bday)
			try:
				leng=len(st.json)
			except:
				leng=0
			return render(request, 'counselling/taby.html',{'ls1dd':leng})
		except:
			return render(request, 'counselling/loggedin.html')
		#return render(request,'counselling/loggedin.html')

def logout(request):
	from django.contrib.auth import logout
	print('m logging out..........')
	logout(request)
	return redirect('/counselling/dashboard.html')


@csrf_exempt
def page(request):
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	save1=studentTable.objects.get(email=request.session['currUser'])
	save1Dict=save1.json
	print(save1Dict)
	try:
		leng=len(save1Dict)
	except:
		leng=0
		save1Dict={}
	print(leng)
	return render(request, 'counselling/page.html',{'ls1d':leng})

userCareer={'ESTJ': 'Chef','ISTJ': 'Systems administrator','ESFJ': 'Registered nurse','ISFJ': 'Kindergarten teacher','ESTP': 'Military officer',
			'ISTP': 'Police officer','ESFP': 'Bartender','ISFP': 'Jeweler','ENTJ': 'Physician','INTJ': 'Microbiologist','ENFJ': 'Minister',
			'INFJ': 'Veterinarian','ENTP': 'Reporter','INTP': 'College professor','ENFP': 'Landscape architect','INFP': 'Fine artist'
}

@csrf_exempt
def frc(request):
	save1=studentTable.objects.get(email=request.session['currUser'])
	save1Dict=save1.json
	answer=[]
	userTrait=''
	print(save1Dict)
	for _ in range(1,len(save1Dict)+1):
		answer.append(save1Dict[str(_)])
	column1=[0,7,14,21,28,35,42,49,56,63]
	column2=[1,8,15,22,29,36,43,50,57,64]
	column3=[2,9,16,23,30,37,44,51,58,65]
	column4=[3,10,17,24,31,38,45,52,59,66]
	column5=[4,11,18,25,32,39,46,53,60,67]
	column6=[5,12,19,26,33,40,47,54,61,68]
	column7=[6,13,20,27,34,41,48,55,62,69]
	cntA=0
	cntB=0
	for _ in column1:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	for _ in column2:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	if cntA>cntB:
		userTrait+='E'
	else:
		userTrait+='I'
	extro=(cntA/20)*100
	intro=(cntB/20)*100
	if extro>=50:
		ei=extro
		labelEI="Extrovert"
	else:
		ei=intro
		labelEI="Introvert"
	cntA=0
	cntB=0
	for _ in column3:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	for _ in column4:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	if cntA>cntB:
		userTrait+='S'
	else:
		userTrait+='N'
	sens=(cntA/20)*100
	intu=(cntB/20)*100
	if sens>=50:
		sn=sens
		labelSN="Sensing"
	else:
		sn=intu
		labelSN="Intuition"
	cntA=0
	cntB=0
	for _ in column5:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	for _ in column6:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	if cntA>cntB:
		userTrait+='T'
	else:
		userTrait+='F'
	think=(cntA/20)*100
	feel=(cntB/20)*100
	if think>=50:
		tf=think
		labelTF="Thinking"
	else:
		tf=feel
		labelTF="Feeling"
	cntA=0
	cntB=0
	for _ in column7:
		if answer[_]=='a':
			cntA+=1
		else:
			cntB+=1
	judge=(cntA/10)*100
	perce=(cntB/10)*100
	if extro>=50:
		jp=judge
		labelJP="Judging"
	else:
		jp=perce
		labelJP="Perceiving"
	if cntA>cntB:
		userTrait+='J'
	else:
		userTrait+='P'
	#return render(request,'counselling/reports.html',{'e_ei':extro,'i_ei':intro,'s_sn':sens,'n_sn':intu,'t_tf':think,'f_tf':feel,'j_jp':judge,'p_jp':perce})
	return render(request,'counselling/frc.html',{'mycareer':userCareer[userTrait],'ei':ei,'labelEI':labelEI,'sn':sn,'labelSN':labelSN,'tf':tf,'labelTF':labelTF,'jp':jp,'labelJP':labelJP})






@csrf_exempt
def view(request):
	print(request.POST)
	if 'N' in request.POST.get('E'):
		E='NA'
		I='NA'
	else:
		E=round(float(request.POST.get('E')),2)
		I=round(float(request.POST.get('I')),2)
	if 'N' in request.POST.get('S'):
		S='NA'
		N='NA'
	else:
		S=round(float(request.POST.get('S')),2)
		N=round(float(request.POST.get('N')),2)
	if 'N' in request.POST.get('T'):
		T='NA'
		F='NA'
	else:
		T=round(float(request.POST.get('T')),2)
		F=round(float(request.POST.get('F')),2)
	if 'N' in request.POST.get('J'):
		J='NA'
		P='NA'
	else:
		J=round(float(request.POST.get('J')),2)
		P=round(float(request.POST.get('P')),2)
	Json={}
	Json=studentTable.objects.get(email=request.POST.get('email')).json
	print(Json)
	if len(Json)==0:
		for _ in range(1,71):
			Json[str(_)]='-'
	return render(request,'counselling/view.html',{'Json':Json,'course':request.POST.get('course'),'scu':request.POST.get('scu'),'email':request.POST.get('email'),'sem':request.POST.get('sem'),'tg':request.POST.get('tg'),'bday':request.POST.get('bday'),'name':request.POST.get('name'),'gender':request.POST.get('gender'),'E':E,'I':I,'S':S,'N':N,'T':T,'F':F,'J':J,'P':P})





@csrf_exempt
def auth(request):
	if request.method == 'POST' and request.POST.get('login')=='login':
		tem = request.POST.get('username')
		try:
			
			cheese_blog = RegisterLogin.objects.get(username=tem)
			
			#print(cheese_blog,";;;;;;;;;;;;;;;;;;;;;")
			#print(cheese_blog.password,request.POST.get('password'))
			#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
			if hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()==cheese_blog.password and cheese_blog.activated==True:
				if request.method=='POST' and request.POST.get('login')=='login':
					print(request.POST.get('username'),type(request.POST.get('username')))
					ch=RegisterLogin.objects.get(username=request.POST.get('username'))
					request.session['currUser'] = ch.email
					#print(user.email,request.session['currUser'])
					try:
						st=studentTable.objects.get(email=ch.email)
						print(st.email,st.name,st.gender,st.scu,st.bday)
						try:
							leng=len(st.json)
						except:
							leng=0
						return render(request, 'counselling/taby.html',{'ls1dd':leng})
					except:
						return render(request, 'counselling/loggedin.html')
			else:
				#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
				if hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()!=cheese_blog.password:
					return render(request, 'counselling/dashboard.html',{'impmsg':'Wrong Password. Please enter the correct password or use Forget password to change the password. Thank You.'})
				elif cheese_blog.activated==False:
					return render(request, 'counselling/dashboard.html',{'impmsg':'Please activate your account. Link had been sent to your email. Thank You.'})	
		except Exception as e:
			#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
			print(e)
			return render(request, 'counselling/dashboard.html',{'impmsg':'Please Register yourself. This username is not yet registered. Thank You.'})
	else:
		tem=[]
		tem.append('mycomany')
		tem.append(request.POST.get('username1'))
		tem.append(request.POST.get('email1'))
		tem.append(request.POST.get('password1'))
		tem.append(request.POST.get('repassword1'))
		#print(request.POST['username1'])
		try:
			cheese_blog = RegisterLogin.objects.get(username=tem[1])
			try:
				cheese_blog1 = RegisterLogin.objects.get(email=tem[2])
				print(cheese_blog1.email)
				return render(request, 'counselling/dashboard.html',{'impmsg':'This Email is already registered. Thank You'})
			except:
				return render(request, 'counselling/dashboard.html',{'impmsg':'This Username already exist. Please Choose another Username and Register again. Thank You'})
		except Exception as e:
			print(e)
			hash_object = hashlib.md5(tem[3].encode('utf-8'))
			#print(hash_object.hexdigest())
			RegisterLogin.objects.create(username=tem[1],email=tem[2],password=hash_object.hexdigest())
			content = '<a href="http://127.0.0.1:8080/counselling/activate.html"></a>'
			sender = 'ymmud32121@gmail.com'
			receivers = tem[2]
			msg = MIMEText(u'Greetings from DataBytes Analytics Pvt. Ltd. Thank for using our Product. Please <a href="http://127.0.0.1:8080/counselling/activate.html?'+tem[1]+'">Click Here</a> to activate your account.','html')
			msg['Subject'] = 'AI Based Hiring - Account Activation Link.'
			msg['From'] = sender
			msg['To'] = receivers
			#s.sendmail(me, [you], msg.as_string())
			#print("Successfully sent email")
			#s.quit()
			#print(content)
		
			#print(tem[2],type(tem[2]))
			mail=smtplib.SMTP('smtp.gmail.com:587')
			mail.starttls()
			mail.login(sender,'dummyymmud')
			#mail.sendmail(sender, receivers, content)   
			mail.sendmail(sender, receivers, msg.as_string())
			print("Successfully sent email")      
			#print("Successfully sent email")
			mail.close()
			#print(e)
			return render(request, 'counselling/dashboard.html',{'impmsg':'Your registeration is done. Please Activate your account before logging in. Thank You.'})

@csrf_exempt
def activate(request):
	print("i am in activate view////////////////////")
	print(str(request.get_full_path).split()[-1].split("'")[1].split('?')[-1])
	try:
		cheese_blog = RegisterLogin.objects.get(username=str(request.get_full_path).split()[-1].split("'")[1].split('?')[-1])
		cheese_blog.activated = True
		cheese_blog.save()
	except:
		return render(request, 'counselling/dashboard.html',{'impmsg':'Error while activating!!!'})
	#print(request.GET)
	return render(request, 'counselling/dashboard.html',{'impmsg':'Account Activated. You can login now. Thank You'})

@csrf_exempt
def forget(request):
	#print("fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
	return render(request,'counselling/forget.html')


@csrf_exempt
def otp(request):
	username=request.POST['username2']
	email=request.POST.get('email2')
	request.session['username']=username
	request.session["email"]=email
	#print("request.session:::::::::::::",request.session['username'])
	#print(username,'SSSSSSSSSSSSSSSSSSSSS',type(username))
	
	sender = 'ymmud32121@gmail.com'
	receivers = email
	#cheese_blog = RegisterLogin.objects.get(username=username)
	#print(cheese_blog)
	now = dt.datetime.now()
	delta = dt.timedelta(seconds = 1800)
	t = now.time()
	try:
		#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		cheese_blog = RegisterLogin.objects.get(username=username)
		try:
			cheese_blog1 = UserOTP.objects.get(username=username)
			cheese_blog1.delete()
			def random_with_N_digits(n):
				range_start = 10**(n-1)
				range_end = (10**n)-1
				return randint(range_start, range_end)
			content = str(random_with_N_digits(4))
			mail=smtplib.SMTP('smtp.gmail.com:587')
			mail.starttls()
			mail.login(sender,'dummyymmud')
			mail.sendmail(sender, receivers, content)         
			#print("Successfully sent email")
			mail.close()
			UserOTP.objects.create(username=username,email=cheese_blog,otp=content,startTime=now,endTime=now + delta)
		except:
			def random_with_N_digits(n):
				range_start = 10**(n-1)
				range_end = (10**n)-1
				return randint(range_start, range_end)
			content = str(random_with_N_digits(4))
			mail=smtplib.SMTP('smtp.gmail.com:587')
			mail.starttls()
			mail.login(sender,'dummyymmud')
			mail.sendmail(sender, receivers, content)         
			#print("Successfully sent email")
			mail.close()
			UserOTP.objects.create(username=username,email=cheese_blog,otp=content,startTime=now,endTime=now + delta)
		#print(cheese_blog,";;;;;;;;;;;;;;;;;;;;;")
		return render(request, 'counselling/otp.html')
	except ObjectDoesNotExist:
		#print("hshshshshh")
		return render(request, 'counselling/forget.html',{'impmsg':'Please Register yourself. This username is not yet registered. Thank You.'})
	#print((dt.datetime.combine(dt.date(1,1,1),t) + delta).time())
	#print(datetime.datetime.time(datetime.datetime.now()),datetime.datetime.time(datetime.datetime.now())+timedelta(seconds=5))
		#UserOTP.objects.create(username=username,email=cheese_blog,otp=content,startTime=dt.datetime.time(dt.datetime.now()),endTime=(dt.datetime.combine(dt.date(1,1,1),t) + delta).time())
		#print(cheese_blog,";;;;;;;;;;;;;;;;;;;;;")
		#return render(request, 'AiHiring/index.html')
	#except:
	#	return render(request, 'signupin.html')
	#return render(request,'otp.html',{'usr':username,'em':email})


@csrf_exempt
def changePSWD(request):
	usrOTP = request.POST.get('OTP')
	now = dt.datetime.now().replace(tzinfo=None)
	delta = dt.timedelta(seconds = 10)
	t = now.time()
	username=request.session['username']
	email=request.session["email"]
	cheese_blog = UserOTP.objects.get(username=username)
	strtTM = cheese_blog.startTime.replace(tzinfo=None)
	endTM = cheese_blog.endTime.replace(tzinfo=None)
	dbOTP = cheese_blog.otp
	#print(type(usrOTP),type(dbOTP))
	#print(t,strtTM,endTM)
	#if(now.time()>strtTM.time()):
	#	print(now.time(),strtTM.time())
	#if usrOTP==dbOTP:
	#	print("bcbcbcbcb")
	#if (now>strtTM and now<endTM):
	#	print('111111fvgbhjnkm')
	if (usrOTP==dbOTP and now>strtTM and now<endTM):
		#print('222222fvgbhjnkm')
		return render(request, 'counselling/changePSWD.html',{'helo':request.session['username']})
	else:
		#print('333333fvgbhjnkm')
		if usrOTP!=dbOTP:
			return render(request,'counselling/otp.html',{'impmsg':'You have entered the wrong OTP. Please Enter the correct OTP. Thank You.'})
		elif now>endTM:
			return render(request,'counselling/otp.html',{'impmsg':'This OTP has expired. Please use the new OTP. Thank You.'})
		else:
			return render(request,'counselling/otp.html',{'impmsg':'heheheehhe'})



@csrf_exempt
def test(request):
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	#uname = request.POST.get('uname')
	#scu = request.POST.get('scu')
	#course = request.POST.get('course')
	#sem = request.POST.get('sem')
	#bday = request.POST.get('bday')
	#gender = request.POST.get('gender')
	#print(uname,scu,course,sem,bday,gender)
	#if gender=='male':
		#print('heheheh')
	#	gender=True
	#else:
	#	gender=False
	#print(request.user.email)
	#studentTable.objects.create(email=request.session['currUser'],name=uname,scu=scu,course=course,sem=sem,bday=bday,gender=gender,testGiven=False)
	#print(studentTable.objects.get(name='rohan').id)
	#print(save1Dict,type(save1Dict))
	#print(len(save1Dict))
	#if len(save1Dict)>5:
	#	print(save1Dict['1'],type(save1Dict['1']))
	try:
		sT=studentTable.objects.get(email=request.session['currUser'])
		if sT.testGiven==True:
			try:
				leng=len(st.json)
			except:
				leng=0
			return render(request,'counselling/taby.html',{'ls1dd':leng})
		else:
			save1=studentTable.objects.get(email=request.session['currUser'])
			save1Dict=save1.json
			#ans=[]
			#for _ in range(1,len(save1Dict)+1):
			#	ans.append(str(save1Dict[str(_)].upper()))
			print(save1Dict)
			#print(ans)
			try:
				leng=len(save1Dict)
			except:
				leng=0
				save1Dict={}
			print(leng)
			return render(request,'counselling/test.html',{'s1d':save1Dict,'ls1d':leng})
	except:
		save1=studentTable.objects.get(email=request.session['currUser'])
		save1Dict=save1.json
		#ans=[]
		#for _ in range(1,len(save1Dict)+1):
		#	ans.append(str(save1Dict[str(_)].upper()))
		#sprint(ans)
		print(save1Dict)
		try:
			leng=len(save1Dict)
		except:
			leng=0
			save1Dict={}
		print(leng)
		return render(request,'counselling/test.html',{'s1d':save1Dict,'ls1d':leng})


save1Dict={}


@csrf_exempt
def adminLogin(request):
	return render(request,'counselling/adminLogin.html')

@csrf_exempt
def admin(request):
	allEntry1=studentTable.objects.all()
	print(len(allEntry1))
	print(studentTable.objects.get(name=allEntry1[0]).email)
	allEmail=[]
	allName=[]
	allScu=[]
	allCourse=[]
	allSem=[]
	allBday=[]
	allGender=[]
	allTestgiven=[]
	allJson=[]
	allE=[]
	allI=[]
	allS=[]
	allN=[]
	allT=[]
	allF=[]
	allJ=[]
	allP=[]
	for _ in range(len(allEntry1)):
		allEmail.append(studentTable.objects.get(name=allEntry1[_]).email)
		allName.append(studentTable.objects.get(name=allEntry1[_]).name)
		allScu.append(studentTable.objects.get(name=allEntry1[_]).scu)
		allCourse.append(studentTable.objects.get(name=allEntry1[_]).course)
		allSem.append(studentTable.objects.get(name=allEntry1[_]).sem)
		allBday.append(studentTable.objects.get(name=allEntry1[_]).bday)
		if studentTable.objects.get(name=allEntry1[_]).gender==True:
			allGender.append('Male')
		else:
			allGender.append('Female')
		if studentTable.objects.get(name=allEntry1[_]).testGiven==True:
			allTestgiven.append('Yes')
		else:
			allTestgiven.append('No')
		allJson.append(studentTable.objects.get(name=allEntry1[_]).json)
		if studentTable.objects.get(name=allEntry1[_]).EI != None:
			allE.append(studentTable.objects.get(name=allEntry1[_]).EI.split(',')[0])
			allI.append(studentTable.objects.get(name=allEntry1[_]).EI.split(',')[1])
		else:
			allE.append('N')
			allI.append('A')
		if studentTable.objects.get(name=allEntry1[_]).SN!=None:
			allS.append(studentTable.objects.get(name=allEntry1[_]).SN.split(',')[0])
			allN.append(studentTable.objects.get(name=allEntry1[_]).SN.split(',')[1])
		else:
			allS.append('N')
			allN.append('A')
		if studentTable.objects.get(name=allEntry1[_]).TF!=None:
			allT.append(studentTable.objects.get(name=allEntry1[_]).TF.split(',')[0])
			allF.append(studentTable.objects.get(name=allEntry1[_]).TF.split(',')[1])
		else:
			allT.append('N')
			allF.append('A')
		if studentTable.objects.get(name=allEntry1[_]).JP!=None:
			allJ.append(studentTable.objects.get(name=allEntry1[_]).JP.split(',')[0])
			allP.append(studentTable.objects.get(name=allEntry1[_]).JP.split(',')[1])	
		else:
			allJ.append('N')
			allP.append('A')
	print(allEmail)
	print(allName)
	print(allScu)
	print(allCourse)
	print(allSem)
	print(allBday)
	print(allGender)
	print(allTestgiven)
	print(allJson)
	print(allE,allI)
	print(allS,allN)
	print(allT,allF)
	print(allJ,allP)

	return render(request,'counselling/admin.html',{'allE':allE,'allI':allI,'allS':allS,'allN':allN,'allT':allT,'allF':allF,'allJ':allJ,'allP':allP,'len':len(allEntry1),'allEmail':allEmail,'allName':allName,'allScu':allScu,'allCourse':allCourse,'allSem':allSem,'allBday':allBday,'allGender':allGender,'allTestgiven':allTestgiven,'allJson':allJson})


@csrf_exempt
def taby(request):
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	if request.method == 'POST' and request.POST.get('login')=='login':
		tem = request.POST.get('username')
		try:
			
			cheese_blog = RegisterLogin.objects.get(username=tem)
			
			#print(cheese_blog,";;;;;;;;;;;;;;;;;;;;;")
			#print(cheese_blog.password,request.POST.get('password'))
			#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
			if hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()==cheese_blog.password and cheese_blog.activated==True:
				if request.method=='POST' and request.POST.get('login')=='login':
					print(request.POST.get('username'),type(request.POST.get('username')))
					ch=RegisterLogin.objects.get(username=request.POST.get('username'))
					request.session['currUser'] = ch.email
					#print(user.email,request.session['currUser'])
					try:
						st=studentTable.objects.get(email=ch.email)
						print(st.email,st.name,st.gender,st.scu,st.bday)
						try:
							leng=len(st.json)
						except:
							leng=0
						return render(request, 'counselling/taby.html',{'ls1dd':leng})
					except:
						return render(request, 'counselling/loggedin.html')
			else:
				#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
				if hashlib.md5(request.POST.get('password').encode('utf-8')).hexdigest()!=cheese_blog.password:
					return render(request, 'counselling/dashboard.html',{'impmsg':'Wrong Password. Please enter the correct password or use Forget password to change the password. Thank You.'})
				elif cheese_blog.activated==False:
					return render(request, 'counselling/dashboard.html',{'impmsg':'Please activate your account. Link had been sent to your email. Thank You.'})	
		except Exception as e:
			#print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
			print(e)
			return render(request, 'counselling/dashboard.html',{'impmsg':'Please Register yourself. This username is not yet registered. Thank You.'})
	elif request.method == 'POST' and request.POST.get('register1')=='register1':
		tem=[]
		tem.append('mycomany')
		tem.append(request.POST.get('username1'))
		tem.append(request.POST.get('email1'))
		tem.append(request.POST.get('password1'))
		tem.append(request.POST.get('repassword1'))
		#print(request.POST['username1'])
		try:
			cheese_blog = RegisterLogin.objects.get(username=tem[1])
			try:
				cheese_blog1 = RegisterLogin.objects.get(email=tem[2])
				print(cheese_blog1.email)
				return render(request, 'counselling/dashboard.html',{'impmsg':'This Email is already registered. Thank You'})
			except:
				return render(request, 'counselling/dashboard.html',{'impmsg':'This Username already exist. Please Choose another Username and Register again. Thank You'})
		except Exception as e:
			print(e)
			hash_object = hashlib.md5(tem[3].encode('utf-8'))
			#print(hash_object.hexdigest())
			RegisterLogin.objects.create(username=tem[1],email=tem[2],password=hash_object.hexdigest())
			content = '<a href="http://127.0.0.1:8080/counselling/activate.html"></a>'
			sender = 'ymmud32121@gmail.com'
			receivers = tem[2]
			msg = MIMEText(u'Greetings from DataBytes Analytics Pvt. Ltd. Thank for using our Product. Please <a href="http://127.0.0.1:8080/counselling/activate.html?'+tem[1]+'">Click Here</a> to activate your account.','html')
			msg['Subject'] = 'AI Based Hiring - Account Activation Link.'
			msg['From'] = sender
			msg['To'] = receivers
			#s.sendmail(me, [you], msg.as_string())
			#print("Successfully sent email")
			#s.quit()
			#print(content)
		
			#print(tem[2],type(tem[2]))
			mail=smtplib.SMTP('smtp.gmail.com:587')
			mail.starttls()
			mail.login(sender,'dummyymmud')
			#mail.sendmail(sender, receivers, content)   
			mail.sendmail(sender, receivers, msg.as_string())
			print("Successfully sent email")      
			#print("Successfully sent email")
			mail.close()
			#print(e)
			return render(request, 'counselling/dashboard.html',{'impmsg':'Your registeration is done. Please Activate your account before logging in. Thank You.'})
	elif request.method == 'POST' and request.POST.get('update')=='update':
		#print(request.POST.get('nname'))
		change=studentTable.objects.get(email=request.session['currUser'])
		change.name=request.POST.get('nname')
		change.scu=request.POST.get('nscu')
		change.course=request.POST.get('ncourse')
		change.sem=request.POST.get('nsem')
		change.bday=request.POST.get('nbday')
		if request.POST.get('ngender')=='male':
			change.gender=True
		else:
			change.gender=False
		change.save()
		try:
			leng=len(change.json)
		except:
			leng=0
		return render(request,'counselling/taby.html',{'ls1dd':leng})
	else:
		print("requesttttttttt::::::::::::::",request.POST)
		if request.POST.get('submitTest')=='submitTest':
			print('submitTest')
			change=studentTable.objects.get(email=request.session['currUser'])
			change.testGiven=True
			change.save()
			print(request.POST.get('submitTest'))
			print(request.POST.get('EI'))
			print(request.POST.get('SN'))
			print(request.POST.get('TF'))
			print(request.POST.get('JP'))
			request.session['EI']=(request.POST.get('EI')).split(',')
			request.session['SN']=(request.POST.get('SN')).split(',')
			request.session['TF']=(request.POST.get('TF')).split(',')
			request.session['JP']=(request.POST.get('JP')).split(',')
			testReport=studentTable.objects.get(email=request.session['currUser'])
			testReport.EI=request.session['EI']
			testReport.SN=request.session['SN']
			testReport.TF=request.session['TF']
			testReport.JP=request.session['JP']
			testReport.save()
			try:
				leng=len(change.json)
			except:
				leng=0
			return render(request,'counselling/.html',{'ls1dd':leng})
		elif request.POST.get('skipTest')=='skipTest':
			change=studentTable.objects.get(email=request.session['currUser'])
			try:
				leng=len(change.json)
			except:
				leng=0
			return render(request,'counselling/taby.html',{'ls1dd':leng})
		elif request.POST.get('submit1')=='submit1':
			print("i m in taby from submit1.........")
			print(request.POST.get('ques1'))
			print(type(request.POST.get('ques1')))
			print(len(request.POST.get('ques1')))
			save1=studentTable.objects.get(email=request.session['currUser'])
			print(type(save1.json))
			try:
				lenOfjson=len(save1.json)
			except:
				lenOfjson=0

			if lenOfjson==0:
				print(request.POST.get('ques1').split(','))
				save1.json={}
				for _ in range(0,len(request.POST.get('ques1').split(','))):
					if request.POST.get('ques1').split(',')[_]=='a':
						save1.json[int(_+1)]='a'
					elif request.POST.get('ques1').split(',')[_]=='b':
						save1.json[int(_+1)]='b'
				#save1.json=save1Dict
				save1.save()
			else:
				for _ in range(0,len(request.POST.get('ques1').split(','))):
					if request.POST.get('ques1').split(',')[_]=='a':
						save1.json[int(lenOfjson+_+1)]='a'
					elif request.POST.get('ques1').split(',')[_]=='b':
						save1.json[int(lenOfjson+_+1)]='b'
				#save1.json=save1Dict
				save1.save()
			try:
				leng=len(save1.json)
			except:
				leng=0
			return render(request,'counselling/taby.html',{'ls1dd':leng})
		else:
			if request.POST.get('submit')=='submit':
				uname = request.POST.get('uname')
				scu = request.POST.get('scu')
				course = request.POST.get('course')
				sem = request.POST.get('sem')
				bday = request.POST.get('bday')
				gender = request.POST.get('gender')
				print(uname,scu,course,sem,bday,gender)
				if gender=='male':
					print('heheheh')
					gender=True
				else:
					gender=False
				#print(request.user.email)
				studentTable.objects.create(email=request.session['currUser'],name=uname,scu=scu,course=course,sem=sem,bday=bday,gender=gender,testGiven=False)
				#print(studentTable.objects.get(name='rohan').id)
				save1=studentTable.objects.get(email=request.session['currUser'])
				try:
					leng=len(save1.json)
				except:
					leng=0
				return render(request,'counselling/taby.html',{'ls1dd':leng})
			else:
				save1=studentTable.objects.get(email=request.session['currUser'])
				try:
					leng=len(save1.json)
				except:
					leng=0
				return render(request,'counselling/taby.html',{'ls1dd':leng})
				'''
	if request.POST.get('save1')=='save1':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(1,11):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
	elif request.POST.get('save2')=='save2':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(11,21):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
	elif request.POST.get('save3')=='save3':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(21,31):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
	elif request.POST.get('save4')=='save4':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(31,41):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
	elif request.POST.get('save5')=='save5':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(41,51):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
	elif request.POST.get('save6')=='save6':
		save1=studentTable.objects.get(email=request.session['currUser'])
		print(request.POST)
		for _ in range(51,61):
			if request.POST.get('q'+str(_))[0]=='a':
				save1Dict[str(_)]='a'
			else:
				save1Dict[str(_)]='b'
		save1.json=save1Dict
		save1.save()
		return render(request,'counselling/jove.html')
'''




@csrf_exempt
def manage(request):
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	try:
		change=studentTable.objects.get(email=request.session['currUser'])
		regName=change.name
		regSCU=change.scu
		regCourse=change.course
		regSem=change.sem
		regBday=change.bday
		if change.gender==True:
			regGend='Male'
		else:
			regGend='Female'
		return render(request,'counselling/manage.html',{'regName':regName,'regSCU':regSCU,'regCourse':regCourse,'regSem':regSem,'regBday':regBday,'regGend':regGend})
	except Exception as e:
		print(e)
		return render(request,'counselling/dashboard.html')



@csrf_exempt
def reports(request):
	if request.method=='POST' and request.POST.get('submit')=='submit':
		print(request.POST)
		answer = request.POST.get('ques').split(',')
		save1=studentTable.objects.get(email=request.session['currUser'])
		save1Dict=save1.json
		try:
			lenOfjson=len(save1.json)
		except:
			lenOfjson=0
		if lenOfjson==0:
			save1Dict={}
			for _ in range(0,len(request.POST.get('ques').split(','))):
				if request.POST.get('ques').split(',')[_]=='a':
					save1Dict[str(_+1)]='a'
				elif request.POST.get('ques').split(',')[_]=='b':
					save1Dict[str(_+1)]='b'
				save1.json=save1Dict
				save1.save()
		else:
			for _ in range(0,len(request.POST.get('ques').split(','))):
				if request.POST.get('ques').split(',')[_]=='a':
					save1Dict[str(lenOfjson+_+1)]='a'
				elif request.POST.get('ques').split(',')[_]=='b':
					save1Dict[str(lenOfjson+_+1)]='b'
			save1.json=save1Dict
			save1.save()


		answer=[]
		print(save1Dict)
		for _ in range(1,len(save1Dict)+1):
			answer.append(save1Dict[str(_)])
		column1=[0,7,14,21,28,35,42,49,56,63]
		column2=[1,8,15,22,29,36,43,50,57,64]
		column3=[2,9,16,23,30,37,44,51,58,65]
		column4=[3,10,17,24,31,38,45,52,59,66]
		column5=[4,11,18,25,32,39,46,53,60,67]
		column6=[5,12,19,26,33,40,47,54,61,68]
		column7=[6,13,20,27,34,41,48,55,62,69]
		#column1=[0,7]
		#column2=[1,8]
		#column3=[2,9]
		#column4=[3,10]
		#column5=[4,11]
		#column6=[5,12]
		#column7=[6,13]
		cntA=0
		cntB=0
		for _ in column1:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column2:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		extro=(cntA/20)*100
		intro=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column3:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column4:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		sens=(cntA/20)*100
		intu=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column5:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column6:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		think=(cntA/20)*100
		feel=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column7:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		judge=(cntA/10)*100
		perce=(cntB/10)*100
		save1.EI=str(extro)+','+str(intro)
		save1.SN=str(sens)+','+str(intu)
		save1.TF=str(think)+','+str(feel)
		save1.JP=str(judge)+','+str(perce)
		save1.testGiven=True
		save1.save()
		return render(request,'counselling/reports.html',{'e_ei':extro,'i_ei':intro,'s_sn':sens,'n_sn':intu,'t_tf':think,'f_tf':feel,'j_jp':judge,'p_jp':perce})
	else:
		save1=studentTable.objects.get(email=request.session['currUser'])
		save1Dict=save1.json
		answer=[]
		print(save1Dict)
		for _ in range(1,len(save1Dict)+1):
			answer.append(save1Dict[str(_)])
		print(answer,":::::::::::Answer")
		column1=[0,7,14,21,28,35,42,49,56,63]
		column2=[1,8,15,22,29,36,43,50,57,64]
		column3=[2,9,16,23,30,37,44,51,58,65]
		column4=[3,10,17,24,31,38,45,52,59,66]
		column5=[4,11,18,25,32,39,46,53,60,67]
		column6=[5,12,19,26,33,40,47,54,61,68]
		column7=[6,13,20,27,34,41,48,55,62,69]
		#column1=[0,7]
		#column2=[1,8]
		#column3=[2,9]
		#column4=[3,10]
		#column5=[4,11]
		#column6=[5,12]
		#column7=[6,13]
		cntA=0
		cntB=0
		for _ in column1:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column2:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		extro=(cntA/20)*100
		intro=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column3:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column4:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		sens=(cntA/20)*100
		intu=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column5:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		for _ in column6:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		think=(cntA/20)*100
		feel=(cntB/20)*100
		cntA=0
		cntB=0
		for _ in column7:
			if answer[_]=='a':
				cntA+=1
			else:
				cntB+=1
		judge=(cntA/10)*100
		perce=(cntB/10)*100
		save1.EI=str(extro)+','+str(intro)
		save1.SN=str(sens)+','+str(intu)
		save1.TF=str(think)+','+str(feel)
		save1.JP=str(judge)+','+str(perce)
		save1.testGiven=True
		save1.save()
		return render(request,'counselling/reports.html',{'e_ei':extro,'i_ei':intro,'s_sn':sens,'n_sn':intu,'t_tf':think,'f_tf':feel,'j_jp':judge,'p_jp':perce})

'''
@csrf_exempt
def reports(request):
	request.session.set_expiry(420)
	print(request.session.get_expiry_age())
	testReport=studentTable.objects.get(email=request.session['currUser'])
	EI=testReport.EI
	SN=testReport.SN
	TF=testReport.TF
	JP=testReport.JP
	newEI=''
	newSN=''
	newTF=''
	newJP=''
	
	for _ in EI:
		if _=='0' or _=='1' or _=='2' or _=='3' or _=='4' or _=='5' or _=='6' or _=='7' or _=='8' or _=='9' or _==',':
			newEI+=_
	for _ in SN:
		if _=='0' or _=='1' or _=='2' or _=='3' or _=='4' or _=='5' or _=='6' or _=='7' or _=='8' or _=='9' or _==',':
			newSN+=_
	for _ in TF:
		if _=='0' or _=='1' or _=='2' or _=='3' or _=='4' or _=='5' or _=='6' or _=='7' or _=='8' or _=='9' or _==',':
			newTF+=_
	for _ in JP:
		if _=='0' or _=='1' or _=='2' or _=='3' or _=='4' or _=='5' or _=='6' or _=='7' or _=='8' or _=='9' or _==',':
			newJP+=_
	EI=newEI.split(',')
	SN=newSN.split(',')
	TF=newTF.split(',')
	JP=newJP.split(',')
	extrovert=(int(EI[0])/(int(EI[0])+int(EI[1])))*100
	introvert=(int(EI[1])/(int(EI[0])+int(EI[1])))*100
	sensing=(int(SN[0])/(int(SN[0])+int(SN[1])))*100
	intuition=(int(SN[1])/(int(SN[0])+int(SN[1])))*100
	Thinking=(int(TF[0])/(int(TF[0])+int(TF[1])))*100
	Feeling=(int(TF[1])/(int(TF[0])+int(TF[1])))*100
	Judging=(int(JP[0])/(int(JP[0])+int(JP[1])))*100
	Perceiving=(int(JP[1])/(int(JP[0])+int(JP[1])))*100
	return render(request,'counselling/reports.html',{'e_ei':extrovert,'i_ei':introvert,'s_sn':sensing,'n_sn':intuition,'t_tf':Thinking,'f_tf':Feeling,'j_jp':Judging,'p_jp':Perceiving})
	'''