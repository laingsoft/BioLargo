from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Item

class ItemList(ListView):
    model = Item
    template_name = "inventory/item_list.html"
    def get(self, request, *args, **kwargs):
        retval = Item.objects.filter(company = request.user.company)
        return render(request, self.template_name, {"object_list":retval})
    

class ItemCreate(CreateView):
    model = Item
    fields = ['description']

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super(ItemCreate, self).form_valid(form)

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        return context
        
# Create your views here.
def index(request):
    return render(request, 'inventory/index.html')
