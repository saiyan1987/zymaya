from decimal import Decimal
from .models import ProductVariant
class Cart:
    def __init__(self, request):
        self.session=request.session
        self.cart=self.session.setdefault('cart', {})
    def add(self, variant, quantity=1, override=False):
        vid=str(variant.id)
        if vid not in self.cart:
            self.cart[vid]={'quantity':0,'price':str(variant.final_price)}
        self.cart[vid]['quantity']=quantity if override else self.cart[vid]['quantity']+quantity
        self.save()
    def remove(self, variant_id):
        self.cart.pop(str(variant_id), None); self.save()
    def clear(self):
        self.session['cart']={}; self.session.modified=True
    def save(self): self.session.modified=True
    def __iter__(self):
        ids=self.cart.keys(); variants=ProductVariant.objects.select_related('product').filter(id__in=ids)
        lookup={str(v.id):v for v in variants}
        for vid,item in self.cart.items():
            variant=lookup.get(vid)
            if not variant: continue
            price=Decimal(item['price']); qty=item['quantity']
            yield {'variant':variant,'quantity':qty,'price':price,'total':price*qty}
    def __len__(self): return sum(i['quantity'] for i in self.cart.values())
    def get_total_price(self): return sum(i['total'] for i in self)
