from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, register_converter
from . import views

# Define a custom path converter for float
class FloatConverter:
    regex = r'\d+(\.\d+)?'  # Matches integers and floats
    def to_python(self, value):
        return float(value)  # Convert the matched value to a float
    def to_url(self, value):
        return str(value)  # Convert the float back to a string for the URL

# Register the custom converter
register_converter(FloatConverter, 'float')

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('update-password/', views.update_password_view, name='update_password'),
    path('category/<str:category_name>/', views.category_items, name='category_items'),
    path('add-to-cart/<str:item_name>/<float:item_price>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<str:item_name>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<str:item_name>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.payment_page, name='payment_page'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('orders/', views.orders, name='orders'),
    path('support/', views.support_view, name='support'),
    path('raise-ticket/', views.raise_ticket_view, name='raise_ticket'),
    path('orders/<int:order_id>/', views.order_items_view, name='order_items'),

    # path('admin/', admin.site.urls),
    
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
