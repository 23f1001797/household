from flask import render_template, redirect, url_for, flask
from app import app
from models import db, Customer, Professional, User, Service, Service_request, Review
from sqlalchemy.orm import joinedload
from functools import wraps
from sqlalchemy import or_, func, and_
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from utils import allowed_file, get_upload_folder
from forms import Loginform, Adminprofileform, Passwordeditform, Customerregistrationform, Professionalregistrationform, Editprofileform, Editserviceform, Reviewform, Customerfilterform, Addserviceform
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import os
from datetime import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@app.context_processor
def inject_forms():
    admin_profile_form = Adminprofileform()
    user_profile_form = Editprofileform()
    edit_password_form = Passwordeditform()
    add_service_form = Addserviceform()
    edit_service_form = Editserviceform()
    review_form = Reviewform()
    customer_filter_form = Customerfilterform()
    
                                                                                          