
from django.contrib import admin
from django.conf.urls import include,url


from django.conf import settings
from django.conf.urls.static import static
#app_name='AiHiring'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/',include(('payment.urls','payment'),namespace='payment')),
    url(r'^counselling/', include('counselling.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    #url(r'^500.html/',include('counselling.urls')),
    #url(r'^400.html/',include('counselling.urls')),
    #url(r'^404.html/',include('counselling.urls')),
    #url(r'^403.html/',include('counselling.urls')),


]


handler500 = 'counselling.views.handler500'
handler400 = 'counselling.views.handler400'
handler404 = 'counselling.views.handler404'
handler403 = 'counselling.views.handler403'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)