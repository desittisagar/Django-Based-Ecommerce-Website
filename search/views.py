from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# from django.db.models import Q

# Create your views here.
class SearchProductView(ListView):
	#queryset = Product.objects.all()
	template_name = "search/list.html"

	def get_context_data(self, *args,**kwargs):
		context = super(SearchProductView,self).get_context_data(*args,**kwargs)
		context['query'] = self.request.GET.get('q')
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		print(request.GET)
		query = request.GET.get('q',None) # request.GET.get('q',default_value)
		print(query)
		if query is not None:
			return Product.objects.search(query)
		else:
			return Product.objects.featured()	