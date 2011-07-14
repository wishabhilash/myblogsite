# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from processors import *
from forms import *
from django.core.context_processors import csrf

def index(request):
	if ArticleModel.objects.all():
		posts = ArticleModel.objects.all().order_by('-post_date')[:10] or ArticleModel.objects.all().order_by('-post_date')
	else:
		posts = []
	return render_to_response('index_page.html', 
	context_instance = RequestContext(request, {'posts' : posts}, processors = [base_processors, tree_processors]))


def cp_view(request, site_template, ids = None, categ = None):
	if categ:
		obj = CategoryModel.objects.get(category = categ)
		posts = obj.articlemodel_set.all()
	elif ids:
		posts = ArticleModel.objects.get(id = ids)
	if posts:
		return render_to_response(site_template, {'posts' : posts},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
	else:
		return render_to_response(site_template, {'message' : "No posts in this category yet!!!"},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))

def search_query(request, site_template):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			result = []
			res = []
			data = list(form.cleaned_data['search_box'].split())
	
			for dat in data:
				res.append(ArticleModel.objects.filter(title__icontains = dat))
				res.append(ArticleModel.objects.filter(article__icontains = dat))
			for objs in res:
				for obj in objs:
					if obj not in result:
						result.append(obj)
			if result:		
				return render_to_response(site_template, {'posts' : result, 'message' : "yes i m working"},
				context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
			else:
				return render_to_response(site_template, {'message' : "No posts in this category yet!!!"},
				context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
	else:
		form = SearchForm()
	c['form'] = form
	return render_to_response('category_display.html', c)

def author_page(request, aname):
	author = AuthorModel.objects.get(name = aname)
	if author:
		return render_to_response('author_page.html', {'author' : author, 'message' : "yes i m working"},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
	else:
		return render_to_response('author_page.html', {'author' : author, 'message' : "No author found!!!"},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
	
