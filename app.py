from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db  = SQLAlchemy(app)

class User(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String, nullable=False)
    email   = db.Column(db.String, unique=True, nullable=False)

    def as_dict(self):  
        dictionary =  {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        return dictionary

@app.route("/")
def hello_world():
    return '<p>Welcome to my User API</p>'

@app.route("/user_create")
def user_create():
    print('user_create')
    
    name  = request.args.get('name', None)
    email = request.args.get('email', None)

    print('name: ', name)
    print('email: ', email)    
    
    if name == None:
        return {'error': 'name is required'}
    
    if email == None:
        return {'error': 'email is required'}
    
    email   = email.lower().replace(' ', '')
    user    = db.session.query(User).filter(User.email==email).first()
    if user != None:
        return {'error': f'User with email: {email} already exists'}
    
    query = User()
    query.name = name
    query.email = email 
    db.session.add(query)
    db.session.commit()
    
    return {'success': f'User {name} created'}


    

@app.route("/user_update")
def user_update():
    pass

@app.route("/user_review")
def user_review():
    pass

@app.route("/user_delete")
def user_delete():
    pass


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
