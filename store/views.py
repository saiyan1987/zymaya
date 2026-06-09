from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CheckoutForm
from .models import Category, OrderItem, Product, ProductVariant

def home(request):
    categories=Category.objects.all()[:4]
    featured=Product.objects.filter(is_active=True, is_featured=True).prefetch_related('variants')[:8]
    return render(request,'store/home.html',{'categories':categories,'featured_products':featured})

def product_list(request, category_slug=None):
    categories=Category.objects.all()
    products=Product.objects.filter(is_active=True).select_related('category').prefetch_related('variants')
    active_category=None
    if category_slug:
        active_category=get_object_or_404(Category, slug=category_slug)
        products=products.filter(category=active_category)
    return render(request,'store/product_list.html',{'categories':categories,'products':products,'active_category':active_category})

def product_detail(request, slug):
    product=get_object_or_404(Product.objects.prefetch_related('variants'), slug=slug, is_active=True)
    return render(request,'store/product_detail.html',{'product':product})

@require_POST
def cart_add(request):
    variant=get_object_or_404(ProductVariant, id=request.POST.get('variant_id'))
    qty=int(request.POST.get('quantity',1))
    Cart(request).add(variant, qty)
    return redirect('store:cart_detail')

def cart_remove(request, variant_id):
    Cart(request).remove(variant_id)
    return redirect('store:cart_detail')

def cart_detail(request): return render(request,'store/cart_detail.html')

def checkout(request):
    cart=Cart(request)
    if len(cart)==0: return redirect('store:product_list')
    if request.method=='POST':
        form=CheckoutForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False); order.total=cart.get_total_price(); order.save()
            for item in cart:
                OrderItem.objects.create(order=order, variant=item['variant'], quantity=item['quantity'], price=item['price'])
            cart.clear(); return redirect('store:order_success', order_id=order.id)
    else: form=CheckoutForm()
    return render(request,'store/checkout.html',{'form':form})

def order_success(request, order_id):
    return render(request,'store/order_success.html',{'order_id':order_id})
