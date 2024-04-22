from flask import*
from database import*
import uuid
import qrcode


public=Blueprint('public',__name__)


@public.route('/')
def home():
    return render_template('publichome.html')


@public.route('/login',methods=['get','post'])
def login():
    if'login'in request.form:
        uname=request.form['uname']
        password=request.form['pass']
        
        qry="select * from login where username='%s' and password='%s'"%(uname,password)
        res=select(qry)
        if res:
            session['log']=res[0]['login_id']
            
            if res[0]['usertype']=='admin':
                return ("<script>alert('welcome admin');window.location='/adminhome'</script>")
            elif res[0]['usertype']=='shop':
                qry2="select * from shops where login_id='%s'"%(session['log'])
                res2=select(qry2)
                if res2:
                    session['shop']=res2[0]['shop_id']
                    session['shopname']=res2[0]['shop_name']
                return ("<script>alert('welcome shop...');window.location='/shophome'</script>")
            elif res[0]['usertype']=='user':
                qry3="select * from users where login_id='%s'"%(session['log'])
                res3=select(qry3)
                if res3:
                    session['user']=res3[0]['user_id']
                return ("<script>alert('welcome user...');window.location='/userhome'</script>")

                
                

        
    return render_template("login.html")

@public.route('/reg',methods=['get','post'])
def reg():
    if 'register'in request.form:
        shopname=request.form['shop']
        place=request.form['place']
        landmark=request.form['land']
        phone=request.form['phone']
        email=request.form['email']
      
        uname=request.form['uname']
        password=request.form['password']
        
        q="select * from login where password='%s'"%(password)
        r=select(q)
        if r:
            return ("<script>alert('Already Existing');window.location='/reg'</script>")
        else:
            qry="insert into login values(null,'%s','%s','pending')"%(uname,password)
            res=insert(qry)
            
            qry2="insert into shops values(null,'%s','%s','%s','%s','%s','%s','pending')"%(res,shopname,place,landmark,phone,email)
            res2=insert(qry2)
            return ("<script>alert('Registeration Completed ... Please wait for approval');window.location='/login'</script>")

        
        
        
    return render_template("shop_reg.html")


import bcrypt
@public.route('/user_reg',methods=['get','post'])
def user_reg():
    if'register' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        hname=request.form['hname']
        place=request.form['place']
        landmark=request.form['landmark']
        pincode=request.form['pincode']
        email=request.form['email']
        uname=request.form['uname']
        password=request.form['password']
        
        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # print(hashed_password,"pppppppppppppppppppppppppp")
        
        q="select * from login where password='%s'"%(password)
        r=select(q)
        if r:
            return ("<script>alert('Already Existing');window.location='/reg'</script>")
        else:
    
            qry="insert into login values(null,'%s','%s','user')"%(uname,password)
            res=insert(qry)
            
            
            
            qry2="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(res,fname,lname,hname,place,landmark,pincode,email)
            res2=insert(qry2)
            return ("<script>alert('Registeration Completed ... ');window.location='/login'</script>")

        
    return render_template("user_reg.html") 