from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from products.models import Category, Product, Sku, Brand, Media


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    items_per_page = 20
    page_number = 1

    def get_category_products(self, parent_category):
        products = []

        def get_products_recursive(category):
            nonlocal products
            child_categories = Category.objects.filter(parent=category)

            for child_category in child_categories:
                products.extend(Product.objects.filter(category=child_category))
                get_products_recursive(child_category)

        get_products_recursive(parent_category)
        return products

    def get_page(self, paginator):
        try:
            page = paginator.get_page(self.page_number)
        except EmptyPage:
            page = paginator.get_page(1)
        except PageNotAnInteger:
            # Handle non-integer page number
            page = paginator.get_page(1)

        return page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(Category, id=self.kwargs['pk'])
        context['categories'] = Category.objects.filter(parent=parent_category)
        context['products'] = self.get_category_products(parent_category)
        paginator = Paginator(context['products'], self.items_per_page)
        context['page'] = self.get_page(paginator)
        
        return context
        
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        context['skus'] = Sku.objects.filter(product=product)
        context['media'] = Media.objects.filter(product=product)
        
        return context
