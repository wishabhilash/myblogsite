from django.db import models, connection

# Create your models here.
class AuthorModel(models.Model):
	name = models.CharField(max_length = 100)
	personal_desc = models.TextField()
	address = models.CharField(max_length = 500)
	email = models.EmailField()
	author_image = models.CharField(max_length = 500)
	
	def __unicode__(self):
		return self.name

class CategoryModel(models.Model):
	category = models.CharField(max_length = 20)
	
	def __unicode__(self):
		return self.category

class ArticleModel(models.Model):
	title = models.CharField(max_length = 150)
	article = models.TextField()
	image = models.CharField(max_length = 500)
	post_time = models.TimeField(auto_now_add = True)
	post_date = models.DateField()
	author = models.ManyToManyField(AuthorModel)
	category = models.ForeignKey(CategoryModel)
	
	def __unicode__(self):
		return self.title

