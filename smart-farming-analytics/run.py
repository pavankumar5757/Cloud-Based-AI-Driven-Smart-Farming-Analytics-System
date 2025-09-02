 from app import create_app, db
 from data.sample_data import ensure_sample_data

 app = create_app()

 with app.app_context():
     db.create_all()
     ensure_sample_data()

 if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)
