from flask import*
from database import*

admin=Blueprint('admin',__name__)


@admin.route('/adminhome')
def adminhome():
    return render_template("adminhome.html")



@admin.route('/adminverifyshops')
def adminverifyshops():
    data={}
    qry="select * from shops inner join login using(login_id)"
    res=select(qry)
    if res:
        data['view']=res
        if'action'in request.args:
            action=request.args['action']
            id=request.args['id']
            
            if action=='accept':
                qry2="update login set usertype='shop' where login_id='%s'"%(id)
                update(qry2)
                qry5="update shops set status='verified' where login_id='%s'"%(id)
                update(qry5)
                return ("<script>alert('Verified');window.location='/adminverifyshops'</script>")

                
            if action=='reject':
                qry3="delete from shops where login_id='%s'"%(id)
                delete(qry3)
                qry4="delete from login where login_id='%s'"%(id)
                delete(qry4)
                return ("<script>alert('Rejected');window.location='/adminverifyshops'</script>")

    return render_template("adminverify_shop.html",data=data)




@admin.route('/adminmanagecategory',methods=['get','post'])
def adminmanagecategory():
    data={}
    qry2="select * from category"
    res2=select(qry2)
    if res2:
        data['view']=res2
    
    if'sub'in request.form:
        cat=request.form['cat']
        
        qry="insert into category values(null,'%s')"%(cat)
        insert(qry)
        return ("<script>alert('ADDED SUCCESSFULLY');window.location='/adminmanagecategory'</script>")

        
    if 'action'in request.args:
        action=request.args['action']
        id=request.args['id']
        
        if action=='update':
            qry2="select * from category where category_id='%s'"%(id)
            res2=select(qry2)
            if res2:
                data['up']=res2
                
                if'up'in request.form:
                    cat=request.form['cat']
                    
                    qry3="update category set category_name='%s' where category_id='%s'"%(cat,id)
                    update(qry3)
                    return ("<script>alert('UPDATE SUCCESSFULLY');window.location='/adminmanagecategory'</script>")

        if action=='delete':
            qry4="delete from category where category_id='%s'"%(id)
            delete(qry4)
            return ("<script>alert('DELETED SUCCESSFULLY');window.location='/adminmanagecategory'</script>")


                        
                    
    return render_template("adminmanage_category.html",data=data)



@admin.route('/viewproducts',methods=['get','post'])
def viewproducts():
    data={}
    qry="select * from products inner join stocks using(product_id)"
    res=select(qry)
    if res:
        data['view']=res
        
    return render_template("adminviewproducts.html",data=data)


@admin.route('/viewcustomers')
def viewcustomers():
    data={}
    qry="select * from users"
    res=select(qry)
    if res:
        data['view']=res
    return render_template("adminviewusers.html",data=data)


@admin.route('/complaints',methods=['get','post'])
def complaints():
    data={}
    qry="select * from complaints inner join users using(user_id)"
    res=select(qry)
    if res:
        data['view']=res
        
        if'action'in request.args:
            action=request.args['action']
            id=request.args['id']
            
            if action=='reply':
                qry1="select * from complaints where complaint_id='%s'"%(id)
                res1=select(qry1)
                if res1:
                    data['up']=res1
                    
                    if'submit'in request.form:
                        reply=request.form['reply']
                        qry2="update complaints set reply='%s' where complaint_id='%s'"%(reply,id)
                        update(qry2)
                        return ("<script>alert('SEND SUCCESSFULLY');window.location='/complaints'</script>")

                        
    return render_template("adminviewcomplaints.html",data=data)
    