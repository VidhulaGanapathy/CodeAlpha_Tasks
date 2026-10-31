from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm     # ready-made signup form
from django.contrib.auth import login                      # function to log a user in
from django.contrib.auth.decorators import login_required  # protects a page: only logged-in users
from .models import Product, Order, OrderItem


# ---------- PRODUCT PAGES ----------

def landing(request):
    if request.user.is_authenticated:      # is this visitor already logged in?
        return redirect('home')            # yes → skip the entrance, go straight to the shop
    return render(request, 'store/landing.html')   # no → show the welcome page


@login_required
def home(request):                                   # every view receives 'request' (info about the visitor's request)
    products = Product.objects.all()                 # get ALL rows from the Product table
    return render(request, 'store/home.html', {'products': products})
    # render = fill the template with data. {'products': products} sends data to the template under the name 'products'

@login_required
def product_detail(request, product_id):             # product_id comes from the URL (e.g. /product/3/)
    product = get_object_or_404(Product, id=product_id)   # get product with that id, or show a 404 error page
    return render(request, 'store/product_detail.html', {'product': product})


# ---------- CART (stored in the session) ----------
# A session is a small notebook Django keeps for each visitor. Our cart looks like:
# {'3': 2, '5': 1}  means  product 3 → quantity 2,  product 5 → quantity 1
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})           # read the cart from the session; if none exists, use an empty {}
    key = str(product_id)                            # session keys must be text, so convert the number to a string
    cart[key] = cart.get(key, 0) + 1                 # current quantity (0 if new) + 1
    request.session['cart'] = cart                   # save the cart back into the session
    return redirect('cart')                          # send the user to the cart page

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)                  # remove that product (None = don't crash if it's not there)
    request.session['cart'] = cart
    return redirect('cart')


def get_cart_items(request):                         # helper function used by both cart and checkout
    cart = request.session.get('cart', {})
    items = []                                       # list that will hold each cart line
    total = 0                                        # running total of the bill
    for product_id, quantity in cart.items():        # loop through each (id, quantity) pair
        product = Product.objects.get(id=product_id)         # fetch the product from the database
        subtotal = product.price * quantity                  # price x quantity for this line
        total += subtotal                                    # add to the bill total
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return items, total                              # give back both the list and the total

@login_required
def cart(request):
    items, total = get_cart_items(request)           # call the helper
    return render(request, 'store/cart.html', {'items': items, 'total': total})


# ---------- ORDER PROCESSING ----------

@login_required                                      # if not logged in → redirected to the login page
def checkout(request):
    items, total = get_cart_items(request)
    if not items:                                    # empty cart? nothing to buy
        return redirect('home')

    if request.method == 'POST':                     # POST = the user submitted the form
        address = request.POST['address']            # read the 'address' field from the form
        order = Order.objects.create(user=request.user, address=address, total=total)
        # request.user = the currently logged-in user. .create() adds a new row to the database.
        for item in items:                           # save each cart line as an OrderItem
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
            )
        request.session['cart'] = {}                 # empty the cart after ordering
        return redirect('my_orders')

    return render(request, 'store/checkout.html', {'items': items, 'total': total})
    # if it's a GET request (just opening the page), show the checkout form


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # filter = only this user's orders; '-created_at' = newest first
    return render(request, 'store/my_orders.html', {'orders': orders})


# ---------- USER REGISTRATION ----------

def register(request):
    if request.method == 'POST':                     # form was submitted
        form = UserCreationForm(request.POST)        # fill the form with submitted data
        if form.is_valid():                          # checks username is unique, passwords match, password is strong...
            user = form.save()                       # creates the user in the database (password is hashed automatically)
            login(request, user)                     # log them in right away
            return redirect('home')
    else:
        form = UserCreationForm()                    # GET request → show an empty form
    return render(request, 'store/register.html', {'form': form})

@login_required
def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})        # read the cart from the session
    key = str(product_id)                         # session keys are text
    if key in cart:                               # only act if the product is in the cart
        cart[key] -= 1                            # reduce quantity by 1
        if cart[key] <= 0:                        # if it reached 0...
            del cart[key]                         # ...remove the product completely
    request.session['cart'] = cart                # save the cart back
    return redirect('cart')                       # return to the cart page


