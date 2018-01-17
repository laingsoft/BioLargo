from django.shortcuts import redirect
from json import loads


class CompanyObjectsMixin:
    """
    Mixin for overriding get_queryset in l
    """
    def get_queryset(self):
        """
        method to set queryset for retrieving objects for user's company only.
        """
        qs = super().get_queryset()
        qs = qs.filter(company=self.request.user.company)
        return qs


class CompanyObjectCreateMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user.company
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class BaseFilterMixin(CompanyObjectsMixin):
    """
    Base Filter Mixin for query sets. FILTERS and ORDER_BY from another mixin.
    """

    def get_queryset(self):
        """
        Gets a queryset with specified filters from request.GET
        overrides django.views.generic.list.MultipleObjectMixin.get_queryset
        """

        qs = super().get_queryset()  # get company specific queryset

        filters = dict(self.request.GET.lists())  # dictionary of lists

        # pull out order_by and order
        order_by = filters.pop("order_by", None)
        order = filters.pop("order", "asc")

        if order_by in self.ORDER_FIELDS:
            if order == "desc":
                qs = qs.order_by("-" + order_by)
            else:
                qs = qs.order_by(order_by)
        else:
            qs = qs.order_by("-id")  # default to descending id order

        for f in filters:
            try:
                if any(filters[f]):
                    qs = self.FILTERS[f](qs, filters[f])
            except KeyError:
                pass  # do nothing if not a filter.

        return qs


class ExpFilterMixin(BaseFilterMixin):
    """
    Filter mixin for filtering experiments. Inherits from CompanyObjectMixin
    to get company specific experiments.
    """

    # a dictionary of existing filters
    # x is the param(as a list) from the querydict, which is a dictionary of
    # lists. Metadata and fields are JSON strings.
    FILTERS = {
        "name": lambda qs, x: qs.filter(friendly_name__icontains=x[0]),
        "project_name": lambda qs, x: qs.filter(project__name__icontains=x[0]),
        "before_date": lambda qs, x: qs.filter(create_timestamp__lt=x[0]),
        "after_date": lambda qs, x: qs.filter(create_timestamp__gt=x[0]),
        "on_date": lambda qs, x: qs.filter(create_timestamp=x[0]),
        "metadata": lambda qs, x: qs.filter(
            metadata__contains=loads(x[0])),
        "fields": lambda qs, x: qs.filter(
            experimentdata__experimentData__contains=loads(x[0])).distinct('id'),
        "tags": lambda qs, x: qs.filter(
          tags__name__in=x).distinct('id'),
    }

    ORDER_FIELDS = (
        "create_timestamp",
        "project__name",
        "friendly_name",
        "user"
    )


class ProjectFilterMixin(BaseFilterMixin):
    """
    filter mixin for filtering projects.
    """

    # a dictionary of existing filters
    FILTERS = {
        "name": lambda qs, x: qs.filter(name=x),
        "start": lambda qs, x: qs.filter(start_date__gte=x),
        "end": lambda qs, x: qs.filter(end_date__lte=x),
        "description": lambda qs, x: qs.filter(description__icontains=x)
    }

    ORDER_FIELDS = (
        "name",
        "start_date",
        "end_date"
    )
