
 
model = Item
template_name = 'product.html'


class CartView(View):
def get(self, *args, **kwargs): try:
order = Order.objects.get(user=self.request.user, ordered=False) context = {
'order': order
}
return render(self.request, 'cart.html', context) except ObjectDoesNotExist:
messages.success(self.request, "You don't have an active order") return redirect('index')


class CheckoutView(View):
def get(self, *args, **kwargs):
order = Order.objects.get(user=self.request.user, ordered=False) address = Address.objects.filter(user=self.request.user, default=True) form = AddressForm()
context = {
'form': form, #'order': order, 'address': address
}
return render(self.request, 'purchase.html', context)


def post(self, *args, **kwargs):
order = Order.objects.get(user = self.request.user, ordered=False) form = AddressForm(self.request.POST or None)
if form.is_valid():
street_address = form.cleaned_data.get('street_address') apartment_address = form.cleaned_data.get('apartment_address') city = form.cleaned_data.get('city')
pin = form.cleaned_data.get('pin')
save_info = form.cleaned_data.get('save_info') use_default = form.cleaned_data.get('use_default') payment_option = form.cleaned_data.get('payment_option')

address = Address( user=self.request.user, street_address=street_address,
 
apartment_address=apartment_address, city=city,
pin=pin,
)
address.save() if save_info:
address.default = True address.save()

order.address = address order.save()

if use_default:
address = Address.objects.get( user=self.request.user, default=True)
order.address = address order.save()


else:
print('form invalid') return redirect('purchase')
def index(request):
return render(request, 'index.html')

def products(request):
return render(request, 'products.html')

def logout1(request): logout(request)
return redirect('/login/')


def register(request):
form = UserRegisterForm(request.POST or None) if form.is_valid():
user = form.save(commit=False)
password = form.cleaned_data.get('password') email = form.cleaned_data.get('email')
# print(email) user.set_password(password)
new_user = authenticate(username=user.username, password=password) user.save()
return redirect('/login/') context = {
 
'form': form,
}
return render(request, "register.html", context)


def login1(request):
form = UserLoginForm(request.POST or None) if form.is_valid():
username = form.cleaned_data.get('username') password = form.cleaned_data.get('password') obje = User.objects.filter(username = username)
user = authenticate(username=username, password=password) login(request, user)
return redirect('/')

context = {
'form': form,
}
return render(request, "login.html", context)

def add_to_cart(request, slug):
item = get_object_or_404(Item, slug=slug)
order_item, created = OrderItem.objects.get_or_create(item=item, user=requ est.user, ordered=False)
order_qs = Order.objects.filter(user=request.user, ordered=False) if order_qs.exists():
order = order_qs[0]
if order.items.filter(item slug=item.slug).exists(): order_item.quantity += 1
order_item.save()
messages.success(request, f"{item.title}'s quantity was updated") return redirect('cart')
else:
order.items.add(order_item)
messages.success(request, f"{item.title} was added to your cart") return redirect('cart')
else:
ordered_date = timezone.now()
order = Order.objects.create(user=request.user, ordered=False, ordered
_date=ordered_date)
order.items.add(order_item)
messages.success(request, f"{item.title} was added to your cart") return redirect('cart')
 
def remove_from_cart(request, slug):
item = get_object_or_404(Item, slug=slug)
order_item, created = OrderItem.objects.get_or_create(item=item, user = re quest.user, ordered=False)
order_qs = Order.objects.filter(user=request.user, ordered=False) if order_qs.exists():
order = order_qs[0]
if order.items.filter(item slug=item.slug).exists(): order.items.remove(order_item)
order.save()
messages.success(request, f"{item.title} was removed from your car
 
t")
 

return redirect('cart') else:
messages.info(request, f"{item.title} is not in your cart") return redirect('cart')
 
else:
messages.info(request, "You don't have an active order!") return redirect('product', slug=slug)


def remove_single_from_cart(request, slug): item = get_object_or_404(Item, slug=slug)
order_item, created = OrderItem.objects.get_or_create( item=item, user=request.user, ordered=False)
order_qs = Order.objects.filter(user=request.user, ordered=False) if order_qs.exists():
order = order_qs[0]
if order.items.filter(item slug=item.slug).exists(): if order_item.quantity > 1:
order_item.quantity -= 1 order_item.save()
else:
order.items.remove(order_item) order.save()
messages.success(request, f"{item.title}'s quantity was updated") return redirect('cart')
else:
messages.info(request, f"{item.title} was not in your cart") return redirect('cart')
else:
messages.info(request, "You don't have an active order") return redirect('cart')
