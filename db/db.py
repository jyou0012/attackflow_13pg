from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create engine
engine = create_engine("sqlite:///dataBase.db", echo=True)

# Create base class
Base = declarative_base()

# Define User class
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)
    
    # Relationship to files
    files = relationship("File", back_populates="user")

# Define File class
class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String)
    content = Column(LargeBinary)
    
    # Relationship to user
    user = relationship("User", back_populates="files")

# Define WebsiteInfo class
class WebsiteInfo(Base):
    __tablename__ = 'website_info'
    
    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary)
    description = Column(Text)

# Initialize database
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Add initial user, file, and website info
def init_data():
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create user
    user = User(username="admin", password="123", role="admin")
    
    # Create file
    file = File(filename="example.txt", content=b"This is an example file.")
    
    # Link file to user
    file.user = user
    
    # Create website info
    website_info = WebsiteInfo(image=b"Some image data", description="This is a sample website description.")
    
    # Add user, file, and website info to session and commit
    session.add(user)
    session.add(file)
    session.add(website_info)
    session.commit()
    
    # Close session
    session.close()

# Create tables and add initial data
if __name__ == "__main__":
    init_db()
    init_data()
