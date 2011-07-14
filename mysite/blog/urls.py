from django.conf.urls.defaults import *
from models import *
from django.views.generic import list_detail

names = {'queryset' : ArticleModel.objects.all(),
		 'template_name' : 'thanks.html',
		 'template_object_name' : 'poems',}

urlpatterns = patterns('mysite.blog.views',
	url(r'^$', 'index'),
	url(r'^category_(?P<categ>.*)['',/]$', 'cp_view', {'site_template' : 'category_display.html'}),
	url(r'^post_(?P<ids>[0-9]*)['',/]$', 'cp_view', {'site_template' : 'post_display.html'}),
	url(r'^searchquery['',/]$', 'search_query', {'site_template' : 'category_display.html'}),
	url(r'^author_page/(?P<aname>\w*)['',/]$', 'author_page'),
)
