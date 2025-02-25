from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models.product import Product
from .models.customer import Customer
from .models.category import Category
from django.http import JsonResponse
from .models.cart import Cart
from django.contrib import messages
from django.views import View
from django.db.models import   Q
from .models.order import OrderDetail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
def profile(request):
    try:
        # Check if the customer is logged in (session has 'phone')
        if 'phone' not in request.session:
            messages.error(request, "You must be logged in to view your profile.")
            return redirect('login')

        # Fetch customer using the phone stored in the session
        phone = request.session['phone']
        customer = Customer.objects.get(phone=phone)
        print(f"Customer Found: {customer}")  # ✅ Debugging

        # Fetch profile using the correct customer reference
        user_profile = Profile.objects.get(name=customer)
        print(f"Profile Found: {user_profile}")  # ✅ Debugging

        return render(request, 'limma/profile.html', {'profile': user_profile})

    except Customer.DoesNotExist:
        messages.error(request, "Customer record not found.")
        return redirect('signup')

    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('signup')


def home(request):
    products = None
    totalitem = 0

    # Check if the session has the 'phone' key
    if request.session.has_key('phone'):
        phone = request.session['phone']
        category = Category.get_allcategories()
        customer = Customer.objects.filter(phone=phone)

        # Get total items in the cart for the user
        totalitem = len(Cart.objects.filter(phone=phone))

        # Check if customer exists
        if customer.exists():
            for c in customer:
                name = c.name
                categoryId = request.GET.get('category')

                # Filter products based on category
                if categoryId:
                    products = Product.get_all_product_by_category(categoryId)
                else:
                    products = Product.get_all_product()

                # Prepare the data dictionary
                data = {
                    'name': name,
                    'products': products,
                    'category': category,
                    'totalitem': totalitem,
                }

                # Render the home template
                return render(request, 'limma/home.html', data)

    # If the user is not logged in, redirect to login
    return redirect('login')


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Profile, Customer  # Import the Customer model

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .models import Customer, Profile

# Signup view
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Customer, Profile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .models import Customer, Profile

class Signup(View):
    def get(self, request):
        return render(request, 'limma/signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get("username")
        password = postData.get("password")
        first_name = postData.get("first_name")
        last_name = postData.get("last_name")
        mobile = postData.get("mobile")
        address = postData.get("address")
        pincode = postData.get("pincode")
        city = postData.get("city")
        state = postData.get("state")

        error_message = None
        value = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'phone': mobile,
            'address': address,
            'pincode': pincode,
            'city': city,
            'state': state
        }

        # Validate input
        if not username:
            error_message = "Username is required."
        elif not password:
            error_message = "Password is required."
        elif not first_name:
            error_message = "First name is required."
        elif not last_name:
            error_message = "Last name is required."
        elif not mobile:
            error_message = "Mobile number is required."
        elif len(mobile) != 10:  # Ensure the mobile number is exactly 10 digits
            error_message = "Mobile number must be 10 digits long."
        elif User.objects.filter(username=username).exists():  # Check if username already exists
            error_message = "Username is already taken."
        elif Customer.objects.filter(phone=mobile).exists():
            error_message = "Customer is already registered with this number."

        if not error_message:
            # Create user
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Create customer
            customer = Customer(name=user, phone=mobile)
            customer.save()

            # Create profile
            profile = Profile(name=customer, first_name=first_name, last_name=last_name, address=address, pincode=pincode, city=city, state=state, phone_number=mobile, email=username)
            profile.save()

            messages.success(request, 'Congratulations! Registration successful.')
            return redirect('login')  # Redirect to login or another page
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'limma/signup.html', data)

class Login(View):
    def get(self, request):
        return render(request, 'limma/login.html')

    def post(self, request):
        phone = request.POST.get('phone')
        error_message = None

        # Check if the customer exists
        customer = Customer.objects.filter(phone=phone).first()  # Use first() to get a single object or None

        if customer:  # If customer exists
            request.session['phone'] = phone  # Store phone in session
            return redirect('homepage')  # Redirect to the homepage if login is successful
        else:
            error_message = "Mobile number is invalid"  # Set error message if customer does not exist

        return render(request, 'limma/login.html', {'error': error_message})
def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    item_already_in_cart=False
    if request.session.has_key('phone'):
        phone=request.session['phone']
        totalitem=len(Cart.objects.filter(phone=phone))
        item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer=Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name

        data={
            'product':product,
            'item_already_in_cart':item_already_in_cart,
            'name':name,
            'totalitem': totalitem
        }
    return render(request,'limma/productdetail.html',data)
def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')
    else:
        return redirect('login')
def add_to_cart(request):
    phone = request.session.get('phone', None)
    if not phone:
        return redirect('login')  # Redirect to login if phone is not in session

    product_id = request.GET.get('prod_id')
    try:
        product = Product.objects.get(id=product_id)  # Get the product by ID

        # Create and save Cart object
        cart_item = Cart(
            phone=phone,
            product=product,
            image=product.image,  # Use the product's image directly
            price=product.price
        )
        cart_item.save()

        return redirect(f"/product-detail/{product_id}")  # Redirect to product detail page
    except Product.DoesNotExist:
        return redirect('homepage')  # If product doesn't exist, redirect to homepage

def show_cart(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone=request.session['phone']
        totalitem=len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
            cart = Cart.objects.filter(phone=phone)
            data={
                'name':name,
                'totalitem':totalitem,
                'cart':cart
            }
            if cart:
                return render(request,'limma/show_cart.html',data)
            else:
                return render(request,'limma/empty_cart.html')

def plus_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.quantity+=1
        cart.save()
        data={
                'quantity':cart.quantity
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.quantity-=1
        cart.save()
        data={
                'quantity':cart.quantity
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.session.has_key('phone'):
        phone=request.session['phone']
        product_id=request.GET['prod_id']
        cart=Cart.objects.get(Q(product_id=product_id)& Q(phone=phone))
        cart.delete()
        return JsonResponse()
def checkout(request):
    if request.session.has_key('phone'):
        # Correctly fetch session data
        phone = request.session.get('phone')

        # Fetch data from the POST request
        name = request.POST.get('name')  # Correct key for 'name'
        address = request.POST.get('address')  # Correct key for 'address'
        mobile = request.POST.get('mobile')  # Correct key for 'mobile'

        # Fetch all cart products for the user
        cart_products = Cart.objects.filter(phone=phone)

        # If the cart is empty, handle gracefully
        if not cart_products.exists():
            return render(request, 'limma/empty_cart.html', {'name': 'Guest', 'totalitem': 0})

        # Create orders for each product in the cart
        for c in cart_products:
            OrderDetail.objects.create(
                user=phone,
                product_name=c.product,
                image=c.image,
                qty=c.quantity,
                price=c.price
            )

        # Clear the cart after saving orders
        cart_products.delete()

        # Fetch total items in the cart and customer name
        totalitem = 0  # Cart is empty now
        customer = Customer.objects.filter(phone=phone).first()
        customer_name = customer.name if customer else "Guest"

        # Prepare data for rendering
        data = {
            'name': customer_name,
            'totalitem': totalitem
        }

        # Render the empty cart page
        return render(request, 'limma/empty_cart.html', data)
    else:
        # Redirect to login if the session is not set
        return redirect('login')
def order(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone=request.session["phone"]
        totalitem=len(Cart.objects.filter(phone=phone))
        customer=Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
            order = OrderDetail.objects.filter(user=phone)
            data = {
                'order': order,
                'name':name,

                'totalitem':totalitem
            }
            if order:
                return render(request,'limma/order.html',data)
            else:
                return render(request,'limma/emptyorder.html',data)
    else:
        return redirect('login')

def search(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query=request.GET.get('query')
        search=Product.objects.filter(name__contains=query)
        category=Category.get_allcategories()
        totalitem = len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
        data={
            'name':name,
            'totalitem':totalitem,
            'search':search,
            'category':category,
            'query':query}
        return render(request,'limma/search.html',data)
    else:
        return redirect('login')
