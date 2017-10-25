# this file contains the Experiment filter.

# dictionary of all filters, with corresponding function/method.
FILTERS = {
    "metadata_filters": ExperimentFilter.filter_metadata,
    "experiment_filters": ExperimentFilter.filter_experiment_data,
    "order_by": ExperimentFilter.order_by,
    "tags": ExperimentFilter.filter_tags,
    "id": ExperimentFilter.filter_id,
    "group": ExperimentFilter.filter_group,
}


class ExperimentFilter():
    def __init__(self, **kwargs):
        self.qs = Experiment.objects.all()
        self.limit = kwargs.pop('limit', None) 
        self.offset = kwargs.pop('offset', 0)
        
        for key, value in kwargs.items():
            try:
                FILTERS[key](value)
            except: 
                pass
            
        
    # the static methods are all filters. all take qs (queryset) as a 
    # parameter, and return a queryset.
    
    # filters by experiment id
    # q: id number
    @staticmethod
    def filter_id(qs, q):
        filtered = qs.filter(id = id_num)
        return filtered
        
    # orders by a field in ascending or descing order.
    # q: tuple (field, 'asc' | 'desc')   
    # Taken from:
    # https://stackoverflow.com/questions/36641759/django-1-9-jsonfield-order-by
    # Oct 25 2017
    @staticmethod
    def order_by(qs, q):
        field = q[0]
        order = q[1]
        
        if order.lower() == "asc":
            return qs.order_by(RawSQL("LOWER(metadata-->%s)", (field,)).asc())
        else if order.lower() == "desc":
            return qs.order_by(RawSQL("LOWER(metadata-->%s)", (field,)).desc())
    
    # filters by a dictionary of metadata fields and values.
    # q: metadata fields. If the field doesn't exist, this does nothing.
    @staticmethod
    def filter_metadata(qs, q):
        return qs.filter(metadata__contains = q)
        
    # filters by experiment data fields 
    # q: dictionary of fields and value. 
    @staticmethod
    def filter_experiment_data(qs, q):
        return qs.filter(experimentdata__experimentData__contains = q)
        
        
    # filters by tags.
    # q: list of tag names.
    @staticmethod
    def filter_tags(qs, q):
        return qs.filter(tags__name in q).distinct()
        
    # filters by group
    # q: group name
    @staticmethod
    def filter_group(qs, q):
        return qs.filter(group__name = q)
         
        
    # gets the total number of filtered results.
    # arguments: none
    # returns: an int
    def get_total_results(self):
        return self.qs.count()
        
    # gets truncated (according to limit and offset) queryset.
    # arguments: none
    # returns: query set
    def get_qs(self):
        if limit:
            return self.qs[self.offset: self.offset + self.limit]
        return self.qs[self.offset: None]
        
    # gets all filtered experiments. 
    # arugments: none
    # returns: queryset
    def get_all_results(self):
        return qs
