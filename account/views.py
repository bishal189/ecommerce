from django.shortcuts import render,HttpResponse,redirect
# from .forms import Registrationform
from .forms import ResitrationForm
from.models import Account
from django.contrib import messages,auth
from cart.models import Cart,Cartitem
import requests

from django.contrib.auth.decorators import login_required

# verification email module import
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.views import _cart_id



def register(request):
    if request.method == 'POST':
        form =ResitrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']  
            last_name=form.cleaned_data['last_name']  
            phone_number=form.cleaned_data['phone_number']  
            email=form.cleaned_data['email']  
            password=form.cleaned_data['password']  
            username=email.split("@")[0]

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password )
            user.phone_number=phone_number
            user.save()




            # user activation
            current_site=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verfication_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()







            
            messages.success(request,'Registration successful')
            return redirect('register')




    else:
       form=ResitrationForm()
    context={ 
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']


        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
               
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=Cartitem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item=Cartitem.objects.filter(cart=cart)
                    

                    # getting the product variations by cart id



                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))


                    
                    cart_item=Cartitem.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=Cartitem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cart_item=Cartitem.objects.filter(cart=cart)

                            for item in cart_item:
                                item.user=user
                                item.save()







            except:
                print('entering into the expect block ')
                pass    
            auth.login(request,user)
            # messages.success(request,'Your are now logged in.')
            url=request.META.get('HTTP_REFERER')
            
            try: 
                query=requests.utils.urlparse(url).query
                print('query->',query)
                params=dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
                
            except:
                return redirect('dashboard')
                 
            
            

        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')



    return render(request,'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out!')
    return redirect('login')





def activate(request):
    return




def dashboard(request):
    return render(request,'store/dashboard.html')