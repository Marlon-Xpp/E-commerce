from django.urls import path
from payments import views

urlpatterns = [
    path("checkout/", views.checkout , name="checkout"),
    path("buy/",views.method_buy , name = "method_buy"),

    path("pending_page/", views.pending_page, name="pending"),
    path("success_page/", views.success_page, name="success"),
    path("failure_page/", views.failure_page, name="failure")

]