from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from customerapp.models import Customer
from sellerapp.models import seller
from .models import product,user,categories
import random
from .utils import *

def login(request):
    if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])
        if uid.role == "seller":
                    sid = seller.objects.get(user_id=uid)
                    context = {
                        "uid" : uid,
                        "sid" : sid,
                        'totalproducts' : product.objects.count(),
                        'totalcategories': categories.objects.count()
                    }
                    return render(request,"sellerapp/index.html",context)
        elif uid.role == "customer":
                    return redirect("userpanel")
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']
            try:
                uid = user.objects.get(email=email)
                if uid.password != password:
                    return render(request,"sellerapp/login.html",{"msg":"invalid password"})
                request.session['email'] = email
                if uid.role == "seller":
                        return redirect("index")
                if uid.role == "customer":
                        return redirect("userpanel")
            except Exception as e:
                print("ERROR:", e)
        return render(request,"sellerapp/login.html")
    
def userpanel(request):
    print("this is userpanel")
    uid = user.objects.get(email=request.session['email'])
    print(uid)
    print(uid.role)
    sid = Customer.objects.filter(user_id=uid).first()
    print(sid)
    products = product.objects.all()
    categories_data = categories.objects.all()
    context = {
        "uid": uid,
        "sid": sid,
        'products': products,
        "categories" : categories_data
    }
    return render(request, "sellerapp/userpanel.html", context)

def index(request):
     uid = user.objects.get(email = request.session['email'])
     sid = seller.objects.get(user_id = uid)
     context = {
          "uid" : uid,
          "sid" : sid
     }
     return render(request,"sellerapp/index.html",context)

def register(request):
    if request.POST:
        role = request.POST['role']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        contactno = request.POST['contactno']

        l1 = ["tu598","njk53","mnkj67","fef23","fws78","tdy732"]

        password = random.choice(l1) + email[3:7] + contactno[3:6]

        uid = user.objects.create(
            role = role,
            email = email,
            password = password
        )

        if role == "seller":
            seller.objects.create(
            user_id = uid,
            firstname = firstname,
            lastname = lastname,
            contactno = contactno
        )
            

        elif role == "customer":
            Customer.objects.create(
            user_id = uid,
            firstname = firstname,
            lastname = lastname,
            contactno = contactno
            )
        context = {
            's_msg' : "successfully registration completed - please check your mail for password"
        }
        return render(request,"sellerapp/login.html",context)
    else:
        return render(request,"sellerapp/register.html")

def logout(request):
     if "email" in request.session:
          del request.session['email']
          return HttpResponseRedirect('/sellerapp/login')
     else:
           return HttpResponseRedirect('/sellerapp/login')

def update_profile(request):
    if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])

        if uid.role == "seller":
                    sid = seller.objects.get(user_id=uid)
                    firstname = request.POST['firstname']
                    lastname = request.POST['lastname']
                    contactno = request.POST['contactno']
                    seller_stock_name = request.POST['seller_stock_name']


                    sid.firstname = firstname
                    sid.lastname = lastname
                    sid.contactno = contactno
                    sid.seller_stock_name = seller_stock_name

                    if "picture" in request.FILES:
                        sid.picture = request.FILES['picture']

                        sid.save()

                    sid.save()

                    context = {
                        "uid" : uid,
                        "sid" : sid
                    }
                    return render(request,"sellerapp/index.html",context)
        return HttpResponseRedirect("/sellerapp/login")
    else:
         return HttpResponseRedirect("/sellerapp/login")
 
def add_product(request):
    if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])

    if uid.role == "seller":
        sid = seller.objects.get(user_id=uid)
        pid = product.objects.create(
              user_id = uid,
              product_name = request.POST['product_name'],
              product_category = request.POST['product_category'],
              product_price = request.POST['product_price'],
              stock_qty = request.POST['stock_qty'],
              picture = request.FILES['picture'],
              description = request.POST['description'],
              discount = request.POST['discount'],
              badge_text = request.POST['badge_text'],
              weight_unit = request.POST['weight_unit'],
              brand = request.POST['brand']
            )
        print("Product Saved")
        print(pid.id)
        print(pid.user_id)
         
        context = {
                        "uid" : uid,
                        "sid" : sid,
                        "pid" : pid
                        }
        return redirect('/sellerapp/view-products')

def view_products(request):
    if "email" in request.session:
        uid = user.objects.get(email=request.session['email'])
        print("Current User ID:", uid.id)
        print("Current User:", uid.email)
        sid = seller.objects.get(user_id=uid)
        products = product.objects.filter(user_id = uid)
        print("Products Count:", products.count())
        context = {
            'products': products,
            'sid': sid,
            'uid': uid,
        }
        return render(request, 'sellerapp/view_products.html',context)
    return HttpResponseRedirect('/sellerapp/login')

def add_category(request):
    if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])
        sid = seller.objects.get(user_id=uid)
        if uid.role == "seller":
            if request.method == "POST":
                cid = categories.objects.create(
                    user_id = uid,
                    categories_name = request.POST['categories_name'],
                    category_picture = request.FILES['category_picture'],
                    description = request.POST['description']
                    )
                
                context = {
                                "uid" : uid,
                                "sid" : sid,
                                "cid" : cid
                                }
                return redirect('/sellerapp/view_categories/')
        return render(request, "sellerapp/add_category.html", {"uid": uid, "sid": sid})

def view_categories(request):
    if "email" in request.session:
        uid = user.objects.get(email=request.session['email'])
        sid = seller.objects.get(user_id=uid)
        all_categories = categories.objects.all()
        context = {
            'categories': all_categories,
            'sid': sid,
            'uid': uid,
        }
        return render(request, 'sellerapp/view_categories.html',context)
    return HttpResponseRedirect('/sellerapp/login')

def product_details(request, pid):
    if "email" in request.session:
        uid = user.objects.get(email=request.session['email'])
        sid = seller.objects.get(user_id=uid)
        p = product.objects.get(id=pid)
    context = {
        "p": p,
        "uid" : uid,
        "sid" : sid
    }
    return render(request, "sellerapp/product_details.html", context)

def edit_product(request, pid):
    p = product.objects.get(id=pid)
    if request.method == "POST":
        p.product_name = request.POST['product_name']
        p.product_category = request.POST['product_category']
        p.product_price = request.POST['product_price']
        p.stock_qty = request.POST['stock_qty']
        p.discount = request.POST['discount']
        p.badge_text = request.POST['badge_text']
        p.weight_unit = request.POST['weight_unit']
        p.brand = request.POST['brand']
        p.description = request.POST['description']

        if 'picture' in request.FILES:
            p.picture = request.FILES['picture']

        p.save()

        return HttpResponseRedirect("/sellerapp/view-products/")
    context = {
        "p": p
    }
    return render(request,"sellerapp/edit_products.html",context)

def delete_product(request,pid):
     p = product.objects.get(id=pid)
     p.delete()
     p = product.objects.all()
     return redirect('/sellerapp/view-products')


def edit_profile(request):
    if "email" in request.session:
        uid = user.objects.get(email = request.session['email'])

        if uid.role == "customer":
            sid = Customer.objects.get(user_id=uid)
            if request.method == "POST":
                sid.firstname = request.POST['firstname']
                sid.lastname = request.POST['lastname']
                sid.contactno = request.POST['contactno']
                sid.address = request.POST['address']

                if "picture" in request.FILES:
                    sid.picture = request.FILES['picture']
                sid.save()

                return HttpResponseRedirect("/sellerapp/userpanel/")
                
        return HttpResponseRedirect("/sellerapp/userpanel/")
    return HttpResponseRedirect("/sellerapp/login")
     
def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        try:
          uid = user.objects.get(email=email)
          otp = random.randint(1111,9999)
          uid.otp = otp
          uid.save()
          myCustomMail("Forgot Password", "mailtemplete", email , {"otp": otp})
          if uid:
                context = {
                    "email" : email
                }
                return render(request,"sellerapp/reset_password.html",context)
        except:
             context = {
                  "e_msg" : "user does not Exists"
             }
             return render(request,"sellerapp/forgot_password.html",context)
    else:
     return render(request,"sellerapp/forgot_password.html")

def reset_password(request):
    if request.POST:
          email = request.POST['email']
          otp = request.POST['otp']
          newpassword = request.POST['newpassword']
          conpassword = request.POST['conpassword']

          uid = user.objects.get(email=email)

          if otp == str(uid.otp) and newpassword == conpassword:
               uid.password = newpassword
               uid.save()
               context = {
                    "user" : "user does not exists"
                  }
               return render(request,"sellerapp/login.html",context)
    else:         
        return render(request,"sellerapp/login.html")

def edit_category(request,cid):
    if "email" in request.session:
        uid = user.objects.get(email=request.session['email'])
        sid = seller.objects.get(user_id=uid)
        cat = categories.objects.get(id=cid)

        if request.POST:
            cat.categories_name = request.POST['categories_name']
            if 'category_picture' in request.FILES:
                cat.category_picture = request.FILES['category_picture']
            cat.description = request.POST['description']

            cat.save()

            return HttpResponseRedirect("/sellerapp/view_categories/")

        context = {
            'uid' : uid,
            'sid' : sid, 
            'cat' : cat
        }
        return render(request,"sellerapp/edit_category.html",context)

def delete_category(request,cid):
     cat = categories.objects.get(id=cid)
     cat.delete()
     cat = product.objects.all()
     return redirect('/sellerapp/view_categories')

def updated(request,pid):
    uid = user.objects.get(email=request.session['email'])
    sid = Customer.objects.get(user_id=uid)

    p = product.objects.get(id=pid)

    context = {
        "uid": uid,
        "sid": sid,
        "p": p
    }
    return  render(request,"sellerapp/updated.html",context)

def categories_product(request):
     uid = user.objects.get(email = request.session['email'])
     sid = Customer.objects.filter(user_id=uid).first()
     context = {
          "sid" : sid
     }
     return render(request,"sellerapp/categories_product.html",context)

def cart(request):
    uid = user.objects.get(email = request.session['email'])
    sid = Customer.objects.filter(user_id=uid).first()

    cart_item = Cart.objects.filter(customer = sid)
    if cart_item:
        cart = Cart.objects.get(customer=sid)
        items = Cartitem.objects.filter(cart=cart)

        sub_total = 0
        for i in items:
            sub_total += i.Product.product_price * i.qty
        
        

        context = {
            "items" : items,
            "sid" : sid,
            "sub_total" : sub_total,
            "total" : sub_total-25
        }
        return render(request,"sellerapp/cart.html",context)
    else:
        context = {
            "items" : items,
            "sid" : sid,
            "sub_total" : sub_total,
            "total" : sub_total-25
        }
        return render(request,"sellerapp/cart.html",context)

def add_to_cart(request,pk):
     uid = user.objects.get(email = request.session['email'])
     if uid.role == "customer":
        cid = Customer.objects.get(user_id = uid)

        Product = product.objects.get(id = pk)

        cart,is_created = Cart.objects.get_or_create(customer = cid)

        cartitemdata,is_created = Cartitem.objects.get_or_create(cart=cart,Product=Product)

        print("cartitem data",cartitemdata)
        print("status",is_created)

        if not is_created:
            cartitemdata.qty += 1
            cartitemdata.save()
        
        return redirect('userpanel')
    
def checkout(request):
     uid = user.objects.get(email = request.session['email'])
     cid = Customer.objects.get(user_id = uid)

     cart = Cart.objects.get(customer=cid)

     Cartitem.objects.filter(cart=cart).delete()

     return redirect('cart')
     



