from flask import*
from database import*
from public import public
from admin import admin
from shop import shop
from user import user



app=Flask(__name__)
app.secret_key="shop"

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(shop)
app.register_blueprint(user)




app.run(debug=True,port=5019,host="0.0.0.0")