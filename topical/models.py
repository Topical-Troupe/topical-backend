from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

MAX_DESCRIPTION_LEN = 8192
MAX_NAME_LEN = 512

DEFAULT_EXCLUSIONS = ["bacitracin", "benzalkonium chloride", "cobalt chloride", "formaldehyde", "fragrance", "potassium dichromate", "nickel", "neomycin", "methylisothiazolinone", "methyldibromo glutaronitrile", "benzophenone 4"]

class User(AbstractUser):
	is_setup = models.BooleanField(default=False)
	def get_default_exclusions():
		common_names = IngredientName.objects.filter(name__in = DEFAULT_EXCLUSIONS)
		return Ingredient.objects.filter(names__in = common_names).all()

class Product(models.Model):
	name = models.CharField(max_length = MAX_NAME_LEN)
	description = models.TextField(max_length = MAX_DESCRIPTION_LEN, null = True)
	upc = models.CharField(max_length = 14, null = True, unique = True)
	image_url = models.CharField(max_length = MAX_DESCRIPTION_LEN, null =  True)
	def __str__(self):
		return f'{self.upc} | {self.name}'

class Ingredient(models.Model):
	name = models.CharField(max_length = MAX_NAME_LEN)
	slug = models.CharField(max_length = MAX_NAME_LEN, unique = True)
	description = models.TextField(max_length = MAX_DESCRIPTION_LEN, blank = True)
	in_products = models.ManyToManyField(to = Product, symmetrical = True, related_name = 'ingredients')
	excluded_by = models.ManyToManyField(to = get_user_model(), symmetrical = True, related_name = 'excluded_ingredients', blank = True)
	def save(self, *args, **kwargs):
		self.slug = self.generate_slug()
		basename = self.ensure_basename()
		super(Ingredient, self).save(*args, **kwargs)
		if basename is not None:
			basename.save()
	def __str__(self):
		return self.name
	def generate_slug(self):
		return (self.name.lower().replace(' ', '-'))
	def ensure_basename(self):
		test = self.names.filter(name = self.name)
		if len(test) == 0:
			basename = IngredientName()
			basename.name = self.name
			basename.ingredient = self
			return basename
	def by_name(name):
		names = IngredientName.objects.filter(name__iexact = name)
		res = Ingredient.objects.filter(names__in = names)
		if len(res) == 0:
			return None
		else:
			return res[0]

class IngredientName(models.Model):
	ingredient = models.ForeignKey(to = Ingredient, on_delete = models.SET_NULL, null = True, related_name = 'names')
	name = models.CharField(max_length = MAX_NAME_LEN, unique = True)
	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length = MAX_NAME_LEN, unique = True)
	products = models.ManyToManyField(to = Product, symmetrical = True, related_name = 'tags', blank = True)
	def by_name(name):
		if len(Tag.objects.filter(name = name.lower())) == 0:
			tag = Tag()
			tag.name = name.lower()
			tag.save()
			return tag
		else:
			return Tag.objects.get(name = name.lower())

class IngredientTagDict(models.Model):
	ingredient = models.OneToOneField(to = Ingredient, on_delete = models.CASCADE, related_name = "tag_stats")

class IngredientTagEntry(models.Model):
	upper = models.ForeignKey(to = IngredientTagDict, on_delete = models.CASCADE)
	refreshed = models.DateTimeField(auto_now_add = True)
	tag = models.ForeignKey(to = Tag, on_delete = models.CASCADE)
	total = models.IntegerField(default = -1)
	matches = models.IntegerField(default = -1)
	def save(self, *args, **kwargs):
		self.refresh()
		super(IngredientTagEntry, self).save(*args, **kwargs)
	def refresh(self):
		now = datetime.now()
		if self.total == -1:
			print('first time!')
		else:
			print(self.refreshed, self.total)
			delta = now - self.refreshed
			if delta.days < 3:
				return
		self.refreshed = now
		all = self.tag.products.all()
		matches = self.upper.ingredient.in_products.filter(tags = self.tag)
		self.total = len(all)
		self.matches = len(matches)