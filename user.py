from os import replace
from flask import*
from database import*

import bcrypt


user=Blueprint('user',__name__)


@user.route('/userhome')
def userhome():
    return render_template("userhome.html")

@user.route('/profile',methods=['get','post'])
def userprofile():
    data={}
    qry="select * from users where user_id='%s'"%(session['user'])
    res=select(qry)
    if res:
        data['view']=res
    if 'action'in request.args:
        action=request.args['action']
        
        if action=='password':
            qry1="select * from users where user_id='%s'"%(session['user'])
            res1=select(qry1)
            if res1:
                data['password']=res1
                if'submit' in request.form:
                    password=request.form['password']
                    confirmpassword=request.form['confirmpassword']
                    
                    if confirmpassword==password:
                        fixed_salt = b'$2b$12$012345678901234567890.'
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'),fixed_salt)
                        hashed_password_str = hashed_password.decode('utf-8')
                        print(hashed_password,"pppppppppppppppppppppppppp")
                        
                        qry3="update users set profile_password='%s' where user_id='%s'"%(hashed_password_str,session['user'])
                        update(qry3)
                        return ("<script>alert('SUCCESSFULLY CREATED');window.location='/profile'</script>")

                    else:
                        return ("<script>alert('PASSWORD MISMATCHING');window.location='/profile'</script>")
              
    return render_template("userprofile.html",data=data)


@user.route('/user_view_shops')
def user_view_shops():
    data={}
    qry="select * from shops inner join login using(login_id)"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("user_view_shops.html",data=data)


@user.route('/user_view_products',methods=['get','post'])
def user_view_products():
    data={}
    qry="select * from products inner join shops using(shop_id) inner join stocks using(product_id)"
    res=select(qry)
    if res:
        data['view']=res
   
        
    if'action'in request.args:
        action=request.args['action']
        id=request.args['id']
        
        if action=='quantity':
            qry1="select * from stocks inner join products using(product_id) where product_id='%s'"%(id)
            res1=select(qry1)
            if res:
                data['stock']=res1
                
                if'submit' in request.form:
                    stock=request.form['stock']
                    quantity=request.form['quantity']
                    product_id=res1[0]['product_id']
                    price=res1[0]['price']
                    shop_id=res1[0]['shop_id']
                    totalamount=int(price)*int(quantity)
                    
                    
                    if int(stock)<int(quantity):
                        return ("<script>alert('PLEASE ADD A VALID QUANTITY OR OUT OF STOCK ... ');window.location='/user_view_products'</script>")
                    else:
                        
                        qry4='select * from order_master where user_id="%s" and status="pending"'%(session['user'])
                        res2=select(qry4)
                            
                        if res2:
                            qry5="update order_master set total=(total+'%s') where user_id='%s'"%(totalamount,session['user'])
                            res1=update(qry5)
                            
                            qry3="insert into order_details values(null,'%s','%s','%s','%s')"%(res1,product_id,quantity,price)
                            insert(qry3)
                            return ("<script>alert('ADDED ... ');window.location='/cart'</script>")

                        else:
                            qry2="insert into order_master values(null,'%s','%s',curdate(),'%s','pending','pending')"%(session['user'],shop_id,totalamount)
                            res1=insert(qry2)
                            qry3="insert into order_details values(null,'%s','%s','%s','%s')"%(res1,product_id,quantity,price)
                            insert(qry3)
                            
                            return ("<script>alert('REMOVED ... ');window.location='/cart'</script>")

        
                        
        
    return render_template("user_view_products.html",data=data)


@user.route('/cart')
def cart():
    data={}
    qry="SELECT * FROM order_master INNER JOIN order_details USING(order_master_id) INNER JOIN products USING(product_id) where user_id='%s' and status='pending'"%(session['user'])
    res=select(qry)
    if res:
        data['view']=res
    else:
        return ("<script>alert('EMPTY CART... ');window.location='/user_view_products'</script>")

    if'action'in request.args:
        action=request.args['action']
        id=request.args['id']
        
        if action=='remove':
            qry2="select * from order_details where order_details_id='%s'"%(id)
            res2=select(qry2)
            amount=res2[0]['amount']
            quantity=res2[0]['quantity']
            tot=int(amount)*int(quantity)
            
            qry3="update order_master set total=(total-'%s') where order_master_id=(select order_master_id from order_details where order_details_id='%s')"%(tot,id)
            update(qry3)
            
            qry4="delete from order_details where order_details_id='%s'"%(id)
            delete(qry4)
            return ("<script>alert('REMOVED ... ');window.location='/cart'</script>")

    return render_template("user_cart.html",data=data)


@user.route('/makepayment',methods=['get','post'])
def makepayment():
    data={}
    qry="select * from order_master where user_id='%s' and shop_verified='accepted' and status='pending'"%(session['user'])
    res=select(qry)
    if res:
        data['view']=res
        session['id']=res[0]['order_master_id']
        
    if 'submit' in request.form:
        password=request.form['password']
        
        fixed_salt = b'$2b$12$012345678901234567890.'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),fixed_salt)
        hashed_password_str = hashed_password.decode('utf-8')
        print(hashed_password,"pppppppppppppppppppppppppp")
        
        qry3="select * from users where user_id='%s'"%(session['user'])
        res3=select(qry3)
        print(res3[0]['profile_password'],"pppppppppppppppppppppppppp")
        print(hashed_password_str,"oooooooooooooooooooooooooooooo")
        if res3[0]['profile_password']==hashed_password_str:
            qry4="update order_master set status='paid' where order_master_id='%s'"%(session['id'])
            res=update(qry4)
            
            
            qry5=" SELECT * FROM order_details INNER JOIN stocks USING(product_id) WHERE order_master_id='%s' "%(session['id'])
            res4=select(qry5)
            print(res4)
            if res4:
                for i in res4:
                    a=i['product_id']
                    b=i['order_qty']
                    c=i['quantity']
                    
                    
                    qry6="update stocks set quantity=(quantity-'%s') where product_id='%s'"%(b,a)
                    update(qry6)
            return ("<script>alert('PAYMENT SUCCESSFULL ... ');window.location='/userhome'</script>")
        else:
            return ("<script>alert('FAILED ... ');window.location='/makepayment'</script>")
        

            
        
    
    return render_template("makepayment.html",data=data)



@user.route('/user_complaint',methods=['get','post'])
def user_complaint():
    data={}
    qry1="select * from complaints where user_id='%s'"%(session['user'])
    res1=select(qry1)
    if res1:
        data['view']=res1
    if'submit' in request.form:
        complaint=request.form['complaint']
        
        qry="insert into complaints values(null,'%s','%s','pending',curdate())"%(session['user'],complaint)
        insert(qry)
        return ("<script>alert('COMPLAINT SEND ... ');window.location='/user_complaint'</script>")

    return render_template("user_complaint.html",data=data)


@user.route('/order_history')
def order_history():
    data={}
    qry="select * from order_details inner join order_master using(order_master_id) inner join products using(product_id) where user_id='%s'"%(session['user'])
    res=select(qry)
    data['view']=res
    return render_template("user_order_history.html",data=data)


@user.route('/rate_product',methods=['get','post'])
def rate_product():
    id=request.args['id']
    if'submit'in request.form:
        rating=request.form['rating']
        review=request.form['review']
        
        qry="insert into ratings values(null,'%s','%s','%s','%s',curdate())"%(session['user'],id,rating,review)
        insert(qry)
        return ("<script>alert('RATED ... ');window.location='/order_history'</script>")

    return render_template("rate_product.html")
    







