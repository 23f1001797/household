from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash 

db = SQLAlchemy(app) 

service_request_association = db.Table('service_request_association', 
                                       db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
                                       db.Column('service_id', db.Interger, db.ForeignKey('service.id'), primary_key=True),
                                       db.Column('request_date', db.DateTime , default=datetime.utcnow, nullable=False),
                                       db.Column('professional_id', db.Integer, db.ForeignKey('professional.id'), nullable=True),
                                       db.Column('status', db.Enum('requested', 'assigned', 'closed', 'reviewed', name='request_status'), nullable=False)
                                       )

class User(db.Model, UserMixin): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    passhash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    blocked = db.Column(db.Boolean, default=False) 
    active = db.Column(db.Boolean, default=False)
    customer_profile = db.relationship('Customer', backref='user', uselist=False)
    professional_profile = db.relationship('Professional', backref='user', uselist=False)

    def set_password(self, password):
        self.passhash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.passhash, password)
    
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    contact = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    services = db.relationship('Service', secondary=service_request_association, backref='customers')

    def is_blocked(self):
        active_services = db.query(Service_request.id).filter(
            Service_request.customer_id == self.id,
            Service_request.service_status.in_(['assigned', 'requested', 'closed'])
        ).count()
        if active_services == 0:
            self.user.active = False
            db.session.commit()
        return self.user.blocked
    
    def active_service_requests(self):
        return db.query(Service_request.id).filter(
            Service_request.customer_id == self.id,
            Service_request.service_status.in_(['assigned', 'requested', 'closed'])
        ).all()
    

class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    contact = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    registration_date = db.Column(db.Datetime, default=datetime.utcnow, nullable=False)
    attachment = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)

    def is_blocked(self):
        return self.user.blocked
    
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    created = db.Column(db.Datetime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_services(self):
        return Service.query.filter_by(deleted=False).all()
    
    def is_active(self):
        return db.session.query(Service_request.id).filter(
            Service_request.service_id == self.id,
            Service_request.service_status.in_(['requested', 'assigned', 'closed'])
        ).count() > 0
    

class Service_request(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    request_date = db.Column(db.Datetime, default=datetime.utcnow, nullable=False)
    completion_date = db.Column(db.Column(db.Datetime, nullable=True))
    service_status = db.Column(db.Enum('requested', 'assigned', 'closed', 'reviewed', name='service_status'), nullable=False)
    service = db.relationship('Service', backref='requests')
    customer = db.relationship('Customer', backref='requests')
    professional = db.relationship('Professional', backref='requests')

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForiegnKey('service_request.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=False)
    service_request = db.relationship('ServiceRequest', backref='reviews')
    customer = db.relationship('Customer', backref='reviews')




with app.app_context():
    db.create_all()

    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User.query.filter_by(username='admin', email='admin@gmail.com', role='admin')
        admin.set_password('adminadmin')
        db.session.add(admin)
        db.session.commit()