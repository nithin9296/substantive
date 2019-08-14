models.py

class Category(models.Model):  #Cycle
	name  = models.Charfield(max_length=10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):  #Objectives
	name = models.Charfield(max_length=30)
	price = models.DecimalField(decimal_places=2, max_digits=10)
	category = models.ForeignKey(Category)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


Forms.py

class ProductForm(form.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'price', 'category')

	def __init__(self, user, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.objects.filter(user=user)

Views.py

def new_product(request):
	if request.method == 'POST':
		form = ProductForm(request.user, request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			return redirect('product_list')
	else:
		form = ProductForm(request.user)
	return render(reqeust, 'product_form.html', {'form': form})

Views.py

def edit_all_products(request):
	ProductFormSet = modelformset_factory(Product, fields=('name', 'price', 'category'), extra=0)
	data = request.POST or None
	formset = ProductFormSet(data=data, queryset= Category.objects.filter(user=request.user))
	for form in formset:













