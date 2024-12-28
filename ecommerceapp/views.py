from django.shortcuts import render, redirect
from ecommerceapp.models import Contact, Product, OrderUpdate, Orders
from django.contrib import messages
from math import ceil
from django.http import HttpResponse
from django.contrib.auth.models import User  # Import User model
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "index.html", params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "We will get back to you soon..")
        return render(request, "contact.html")

    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Create the order object and save it to generate the order_id
        order = Orders(
            user=request.user,  # Associate the order with the logged-in user
            items_json=items_json, name=name, amount=amount, email=email,
            address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone
        )
        order.save()

        # Now we can safely access the order_id
        order_id = order.order_id

        # Create the order update with the correct order_id
        update = OrderUpdate(order_id=order_id, update_desc="The order has been placed")
        update.save()

        thank = True
        return render(request, 'checkout.html', {'thank': thank})

    return render(request, 'checkout.html')


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    currentuser = request.user.username
    items = Orders.objects.filter(user=request.user)  # Get orders for the logged-in user

    orders_with_status = []
    for order in items:
        try:
            updates = OrderUpdate.objects.filter(order_id=order.order_id)
            orders_with_status.append({
                "order": order,
                "updates": updates
            })
        except ValueError:
            messages.error(request, f"Invalid order ID for order: {order.order_id}")
            continue

    context = {"orders_with_status": orders_with_status}
    return render(request, "profile.html", context)

@csrf_exempt
def handlerequest(request):
    return HttpResponse("This is the Handle Request view.")
