from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Item, ItemField

class ItemList(ListView):
    '''
    Lists all of the Items that are in place in the inventory. 
    Only returns the ones that belong to the company the user is in
    '''
    model = Item
    template_name = "inventory/item_list.html"
    def get(self, request, *args, **kwargs):
        retval = Item.objects.filter(company = request.user.company)
        categories = set()
        objects = []
        for i in retval:
            categories.add(i.category)
            objects.append( { "fields":ItemField.objects.filter(item_pointer = i), "item":i})

        return render(request, self.template_name, {"object_list":objects, "categories":categories})
    
class ItemCreate(CreateView):
    '''
    Allows the user to create an inventory item for their company.
    '''
    model = Item
    fields = ['name','description', 'on_hand', 'category']

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(ItemCreate, self).form_valid(form)

class ItemDetail(DetailView):
    '''
    
    '''
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        item = context['item']
        Fields = ItemField.objects.filter(item_pointer = item)
        context['fields'] = Fields
        return context
        

