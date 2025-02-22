from app import app, db, init_db

def create_tables():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize default data
        init_db()

if __name__ == '__main__':
    create_tables()
