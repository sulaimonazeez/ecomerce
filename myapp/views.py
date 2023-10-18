from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .models import Category, Products, UserProfile, Cart, CartItem, Order, Payment

def home(request):
  
    gadget = Products.objects.filter(category__name="Gadget")[0]
    jel = Products.objects.filter(category__name="JEWELERY")[0]
    elec = Products.objects.filter(category__name="Electronic")[0]
    products = Products.objects.all().order_by("-category")[0:20]
    length = CartItem.objects.all()
    return render(request, 'home.html', {'data': products, "length":len(length), "products":products, "gadget":gadget, "jewelery":jel,"eletronic":elec})


def categoryed(request, id):
    if id == 1:
        caption = "Wireless"
        x = Products.objects.filter(category__name="Wireless")
        length = CartItem.objects.all()
        return render(request, "category.html", {"products": x, "length":len(length), "caption":caption})
    elif id == 2:
        caption = "Electronic"
        x = Products.objects.filter(category__name="Electronic")
        length = CartItem.objects.all()
        return render(request, "category.html", {"products": x, "length":len(length), "caption":caption})
    elif id == 3:
        x = Products.objects.filter(category__name="Watch")
        length = CartItem.objects.all()
        return render(request, "category.html", {"products": x, "length":len(length), "caption":"Watch"})
    else:
        return redirect("/category/2")

  
  
  
def increase(request, id):
  indx = CartItem.objects.get(id=id)
  indx.quantity +=1
  indx.save()
  return redirect("cart")

def descrease(request, id):
  indx = CartItem.objects.get(id=id)
  if (indx.quantity > 1):
    indx.quantity -=1
    indx.save()
  return redirect("cart")
def cart_item(request,id):
    product = Products.objects.get(id=id)
    length = CartItem.objects.all()
    return render(request, 'cart.html', {'item': product, "length":len(length)})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use get() to avoid KeyError
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Your successfully login")
            return redirect("/")  # Fixed: Use return to redirect

        else:
            # Handle authentication failure, e.g., display an error message
            messages.error(request, 'Invalid password or username!')
            return redirect("/account/login")  # Fixed: Use return to redirect

    else:
        if request.user.is_authenticated:
            return render(request, "profile.html")
        else:
            return render(request, 'login.html')
@login_required
def add_to_cart(request, id):
  if not request.user.is_authenticated:
        return redirect(reverse('login'))
  else:
    product = Products.objects.get(id=id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, 'Product added to cart successfully!')
    return redirect('/')

@login_required
def cart(request):
  if not request.user.is_authenticated:
        return redirect(reverse('login'))
  else:
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    length = CartItem.objects.all()
    return render(request, 'cart_data.html', {'cart': cart, 'cart_items': cart_items,"length":len(length)})

@login_required
def remove_from_cart(request, id):
  if not request.user.is_authenticated:
        return redirect(reverse('login'))
  else:
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    messages.success(request, 'Product removed from cart successfully!')
    return redirect('cart')

@login_required 
def create_order(request):
  if not request.user.is_authenticated:
    return redirect(reverse('login'))
  else:
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if cart_items:
        total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        order = Order.objects.create(user=user, total_price=total_price)
        for cart_item in cart_items:
            order.items.add(cart_item)
        cart_items.delete()
        payments = Payment.objects.create(order=order, payment_method='Credit Card')  # You can customize this part for payment handling
        payments.save()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail/{id}'.format(id=order.id))
    else:
        messages.error(request, 'Your cart is empty. Add items to your cart first!')
        return redirect('cart')

@login_required
def order_detail(request, id):
    length = CartItem.objects.all()
    order = Order.objects.get(id=id)
    return render(request, 'order_detail.html', {'order': order,"length":len(length)})