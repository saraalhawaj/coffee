from django.shortcuts import render, redirect

from .forms import UserSignup, UserLogin, CoffeeForm

from django.contrib.auth import authenticate, login, logout

from decimal import Decimal

from django.http import JsonResponse
from .models import Bean, Roast, Syrup, Powder
import json


def usersignup(request):
	context = {}
	form = UserSignup()
	context['form'] = form

	if request.method=='POST':
		form = UserSignup(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password


			user.set_password(password)
			user.save()


			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("/")
		
		return redirect("mycoffee:signup")
	return render(request, 'signup.html', context)


def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == 'POST':
		form = UserLogin(request.POST)
		if form.is_valid():


			username = form.cleaned_data['username']
			password = form.cleaned_data['password']


			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('/')
			return redirect("mycoffee:login")
		return render(request, 'login.html', context)

def userlogout(request):
	logout(request)
	return redirect("/")



#x=price
def coffee_price(x):
	total_price = x.bean.price + x.roast.price + (x.espresso_shots.Decimal(0.250))
	if x.steamed_milk:
		total_price += Decimal(0.100)

	if x.powder.all().count()>0:
		for powder in x.powder.all():
			total_price += powder.x

	if x.syrup in x.all().count()>0:
		for syrup in x.syrup.all():
			total_price+= syrup.x
	return total_price



def create_coffee(request):
	context = {}
	if not request.is_authenticated():
		return redirect("mycoffee:login")
	form = CoffeeForm()
	if request.method == "POST":
		form = CoffeeForm(request.POST)
		if form.is_valid:
			coffee = form.save(commit=False)
			coffee.user = requset.user
			coffee.save()
			form.save_m2m()
			coffee.price = coffee_price(coffee)
			coffee.save()
			return redirect('/')
	context['form'] = form

	return (request, 'create_coffee.html', context)




#def get_price(request):
	#total_price = Decimal(0)

	#bean_id = request.GET.get("bean")



	#return JsonResponse(round(, safe=False))


def ajax_price(request):
    total_price = Decimal(0)

    bean_id = request.GET.get('bean')
    if bean_id:
        total_price += Bean.objects.get(id=bean_id).price

    roast_id = request.GET.get('roast')
    if roast_id:
        total_price += Roast.objects.get(id=roast_id).price

    syrups = json.loads(request.GET.get('syrups'))
    if len(syrups)>0:
        for syrup_id in syrups:
            total_price += Syrup.objects.get(id=syrup_id).price

    powders = json.loads(request.GET.get('powders'))
    if len(powders)>0:
        for powder_id in powders:
            total_price += Powder.objects.get(id=powder_id).price

    milk = request.GET.get('milk')
    if milk=='true':
        total_price += Decimal(0.100)

    shots=request.GET.get('espresso_shots')
    if shots:
        total_price += (int(shots)*Decimal(0.250))

    return JsonResponse(round(total_price,3), safe=False)