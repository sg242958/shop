from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import SignUp, Category, Product, Feedback, Cart, Buy
import random
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    prod_cat = set()
    prod = Product.objects.all()
    for i in prod:
        prod_cat.add(i.category)
    ccats = list()
    for i in prod_cat:
        ccats.append(Product.objects.filter(category__in=Category.objects.filter(category=i)).count())
    return render(request, 'home.html', {'products': prod, 'categories': prod_cat, 'ccats': ccats})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def admin_login(request):
    error = ""
    if request.user.is_authenticated:
        return redirect('/admin_login/admin_home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                request.session['is_logged'] = 'is_logged'
                error = "no"
            else:
                error = "yes"
        except:
                error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Logout_Admin(request):
    logout(request)
    del request.session
    return redirect('/')

def Logout_User(request):
    logout(request)
    del request.session
    return redirect('/')

def admin_user(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        user = User.objects.filter(is_staff=False)
        return render(request, 'admin_user.html', {'users': user})
    return redirect('/admin_login')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        bp = Buy.objects.filter(status__iexact='Pending').count()
        bc = Buy.objects.filter(status__iexact='Confirmed').count()
        bd = Buy.objects.filter(status__iexact='Delivered').count()
        cb = Buy.objects.filter(status__iexact='Cancelled').count()
        bo = Buy.objects.filter(status__iexact='On Way').count()
        br = Buy.objects.filter(status__iexact='Ready').count()
        up = User.objects.filter(is_staff=False).count()
        ap = Product.objects.all().count()
        ba = Buy.objects.all().count()
        context = {'bp': bp, 'bc': bc, 'bd': bd, 'ba': ba, 'cb': cb, 'bo': bo, 'br': br, 'ap': ap, 'up': up}
        return render(request, 'admin_home.html', context)
    return render(request, 'admin_login.html')

def admin_add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        if request.session.has_key('is_logged'):
            try:
                c = Category.objects.get(category__iexact=category)
                mssg = "This Category Name already exist!"
                return redirect('/admin_login/admin_add_category')
            except:
                if len(category) > 0:
                    cats = Category(category=category)
                    cats.save()
                    return redirect('/admin_login/admin_add_category', message="Successfully saved!")
    return render(request, 'admin_category_form.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/user/user_home')
    error = ""
    if request.method == 'POST':
        us = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=us, password=password)
        try:
            if user:
                request.session["data"] = "data"
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_login.html', d)

def signup(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        try:
            userna = User.objects.filter(username__iexact=username)
            sign = SignUp.objects.filter(user__iexact=userna)
            return redirect('/signup')
        except:
            first = request.POST['first']
            last = request.POST['last']
            contact = request.POST['contact']
            email = request.POST['email']
            password = request.POST['password']
            mpassword = make_password(password, None)
            try:
                user = User.objects.create(username=username, password=mpassword, email=email, first_name=first, last_name=last)
                data = SignUp(user=user, contact=contact)
                data.save()
                error = "no"
            except:
                error = "yes"
    d = {"error": error}
    return render(request, 'signup.html', d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        user = User.objects.get(id=request.user.id)
        data = SignUp.objects.get(user=user)
        return render(request, 'profile.html', {'data': data, 'user': user})
    return redirect('/user')

def change_password(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        if request.method == 'POST':
            old = request.POST['old']
            new = request.POST['new']
            confirm = request.POST['confirm']
            if new == confirm:
                u = User.objects.get(username__iexact=request.user.username)
                u.set_password(new)
                u.save()
                error = "no"
            else:
                error = "yes"
        cart = Cart.objects.filter(user=request.user).count()
        d = {"error": error, 'cart': cart}
        return render(request, 'change_password.html', d)
    return redirect('/user')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        user = User.objects.get(id=request.user.id)
        data = SignUp.objects.get(user=user)
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'profile.html', {'data': data, 'user': user, 'cart': cart})
    return redirect('/user')

def edit(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        if request.method == 'POST':
            user = User.objects.get(username__iexact=request.user.username)
            detail = SignUp.objects.get(user=user)
            user.username = request.POST['user']
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            detail.contact = request.POST.get('contact')
            user.save()
            detail.save()
            message = "Successful Updated Profile"
        user = User.objects.get(id=request.user.id)
        data = SignUp.objects.get(user=user)
        return redirect('/user/profile', {'message': message})
    return redirect('/user')

def view_category(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        cats = Category.objects.all()
        return render(request, 'view_category.html', {'cats': cats})
    return redirect('/admin_login')

def category_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        cat = Category.objects.get(pk=id)
        cat.delete()
        return redirect('/admin_login/view_category')
    return redirect('/admin_login')

def add_product(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            ca = request.POST['category']
            category = Category.objects.get(id=request.POST['category'])
            product = request.POST['product']
            price = request.POST['price']
            description = request.POST['description']
            image = request.FILES['image']
            prod = Product(category=category, product_name=product, price=price, Description=description, image=image)
            prod.save()
            return redirect('/admin_login/admin_home')
        cats = Category.objects.all()
        return render(request, 'add_product.html', {'cats': cats})
    return redirect('/admin_login')

def view_product(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        prod = Product.objects.all()
        return render(request, 'view_product.html', {'products': prod})
    return redirect('/admin_login')

def product_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        prod = Product.objects.get(pk=id)
        prod.delete()
        return redirect('/admin_login/view_product')
    return redirect('/admin_login')

def user_view_product(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        if request.method == 'POST':
            data = request.POST['data']
            li = Category.objects.filter(category=data)
            search = Product.objects.filter(Q(product_name__icontains=data) | Q(Description__icontains=data) | Q(category__in=li))
            cart = Cart.objects.filter(user=request.user).count()
            return render(request, 'user_view_product.html', {'search': search, 'cart': cart})
        prod = Product.objects.all()
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'user_view_product.html', {'products': prod, 'cart': cart})
    return redirect('/user')

def user_homes(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        prod_cat = set()
        prod = Product.objects.all()
        for i in prod:
            prod_cat.add(i.category)
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'user_home.html', {'products': prod, 'categories': prod_cat, 'cart': cart})
    return redirect('/user')

def send_feedback(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        user = request.user.username
        datas = Feedback.objects.filter(user=request.user.username)
        if request.method == 'POST':
            feedback = request.POST['feedback']
            datetimefield = datetime.now()
            feed = Feedback(user=user, feedback=feedback, datetimefield=datetimefield)
            feed.save()
            datas = Feedback.objects.filter(user=request.user.username)
            return redirect('/user/send_feedback', {'user': user, 'feedback': feedback, 'datas': datas})
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'feedback.html', {'datas': datas, 'cart': cart})
    return redirect('/user')

def view_feedback(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        feeds = Feedback.objects.all()
        return render(request, 'view_feedback.html', {'feedbacks': feeds})
    return redirect('/admin_login')

def feedback_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        prod = Feedback.objects.get(pk=id)
        prod.delete()
        return redirect('/admin_login/view_feedback')
    return redirect('/admin_login')

def product_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        prod = Product.objects.get(pk=id)
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'product_detail.html', {'product': prod, 'cart': cart})
    return redirect('/user')

def add_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        prod = Product.objects.get(pk=id)
        d = Product.objects.get(id=prod.id)
        user = request.user.username
        cart = Cart(user=user, product=d)
        cart.save()
        return redirect('/user/user_home')
    return redirect('/user')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        carts = Cart.objects.filter(user=request.user)
        rupees = 0
        for i in carts:
            rupees = rupees + i.product.price
        lcount = Cart.objects.filter(user=request.user).count()
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'cart.html', {'carts': carts, 'lcount': lcount, 'rupees': rupees, 'cart': cart,})
    return redirect('/user')

def cart_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        cart = Cart.objects.get(pk=id)
        cart.delete()
        return redirect('/user/cart')
    return redirect('/user')

def buy_one(request, id):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        product = Product.objects.get(pk=id)
        status = 'Pending'
        payment = 'Cash On Delivery (COD)'
        user = request.user
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST.get('mobile', False)
            address = request.POST['address']
            datetimefield = datetime.now()
            order_no = str(random.randint(0000000000, 9999999999))
            buy = Buy(prod=product, order_no=order_no, address=address, user=user, status=status, payment=payment, name=name, email=email, datetimefield=datetimefield, mobile=mobile)
            buy.save()
            try:
                carts = Cart.objects.get(product=id)
                carts.delete()
            except:
                cart = Cart.objects.filter(user=request.user).count()
                return redirect('/user/user_home', {'cart': cart})
            cart = Cart.objects.filter(user=request.user).count()
            return redirect('/user/user_home', {'cart': cart})
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'buy_one.html', {'product': product, 'cart': cart})
    return redirect('/user')

def user_view_order(request):
    if not request.user.is_authenticated:
        return redirect('/user')
    if request.session.has_key('data'):
        if request.method == 'POST':
            data = request.POST['data']
            search = Buy.objects.filter(Q(status=data) | Q(order_no=data))
            csearch = Buy.objects.filter(Q(status=data) | Q(order_no=data)).count()
            return render(request, 'user_order_view.html', {'search': search, 'csearch': csearch})
        orders = Buy.objects.filter(user=request.user)
        ocount = Buy.objects.filter(user=request.user).count()
        cart = Cart.objects.filter(user=request.user).count()
        return render(request, 'user_order_view.html', {'orders': orders, 'cart': cart, 'ocount': ocount})
    return redirect('/user')

def admin_view_order(request):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            data = request.POST['data']
            search = Buy.objects.filter(Q(status__icontains=data) | Q(order_no=data))
            return render(request, 'admin_view_order.html', {'search': search})
        orders = Buy.objects.all()
        ocount = Buy.objects.all().count()
        return render(request, 'admin_view_order.html', {'orders': orders, 'ocount': ocount})
    return redirect('/admin_login')

def admin_view_order1(request, id):
    if not request.user.is_authenticated:
        return redirect('/admin_login')
    if request.session.has_key('is_logged'):
        pro = Buy.objects.get(pk=id)
        if request.method == 'POST':
            data = request.POST['status']
            pro.status = data
            pro.save()
        return redirect('/admin_login/admin_view_order')
    return redirect('/admin_login')
