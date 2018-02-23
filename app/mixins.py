from django.shortcuts import redirect
from json import loads
from django.db.models import Q
import operator
from functools import reduce


def load_val(x):
    """
    Error handling for loading fields sent as JSON. If values is not JSON
    (in case of search, usually), it returns the value as is.
    """
    try:
        val = loads(x)
    except ValueError:
        return x
    return val


def to_bool(x):
    """
    Converts a string to a bool value. Case insensitive.
    """
    if x.lower() == "false":
        return False
    else:
        return True


class CompanyObjectsMixin:
    """
    Mixin for overriding get_queryset in l
    """
    def get_queryset(self):
        """
        method to set queryset for retrieving objects for user's company only.
        orders qs with descending id.
        """
        qs = super().get_queryset()
        qs = qs.filter(company=self.request.user.company).order_by("-pk")
        return qs


class CompanyObjectCreateMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user.company
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class BaseFilterMixin:
    """
    Base Filter Mixin for query sets defining the get_queryset method.
    Must have the following variables defined:
    FILTERS: dictonary of functions returning ("field", value)
    ORDER_FIELDS: tuple/list or field names that can be used for ordering.
    """

    def get_queryset(self):
        """
        Gets a queryset with specified filters from request.GET
        overrides django.views.generic.list.MultipleObjectMixin.get_queryset
        """

        qs = super().get_queryset()

        filters = dict(self.request.GET.lists())  # dictionary of lists

        Q_objects = []

        # Search will check all fields (OR them together), excluding time and
        # date fields (format problems). Search takes precedence; filters will
        # be ignored.
        if "search" in filters and filters["search"][0].strip():
            for key, f in self.FILTERS.items():
                if "time" not in key and "date" not in key:
                    Q_objects.append(Q(f(filters["search"])))

            qs = qs.filter(reduce(operator.or_, Q_objects))

        else:
            # Create filters as Q objects.
            for key, value in filters.items():
                try:
                    if any(value):
                        Q_objects.append(Q(self.FILTERS[key](value)))
                except KeyError:
                    pass  # do nothing if not a filter.

            if Q_objects:
                qs = qs.filter(reduce(operator.and_, Q_objects))

        # order queryset
        order_by = self.request.GET.get("order_by", None)
        order = self.request.GET.get("order", "asc")

        if order_by in self.ORDER_FIELDS:
            if order == "desc":
                qs = qs.order_by("-" + order_by)
            else:
                qs = qs.order_by(order_by)

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
        "name": lambda x: ("friendly_name__icontains", x[0]),
        "project_name": lambda x: ("project__name__icontains", x[0]),
        "before_date": lambda x: ("create_timestamp__lte", x[0]),
        "after_date": lambda x: ("create_timestamp__gte", x[0]),
        "metadata": lambda x: ("metadata__contains", load_val(x[0])),
        "fields": lambda x: ("experimentdata__experimentData__contains", load_val(x[0])),
        "tags": lambda x: ("tags__name__in", x),
    }

    ORDER_FIELDS = (
        "create_timestamp",
        "project__name",
        "friendly_name",
    )


class ProjectFilterMixin(BaseFilterMixin):
    """
    filter mixin for filtering projects.
    """

    # a dictionary of existing filters
    FILTERS = {
        "name": lambda x: ("name__icontains", x[0]),
        "start_date": lambda x: ("start_date__gte", x[0]),
        "end_date": lambda x: ("end_date__lte", x[0]),
        "description": lambda x: ("description__icontains", x[0])
    }

    ORDER_FIELDS = (
        "name",
        "start_date",
        "end_date"
    )


class UserFilterMixin(BaseFilterMixin):
    """
    filter mixin for filtering users.
    """

    FILTERS = {
        "first": lambda x: ("first_name__icontains", x[0]),
        "last": lambda x: ("last_name__icontains", x[0]),
        "email": lambda x: ("email__icontains", x[0]),
        "is_active": lambda x: ("is_active", x[0])
    }

    ORDER_FIELDS = (
        "first_name",
        "last_name",
        "email",
        "is_active"
        )
