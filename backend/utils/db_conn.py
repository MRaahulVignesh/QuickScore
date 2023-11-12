
# Create a SQLite database
engine = create_engine('sqlite:///exam_management.db')

# Create tables based on the defined models
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()