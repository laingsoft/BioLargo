# Paul Kenjora, Modified and Improved by Carly Stambaugh
# https://en.gravatar.com/site/implement/images/django/

import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
 
register = template.Library()
 
# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=40):
  default = "https://example.com/static/images/defaultavatar.jpg"
  email = email.encode('utf-8')
  return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.parse.urlencode({'d':default, 's':str(size)}))
 
# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img class ="rounded-circle" src="%s" width="%d" height="%d">' % (url, size, size))
