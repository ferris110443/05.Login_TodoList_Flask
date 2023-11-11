import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from os import path
from psycopg2 import OperationalError
from flask_login import LoginManager



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
DB_NAME ="database"


def create_database():
    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    pwd = '123'
    port_id = 5432
    conn = None
    
    try:
        # Connect to PostgreSQL without starting a transaction
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id,
        )
        conn.autocommit = True  # Ensure we are not within a transaction
        # Check if the database already exists
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        database_exists = cursor.fetchone()

        if not database_exists:
            # Create the database
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
        cursor.close()
        conn.close()
    except OperationalError as e:
        print(e)

create_database()



def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:123@localhost:5432/{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')

    from .modules import User
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
