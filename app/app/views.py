from django.shortcuts import render
import app.forms as forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import  render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from app.models import Cart, Item, Product, Order, Address, Stock

def new_user(request):
    if(request.method == 'GET'):
        form = forms.RegisterForm()
        return render(request, 'register.html',{'form' : form} )
    
    elif(request.method == 'POST'):
        form = forms.RegisterForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            cart = Cart(itemsNumber=0, user=user)
            cart.save()
        else:
            return redirect('/registro')
        return redirect('/login/')
    
def do_login(request):
    if(request.method == 'GET'):
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})
    
    elif(request.method == 'POST'):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if(user.is_staff):
                    return redirect('/admin')
                else:
                    return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'erro': 'Usuário ou senha inválidos'})
        else:
            return render(request, 'login.html', {'form': form, 'erro': 'Preencha os dados corretamente'})
        
def new_staff():
    if(request.method == 'GET'):
        form = forms.StaffRegisterForm()
        return render(request, 'staffRegister.html', {'form' : form})

def home(request):
    user = request.user
    products = Product.objects.all()
    return render(request, 'home.html', {'user':user, 'products': products})
        
@login_required(login_url='/login')
def do_logout(request):
    logout(request)
    return redirect('/login')
    
@login_required(login_url='/login')
def cart(request):
    user = request.user
    cart = Cart.objects.get(user = user)
    items = Item.objects.filter(cart = cart)
    totalValue = 0
    for item in items:
        totalValue += item.quantity * item.product.price
    return render(request, 'cart.html', {'items':items, 'cart':cart, 'totalValue': totalValue})

@login_required(login_url="/login")
def add_to_cart(request):
    # pega o user pelo request
    user = request.user
    # consulta o cart pelo bd
    cart = Cart.objects.get(user = user)
    # pega o id do product
    product_id = request.POST.get('product_id')

    quantity = request.POST.get('quantity')
    # consulta o product
    product = Product.objects.get(id=product_id)
    # cria o item
    item = Item.objects.create(cart=cart, product=product, quantity=quantity)
    item.save()
    #print(product.name)
    return redirect('/carrinho')

@login_required(login_url="/login")
def remove_item(request):
    user = request.user
    item_id = request.POST.get('item_id')
    Item.objects.get(id=item_id).delete()
    return redirect('/carrinho')

@login_required(login_url="/login")
def new_order(request):
    if request.GET:
        return redirect('/')

    if request.POST:
        user = request.user
        cart = Cart.objects.get(user = user)
        items = Item.objects.filter(cart = cart)
        totalValue = 0
        for item in items:
            totalValue += item.product.price * item.quantity

        order = Order.objects.create(user = user, status='Pendente', totalValue=totalValue)

        for item in items:
            item.order = order
            item.cart = None
            item.save()

        order_items = Item.objects.filter(order = order)

        return render(request, 'new_order.html', {'order': order, 'items': order_items})


@login_required(login_url="/login")
def checkout(request):
    method = request.POST.get('method')
    postal_code = request.POST.get('postal_code')
    number = request.POST.get('number')
    complement = request.POST.get('complement')
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id = order_id)
    order.status = 'Paga'
    address = Address.objects.create(postal_code = postal_code, complement = complement, number = number, order = order)
    order.save()
    items = Item.objects.filter(order = order)
    for item in items:
        product = item.product
        stock = Stock.objects.get(product = product)
        new_quantity = stock.quantity - item.quantity
        stock.quantity = new_quantity
        stock.save()

    return redirect('/sucesso')
    
def success(request):
    return render(request, 'success.html')

def product(request, slug):
    product = Product.objects.get(id = slug)
    return render(request, 'product.html', {'product': product})


def orders(request):
    user = request.user
    orders = Order.objects.filter(user = user)
    return render(request, 'orders.html', {'orders': orders})