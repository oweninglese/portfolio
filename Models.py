import os
from PIL import Image
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Photo(Base):
    __tablename__: str = 'photos'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)


def upload_photos(folder_path: str, db_path: str) -> None:
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)  # create the table if it doesn't exist

    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            photo_path: str = os.path.join(folder_path, filename)

            # Resize the image and save it to a temporary file
            with Image.open(photo_path) as image:
                image.thumbnail((640, 640))
                temp_file: str = os.path.join(os.path.dirname(photo_path), f'temp_{filename}')
                image.save(temp_file)

            # Add the photo to the database
            photo = Photo(filename=filename, path=temp_file)
            session.add(photo)
            session.commit()

            # Remove the temporary file
            os.remove(temp_file)
