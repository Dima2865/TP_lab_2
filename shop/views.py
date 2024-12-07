from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.db.models import F
from django.urls import reverse

from .models import Product, Purchase, Customers


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()

        # учет кол-ва покупок покупателей
        if Customers.objects.filter(name=self.object.person).exists():
            # purchase_count = Customers.objects.filter(name=self.object.person).values('purchase_count')
            Customers.objects.filter(name=self.object.person).update(purchase_count=F('purchase_count')+1)
        else:
            Customers.objects.create(name=self.object.person, purchase_count=1, discount=0)

        # подсчет скидок
        calculate_discounts_for_customers()

        # получение скидки на товар и его цены
        customer = Customers.objects.filter(name=self.object.person).first()
        discount = customer.discount
        product = Product.objects.filter(id=self.object.product.id).first()
        price = product.price

        # изменение итоговой цены в таблице с данными заказа
        Purchase.objects.filter(product=self.object.product.id).update(final_price=subtract_percent(price, discount))

        # получение итоговой цены
        purchase_price = Purchase.objects.filter(product=self.object.product.id).values("final_price").first()
        final_price = purchase_price['final_price']

        # получение остальных данных о заказе
        # purchase_price = Purchase.objects.filter(product=self.object.product.id).values("id").first()
        # id_ = purchase_price['id']
        # purchase_price = Purchase.objects.filter(product=self.object.product.id).values("person").first()
        # person = purchase_price['person']
        # purchase_price = Purchase.objects.filter(product=self.object.product.id).values("address").first()
        # address = purchase_price['address']
        # purchase_price = Purchase.objects.filter(product=self.object.product.id).values("date").first()
        # date = purchase_price['date']
        # purchase_price = Purchase.objects.filter(product=self.object.product.id).values("product").first()
        # product = purchase_price['product']

        link = reverse('index')
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!'
                            f'<br>Итоговая цена - {final_price} руб.'
                            f'<br><a href="{link}">Вернуться на список товаров</a>'
                            f'<br><br><br>'
                            # f'ID - {id_}<br>'
                            # f'Person - {person}<br>'
                            # f'Address - {address}<br>'
                            # f'Date - {date}<br>'
                            # f'Product - {product}<br>'
                            )


# class CustomersListCreate(CreateView):
#     model = Customers
#     fields = ['name', 'purchase_count', 'discount']


def customers_list(request):
    customers = Customers.objects.all()
    context = {'customers': customers}

    calculate_discounts_for_customers()
    return render(request, 'shop/customers_form.html', context)


def calculate_discounts_for_customers():
    customers = Customers.objects.all()
    for customer in customers:
        if customer.purchase_count < 5:
            Customers.objects.filter(purchase_count=customer.purchase_count).update(discount=0)
        if 10 > customer.purchase_count > 5:
            Customers.objects.filter(purchase_count=customer.purchase_count).update(discount=5)
        if customer.purchase_count > 10:
            Customers.objects.filter(purchase_count=customer.purchase_count).update(discount=10)


def subtract_percent(x, y):
    return x - (y / 100) * x
