# A temporary fix for a Django bug fixed in a later version.
# https: // code.djangoproject.com/ticket/28811
# NOTE: Remove this file once this bug is offically fixed
# NOTE: Also remove the substitution in the app init.

from django.core.exceptions import FieldError
from django.db.models.expressions import Ref
from django.db.models.constants import LOOKUP_SEP


def resolve_ref_temp_fix(self, name, allow_joins=True, reuse=None, summarize=False):
    if not allow_joins and LOOKUP_SEP in name:
        raise FieldError(
            "Joined field references are not permitted in this query")
    if name in self.annotations:
        if summarize:
            # Summarize currently means we are doing an aggregate() query
            # which is executed as a wrapped subquery if any of the
            # aggregate() elements reference an existing annotation. In
            # that case we need to return a Ref to the subquery's annotation.
            return Ref(name, self.annotation_select[name])
        else:
            return self.annotations[name]
    else:
        field_list = name.split(LOOKUP_SEP)
        field, sources, opts, join_list, path = self.setup_joins(
            field_list, self.get_meta(),
            self.get_initial_alias(), reuse)
        targets, _, join_list = self.trim_joins(sources, join_list, path)
        if len(targets) > 1:
            raise FieldError("Referencing multicolumn fields with F() objects "
                                "isn't supported")
        if reuse is not None:
            reuse.update(join_list)
        col = targets[0].get_col(join_list[-1], sources[0])

        return col



