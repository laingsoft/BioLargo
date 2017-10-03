from django.template import Library
register = Library()

@register.filter(name="addclass")
def formcontrol(field, attr):
    return field.as_widget(attrs={"class":attr})
