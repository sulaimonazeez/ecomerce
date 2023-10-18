from django.urls import path
from . import views
urlpatterns = [
  path("", views.home, name="home"),
  path("cart/<int:id>", views.cart_item, name="cart_item"),
  path("add/<int:id>", views.add_to_cart, name="added"),
  path("account/login", views.login_view, name="login"),
  path("cart", views.cart, name="cart"),
  path("remove/<int:id>", views.remove_from_cart, name="remove"),
  path("place", views.create_order, name="place"),
  path("order_detail/<int:id>", views.order_detail, name="order_detail"),
  path("increase/<int:id>", views.increase, name="increase"),
  path("descrease/<int:id>", views.descrease, name="descrease"),
  path("category/<int:id>", views.categoryed, name="categoryed"),
  path("logout", views.logout_view, name="logout"),
  path("signup", views.signup, name="signiup"),
]