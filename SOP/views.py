from .models import SOP
from app.mixins import CompanyObjectsMixin, CompanyObjectCreateMixin
from django.views.generic import CreateView, ListView
from management.mixins import ManagerTestMixin


class SOPListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    model = SOP
    paginate_by = 20


class SOPUploadView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    model = SOP
    fields = ('name', 'description', 'file')
    success_url = '/SOP'

