from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
#from orders.models import Order
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_done(request):
	return render(request,'payment/done.html')


@csrf_exempt
def payment_cancelled(request):
	return render(request,'payment/cancelled.html')



def payment_process(request):
	host = request.get_host()
	paypal_dict = {
	'business': settings.PAYPAL_RECEIVER_EMAIL ,
	'amount': '100',
	'item_name': 'Item_Name_xyz',
	'invoice': ' Test Payment Invoice',
	'currency_code': 'USD',
	'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
	'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
	'cancel_return': 'http://{}{}'.format(host, reverse('payment:cancelled')),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html', {'form': form })