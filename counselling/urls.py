from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
#z
urlpatterns = [
    #url(r'^$', views.hi, name='hi'),
    url(r'^home.html$', views.home, name='home'),
    url(r'^dashboard.html$', views.dashboard, name='dashboard'),
    url(r'^loggedin.html$', login_required(views.loggedin), name='loggedin'),
    url(r'^authenticate.html$', views.auth, name='auth'),
    url(r'^activate.html?', views.activate, name='activate'),
    url(r'^forget.html$', views.forget, name='forget'),
    url(r'^otp.html$', views.otp, name='otp'),
    url(r'^changePSWD.html$', views.changePSWD, name='changePSWD'),
    url(r'^test.html$', views.test, name='test'),
    url(r'^taby.html$', views.taby, name='taby'),
    url(r'^manage.html$', views.manage, name='manage'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^page.html$', views.page, name='page'),
    url(r'^index.html$', views.index, name='index'),
    url(r'^au.html$', views.au, name='au'),
    url(r'^pf.html$', views.pf, name='pf'),
    url(r'^pp.html$', views.pp, name='pp'),
    url(r'^reports.html$', views.reports, name='reports'),
    url(r'^adminLogin.html$', views.adminLogin, name='adminLogin'),
    url(r'^frc.html$', views.frc, name='frc'),
    url(r'^view.html$', views.view, name='view'),
    url(r'^admin.html$', views.admin, name='admin'),
    url(r'^contact.html$', views.contact, name='contact'),
    url(r'^help.html$', views.help, name='help'),
    url(r'^aboutTest.html$', views.aboutTest, name='aboutTest'),
    url(r'^500.html$',views.handler500,name='handler500'),
    url(r'^400.html$',views.handler400,name='handler400'),
    url(r'^404.html$',views.handler404,name='handler404'),
    url(r'^403.html$',views.handler403,name='handler403'),

]


handler500 = 'counselling.views.handler500'
handler400 = 'counselling.views.handler400'
handler404 = 'counselling.views.handler404'
handler403 = 'counselling.views.handler403'