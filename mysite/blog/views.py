# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from processors import *
from forms import *
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
	if ArticleModel.objects.all():
		post = ArticleModel.objects.all().order_by('-post_date')
		paginator = Paginator(post, 5)
		if request.GET.get('page'):
			page_no = request.GET.get('page')
		else:
			page_no = 1
		try:
			posts = paginator.page(page_no)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
		
	else:
		post = []
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
			data = form.cleaned_data['search_box']
			result = (ArticleModel.objects.filter(Q(title__icontains = data)|Q(article__icontains = data))).order_by('-post_date')
			paginator = Paginator(result, 10)
			if request.GET.get('page'):
				page_no = request.GET.get('page')
			else:
				page_no = 1
			try:
				posts = paginator.page(page_no)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)
			
			if result:		
				return render_to_response(site_template, {'posts' : result, 'query' : data, 'message' : "yes i m working"},
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
	
def parse_url(request, year, month, title):
	title = title.replace('_',' ')
	posts = ArticleModel.objects.get(post_date__year = int(year), post_date__month = int(month), title__icontains = title)
	if posts:
		return render_to_response('post_display.html', {'posts' : posts},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
	else:
		return render_to_response('post_display.html', {'message' : "No posts in this category yet!!!"},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))

def parse_month_url(request, year, month):
	posts = ArticleModel.objects.filter(post_date__year = int(year), post_date__month = int(month)).order_by('-post_date')
	if posts:
		return render_to_response('category_display.html', {'posts' : posts},
		context_instance = RequestContext(request, processors = [base_processors, tree_processors]))
