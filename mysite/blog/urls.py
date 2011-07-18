from django.conf.urls.defaults import *
from models import *
from django.views.generic import list_detail

names = {'queryset' : ArticleModel.objects.all(),
		 'template_name' : 'thanks.html',
		 'template_object_name' : 'poems',}

urlpatterns = patterns('mysite.blog.views',
	url(r'^$', 'index'),
	url(r'^category_(?P<categ>.*)['',/]$', 'cp_view', {'site_template' : 'category_display.html'}),
	url(r'^(?P<year>\d{0,4})['',/](?P<month>\d{0,2})['',/](?P<title>[\w_",!.:?-]*)['',/]$', 'parse_url'),
	url(r'^(?P<year>\d{0,4})['',/](?P<month>\d{0,2})['',/]$', 'parse_month_url'),
	url(r'^searchquery['',/]$', 'search_query', {'site_template' : 'category_display.html'}),
	url(r'^author_page/(?P<aname>[\w,\s]*)['',/]$', 'author_page'),
)
