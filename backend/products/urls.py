from django.urls import path
from .views import get_products, scrape_and_add_product_ulta, scrape_and_add_product_buymebeauty, scrape_and_add_product_clinique, delete_product

urlpatterns = [
    path('products/', get_products, name='get-products'),
    path('products/scrape/ulta/', scrape_and_add_product_ulta, name='scrape-and-add-ulta'),
    path('products/scrape/buymebeauty/', scrape_and_add_product_buymebeauty, name='scrape-and-add-buymebeauty'),
    path('products/scrape/clinique/', scrape_and_add_product_clinique, name='scrape-and-add-clinique'),
    path('products/<int:pk>/', delete_product, name='delete-product'),
]