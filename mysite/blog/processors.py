from models import *
from forms import *

def base_processors(request):
	categories = CategoryModel.objects.all()
	form = SearchForm()
	return {'categories' : categories, "form":form}

def tree_processors(request):
	objs = ArticleModel.objects.values('post_date').order_by('-post_date')
	years = []
	for obj in objs:
		if obj['post_date'].year not in years:
			years.append(obj['post_date'].year)
		
	monthlist = []
	postlist = []
	data = []
	for year in years:
		for month in range(12,0,-1):
			posts = ArticleModel.objects.filter(post_date__year = year, post_date__month = month).order_by('-post_date')
			if posts:
				postlist = [month, posts]
				monthlist.append(postlist)
		data.append([year,monthlist])
		monthlist, postlist = [], []
	return {'hdata' : data}


'''def tree_processors(request):
	objs = ArticleModel.objects.all().order_by('-post_date')
	year_list = []
	for obj in objs:
		if not obj.post_date.year in year_list:
			year_list.append(obj.post_date.year)
	return {'hdata' : objs, "year_list" : year_list}'''
