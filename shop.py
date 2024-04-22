from flask import*
from database import*
import uuid
import qrcode



shop=Blueprint('shop',__name__)


@shop.route('/shophome')
def shophome():
    return render_template("shophome.html")


@shop.route('/shopcategory')
def shopcategory():
    data={}
    qry2="select * from category"
    res2=select(qry2)
    if res2:
        data['view']=res2
    return render_template("shopcategory.html",data=data)
    


@shop.route('/shopmanageproducts',methods=['get','post'])
def shopmanageproducts():
    data={}
    qry2="select * from products inner join stocks using(product_id) where shop_id='%s'"%(session['shop'])
    res2=select(qry2)
    if res2:
        data['view']=res2
    
    if'submit'in request.form:
        id=request.args['id']

        pname=request.form['pname']
        details=request.form['details']
        path=request.files['image']
        img="static/product_images/"+str(uuid.uuid4())+path.filename
        path.save(img)
        price=request.form['price']
        quantity=request.form['quantity']
        
        qry="insert into products values(null,'%s','%s','%s','%s','%s','%s')"%(id,session['shop'],pname,details,price,img)
        res=insert(qry)
        
        qry6="insert into stocks values(null,'%s','%s',curdate())"%(res,quantity)
        insert(qry6)
        
        return ("<script>alert('ADDED SUCCESSFULLY');window.location='/shopmanageproducts'</script>")

        
    if 'action'in request.args:
        action=request.args['action']
        id=request.args['id']
            
        if action=='update':
            qry3="select * from products where product_id='%s'"%(id)
            res3=select(qry3)
            if res3:
                data['up']=res3
                if'update'in request.form:
                    pname=request.form['pname']
                    details=request.form['details']
                    price=request.form['price']
                    
                    
                    qry4="update products set product_name='%s',details='%s',price='%s' where product_id='%s'"%(pname,details,price,id)
                    update(qry4)
                    return ("<script>alert('UPDATE SUCCESSFULLY');window.location='/shopmanageproducts'</script>")
        if action=='delete':
            qry5="delete from products where product_id='%s'"%(id)
            delete(qry5)
        
            return ("<script>alert('DELETED SUCCESSFULLY');window.location='/shopmanageproducts'</script>")

            

                    

        
        
        
    return render_template("shopmanage_products.html",data=data)


@shop.route('/upstock',methods=['get','post'])
def upstock():
    id=request.args['id']
    if 'submit'in request.form:
        stock=request.form['stock']
        
        qry="update stocks set quantity='%s' where product_id='%s'"%(stock,id)
        res=update(qry)
        print(res,"RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
     
        # qry1="select * from stocks where product_id='%s'"%(id)
        # res2=select(qry1)
        # sid=res2[0]['stock_id']
        # print(res2,"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        # qry2="update notification set status='stocks available now' where stock_id='%s'"%(sid)
        # update(qry2)
        # # /////////////
        # qry3="select * from users"
        # res3=select(qry3)
        # for i in res3:
        #     user=i['user_id']
        #     print(user,"/////////////////////////////////////////////")
        return ("<script>alert('STOCK UPDATED SUCCESSFULLY');window.location='/shopmanageproducts'</script>")

            
            
           
        
    return render_template("shopupdate_stock.html")



@shop.route('/viewpayments')
def viewpayments():
    data={}
    qry="select * from order_master inner join users using(user_id) where shop_id='%s'"%(session['shop'])
    res=select(qry)
    if res:
        data['view']=res
    return render_template("shop_viewpayments.html",data=data)
    
    
    
@shop.route('/addoffer',methods=['get','post'])
def addoffer():
    id=request.args['id']
    
    
    if'add'in request.form:
        price=request.form['offer']
        sdate=request.form['sdate']
        edate=request.form['edate']
        
        qry="insert into offer values(null,'%s','%s','%s','%s','offerprice')"%(id,price,sdate,edate)
        insert(qry)
        return ("<script>alert('OFFER UPDATED SUCCESSFULLY');window.location='/shopmanageproducts'</script>")

    
    qry1="delete from offer where product_id='%s' and end_date=curdate()"%(id)
    delete(qry1)

    return render_template("shop_manage_offer.html")



@shop.route('/orders')
def orders():
    data={}
    qry="select * from order_master inner join users using(user_id) where shop_id='%s'"%(session['shop'])
    res=select(qry)
    if res:
        data['view']=res
    if'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        
        if action=='accept':
            qry2="update order_master set shop_verified='accepted' where order_master_id='%s'"%(id)
            update(qry2)
            return ("<script>alert('ORDER ACCEPTED');window.location='/orders'</script>")

        else:
            qry3="update order_master set shop_verified='rejected' where order_master_id='%s'"%(id)
            update(qry3)
            return ("<script>alert('ORDER REJECTED');window.location='/orders'</script>")

        
    return render_template("shop_vieworders.html",data=data)



@shop.route('/offerproducts')
def offerproducts():
    data={}
    qry="select * from offer inner join products using (product_id) where shop_id='%s'"%(session['shop'])
    res=select(qry)
    print(qry,"ppppppppppp")

    if res:
        data['view']=res
    return render_template("shop_view_offer.html",data=data) 



        

@shop.route('/view_order')
def view_order():
    data={}
    id=request.args['id']
    qry="select * from order_master inner join order_details using(order_master_id) inner join products using(product_id) where order_master_id='%s'"%(id)
    res=select(qry)
    data['view']=res
    return render_template("shop_view_order.html",data=data)


@shop.route('/view_rating')
def view_rating():
    data={}
    qry="select * from ratings inner join users using(user_id) inner join products using(product_id) where shop_id='%s'"%(session['shop'])
    res=select(qry)
    if res:
        data['view']=res
    return render_template("view_ratings.html",data=data)





