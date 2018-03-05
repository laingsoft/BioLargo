from .models import SOP
from app.mixins import CompanyObjectsMixin, CompanyObjectCreateMixin
from django.views.generic import CreateView, ListView
from management.mixins import ManagerTestMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

class SOPListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    model = SOP
    paginate_by = 20


class SOPUploadView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    Used in management panel for uploading SOP files. usually PDF.
    """
    model = SOP
    fields = ('name', 'description', 'file')
    success_url = '/SOP'


@ login_required
def SOPDownloadView(request, file_id):
    """
    Does internal redirect and sends file through nginx
    """
    if request.method == 'GET':
        # check if the file exists within company. 404 if not.
        sop = get_object_or_404(SOP, company=request.user.company, id=file_id)

        response = HttpResponse()
        response['Content Type'] = ''
        response['X-Accel-Redirect'] = '/' + sop.file.url
        return response


    raise Http404