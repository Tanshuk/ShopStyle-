"""Placeholder views — fully implemented in Step 5 (Cart App)."""
from django.shortcuts import render

def cart_detail_view(request):
    return render(request, 'placeholder.html', {'title': 'Shopping Cart'})