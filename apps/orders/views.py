from django.shortcuts import render
def order_list_view(request):
    return render(request, 'placeholder.html', {'title': 'My Orders'})
def order_detail_view(request, order_number):
    return render(request, 'placeholder.html', {'title': 'Order Detail'})