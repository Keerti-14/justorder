from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import Order
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))  # Redirect to the homepage
        else:
            return render(request, "login.html", {
                "error_message": "Invalid username or password."
            })
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return HttpResponseRedirect(reverse("login"))
            except:
                return render(request, "signup.html", {
                    "error_message": "Username already exists."
                })
        else:
            return render(request, "signup.html", {
                "error_message": "Passwords do not match."
            })
    return render(request, "signup.html")

def forgot_password_view(request):
    if request.method == "POST":
        # Add logic to handle password reset (e.g., send email)
        return render(request, "forgot_password.html", {
            "success_message": "Password reset instructions have been sent to your email."
        })
    return render(request, "forgot_password.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def update_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            return redirect("index")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "update_password.html", {"form": form})

def category_items(request, category_name):
    # Define items for each category
    items = []
    if category_name == "vegetables":
        items = [
            {"name": "Tomato", "price": 2, "description": "Fresh red tomatoes."},
            {"name": "Onion", "price": 1.5, "description": "Crisp and flavorful onions."},
            {"name": "Potato", "price": 1, "description": "Versatile and starchy potatoes."},
            {"name": "Eggplant", "price": 2.5, "description": "Fresh and tender eggplants."},
            {"name": "Bottle Gourd", "price": 3, "description": "Nutritious bottle gourds."},
            {"name": "Cucumber", "price": 1.8, "description": "Cool and refreshing cucumbers."},
            {"name": "Carrot", "price": 2, "description": "Crunchy and sweet carrots."},
            {"name": "Mushroom", "price": 4, "description": "Fresh and organic mushrooms."},
            {"name": "Spinach", "price": 1.2, "description": "Healthy and green spinach."},
        ]
    elif category_name == "fruits":
        items = [
            {"name": "Apple", "price": 3, "description": "Crisp and juicy apples."},
            {"name": "Banana", "price": 1, "description": "Sweet and ripe bananas."},
            {"name": "Orange", "price": 2, "description": "Fresh and tangy oranges."},
            {"name": "Grapes", "price": 4, "description": "Sweet and juicy grapes."},
            {"name": "Mango", "price": 5, "description": "Delicious and ripe mangoes."},
            {"name": "Pineapple", "price": 3.5, "description": "Tropical and sweet pineapples."},
            {"name": "Strawberry", "price": 6, "description": "Fresh and sweet strawberries."},
            {"name": "Watermelon", "price": 2.5, "description": "Refreshing watermelon slices."},
        ]
    elif category_name == "dairy":
        items = [
            {"name": "Milk", "price": 1.5, "description": "Fresh and creamy milk."},
            {"name": "Cheese", "price": 4, "description": "Rich and flavorful cheese."},
            {"name": "Yogurt", "price": 2, "description": "Creamy and tangy yogurt."},
            {"name": "Butter", "price": 3, "description": "Rich and creamy butter."},
            {"name": "Paneer", "price": 5, "description": "Fresh and soft paneer."},
        ]
    elif category_name == "oils":
        items = [
            {"name": "Olive Oil", "price": 10, "description": "High-quality olive oil."},
            {"name": "Sunflower Oil", "price": 5, "description": "Light and healthy sunflower oil."},
            {"name": "Coconut Oil", "price": 8, "description": "Natural and organic coconut oil."},
            {"name": "Mustard Oil", "price": 6, "description": "Strong and flavorful mustard oil."},
        ]
    elif category_name == "spices":
        items = [
            {"name": "Turmeric", "price": 2, "description": "Golden and aromatic turmeric."},
            {"name": "Cumin", "price": 3, "description": "Earthy and flavorful cumin."},
            {"name": "Coriander", "price": 2.5, "description": "Fresh and fragrant coriander."},
            {"name": "Chili Powder", "price": 1.5, "description": "Spicy and vibrant chili powder."},
            {"name": "Garam Masala", "price": 4, "description": "Aromatic and warm garam masala."},
        ]
    elif category_name == "snacks":
        items = [
            {"name": "Chips", "price": 2, "description": "Crispy and salty chips."},
            {"name": "Nuts", "price": 5, "description": "Healthy and crunchy nuts."},
            {"name": "Cookies", "price": 3, "description": "Sweet and delicious cookies."},
            {"name": "Popcorn", "price": 1.5, "description": "Light and fluffy popcorn."},
        ]
    elif category_name == "baked":
        items = [
            {"name": "Bread", "price": 2, "description": "Freshly baked bread."},
            {"name": "Cake", "price": 15, "description": "Delicious and moist cake."},
            {"name": "Pastry", "price": 3, "description": "Flaky and buttery pastry."},
            {"name": "Cookies", "price": 1.5, "description": "Sweet and crunchy cookies."},
        ]
    elif category_name == "beverages":
        items = [
            {"name": "Tea", "price": 1.5, "description": "Refreshing and aromatic tea."},
            {"name": "Coffee", "price": 2, "description": "Rich and strong coffee."},
            {"name": "Juice", "price": 3, "description": "Freshly squeezed juice."},
            {"name": "Soda", "price": 1, "description": "Fizzy and sweet soda."},
        ]
    elif category_name == "personal":
        items = [
            {"name": "Shampoo", "price": 5, "description": "Gentle and nourishing shampoo."},
            {"name": "Soap", "price": 2, "description": "Natural and fragrant soap."},
            {"name": "Toothpaste", "price": 3, "description": "Refreshing and minty toothpaste."},
            {"name": "Lotion", "price": 4, "description": "Moisturizing and soothing lotion."},
        ]
    context = {
        "category_name": category_name.capitalize(),
        "items": items,
    }
    return render(request, "category_items.html", context)

def add_to_cart(request, item_name, item_price):
    # Initialize the cart if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']

    # Check if the item already exists in the cart
    for item in cart:
        if item['name'] == item_name:
            # Ensure the 'quantity' key exists
            if 'quantity' not in item:
                item['quantity'] = 1
            item['quantity'] += 1  # Increase the quantity
            break
    else:
        # Add a new item to the cart
        cart.append({"name": item_name, "price": item_price, "quantity": 1})

    request.session['cart'] = cart  # Save the updated cart in the session
    request.session.modified = True  # Mark the session as modified
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', [])
    
    # Ensure all items have a 'quantity' key
    for item in cart:
        if 'quantity' not in item:
            item['quantity'] = 1

    # Calculate the total price for the cart and for each item
    for item in cart:
        item['total'] = item['price'] * item['quantity']
    total_price = sum(item['total'] for item in cart)
    
    # Save the updated cart back to the session
    request.session['cart'] = cart
    request.session.modified = True

    context = {
        "cart": cart,
        "total_price": total_price,
    }
    return render(request, "cart.html", context)

def remove_from_cart(request, item_name):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['name'] != item_name]  # Remove the item
    request.session['cart'] = cart  # Save the updated cart in the session
    request.session.modified = True
    return redirect('cart_view')

def update_cart(request, item_name, action):
    cart = request.session.get('cart', [])
    for item in cart:
        if item['name'] == item_name:
            if action == "increase":
                item['quantity'] += 1
            elif action == "decrease" and item['quantity'] > 1:
                item['quantity'] -= 1
            break
    request.session['cart'] = cart  # Save the updated cart in the session
    request.session.modified = True
    return redirect('cart_view')

def payment_page(request):
    total_price = sum(item['price'] * item['quantity'] for item in request.session.get('cart', []))
    context = {
        "total_price": total_price,
    }
    return render(request, "payment.html", context)

def process_payment(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        cart = request.session.get('cart', [])
        total_price = sum(item['price'] * item['quantity'] for item in cart)

        # Save the order to the database
        order = Order.objects.create(
            user=request.user,
            items=json.dumps(cart),  # Save cart as a JSON string
            total_price=total_price,
            payment_method=payment_method,
        )

        # Clear the cart after payment
        request.session['cart'] = []
        request.session.modified = True

        context = {
            "payment_method": payment_method,
            "total_price": total_price,
        }
        return render(request, "payment_success.html", context)
    return redirect('cart_view')

def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        "orders": user_orders,
    }
    return render(request, "orders.html", context)