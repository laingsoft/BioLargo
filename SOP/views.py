from .models import SOP
from app.mixins import CompanyObjectsMixin, CompanyObjectCreateMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from management.mixins import ManagerTestMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from api.serializers import SimpleSOPSerializer
from app.models import Experiment

class SOPListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    model = SOP
    paginate_by = 20


class SOPUploadView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    Used in management panel for uploading SOP files. usually PDF.
    """
    model = SOP
    fields = ('name', 'description', 'file')
    success_url = '/management/sop'


@ login_required
def SOPDownloadView(request, file_id):
    """
    Does internal redirect and sends file through nginx. Only requires user to
    be logged in.
    """
    if request.method == 'GET':
        # check if the file exists within company. 404 if not.
        sop = get_object_or_404(SOP, company=request.user.company, id=file_id)

        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={0}".format(sop.file.name[4:])
        response['X-Accel-Redirect'] = '/files/' + sop.file.url
        return response

    raise Http404


class SOPUpdateView(ManagerTestMixin, CompanyObjectsMixin, DetailView):
    model = SOP
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        print(kwargs['object'].id)
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['experiments'] = Experiment.objects.filter(sop = kwargs['object'])
        return context
    template_name = 'SOP/sop_form.html'


@login_required
def findSOP(request):
    if request.method == 'GET':
        qs = request.user.company.sop_set.filter(name__icontains=request.GET.get('q', ''))
        return JsonResponse({'data': SimpleSOPSerializer(qs, many=True).data})
