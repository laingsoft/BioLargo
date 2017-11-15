from .models import Experiment
from django.db.models.expressions import RawSQL

# orders by a field in ascending or descing order.
# Arguments:
#   q: tuple (field, 'asc' | 'desc')   
#   qs: queryset
# returns: a queryset.
# Taken from:
# https://stackoverflow.com/questions/36641759/django-1-9-jsonfield-order-by
# Oct 25 2017
def order_by(qs, q):
    field = q[0]
    order = q[1]
        
    if field in ('id', 'tag', 'group'):
        if order == "desc":
            field = '-' + field
        
        return qs.order_by(field)
            
        
    if order.lower() == "asc":
        return qs.order_by(RawSQL("LOWER(metadata->>%s)", (field,)).asc())
    elif order.lower() == "desc":
        return qs.order_by(RawSQL("LOWER(metadata->>%s)", (field,)).desc())
            
            
# filters by experiment id
# q: id number
#   qs: queryset
# returns: a queryset.
def filter_id(qs, q):
     return qs.filter(id = q)
    
# filters by a dictionary of metadata fields and values.
# q: metadata fields. If the field doesn't exist, this does nothing.
#   qs: queryset
# returns: a queryset.
def filter_metadata(qs, q):
    return qs.filter(metadata__contains = q)
    
# filters by experiment data fields 
# q: dictionary of fields and value. 
#   qs: queryset
# returns: a queryset.
def filter_experiment_data(qs, q):
    return qs.filter(experimentdata__experimentData__contains = q).distinct()
    
    
# filters by tags.
# q: list of tag names.
#   qs: queryset
# returns: a queryset.
def filter_tags(qs, q):
    return qs.filter(tags__name__in = q).distinct()
    
# filters by group
# q: group name
#   qs: queryset
# returns: a queryset.
def filter_group(qs, q):
    return qs.filter(group__name__icontains = q)
     

# dictionary of all available filters 
FILTERS = {
    "metadata_filters": filter_metadata,
    "experiment_filters": filter_experiment_data,
    "order_by": order_by,
    "tags": filter_tags,
    "id": filter_id,
    "group": filter_group,
}


def filter_experiments(**kwargs):
    qs = Experiment.objects.all()
    limit = kwargs.pop('limit', 20) # limit will default to 20 if not provided.
    offset = kwargs.pop('offset', 0)
    
    # filter
    for key, value in kwargs.items():
        try:
            qs = FILTERS[key](qs, value)
        except KeyError: 
            pass # do nothing if key is not in dictionary
            
    
    # get total count
    total_count = qs.count()
    
    # apply limit and offset
    qs = qs[offset: offset + limit]
            
    return qs, total_count
