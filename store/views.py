from django.shortcuts import render,get_object_or_404
from store.models import Product
from Category.models import Category
# Create your views here.


def store(request,category_slug=None):


    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        all_product=Product.objects.all().filter(is_available=True,category=categories)
        # print(products,'***********')
        # print(categories,'***************')

        count=all_product.count()

    else:    

       all_product=Product.objects.all().filter(is_available=True)
       count=all_product.count()
    context={
        'all_products':all_product,
        'count':count
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
       


    except Exception as e:
    
        raise e;


    context={
        'single_product':single_product
    }        
    return render(request,'store/product_details.html',context);    