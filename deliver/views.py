from django.shortcuts import render
from django.views import View
from .models import MenuItem, Checkout


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class Menu(View):
    # get method start
    def get(self, request, *args, **kwargs):
        # get every item from each category
        meals = MenuItem.objects.filter(
            category__name__contains='Meals')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'meals': meals,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'menu.html', context)
    # get method end


    # post method start
    def post(self, request, *args, **kwargs):
        # create a dictionary for items
        order_items = {
            'items': []
        }
        # grab items and make a list
        items = request.POST.getlist('items[]')

        # loop through these items
        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []
        # loop through items which customer like to order
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

            # finally add items to order
            order = Checkout.objects.create(price=price)
            order.items.add(*item_ids)

            context = {
                'items': order_items['items'],
                'price': price
            }

            return render(request, 'cart.html', context)
        # post method end
    