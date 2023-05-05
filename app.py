from typing import Any
import config
from flask import Flask, g
from flask import render_template
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Models import Photo, upload_photos


Config: dict[str, str] = config.config

app = Flask(__name__, template_folder='templates')  # type: Flask
engine = create_engine('sqlite:///resume.db')  # type: Any
Session = sessionmaker(bind=engine)
session = Session()  # type: Any


Base = declarative_base()  # type: Any


class Resume(Base):
    """
    This is a SQLAlchemy model for a table called "resume".
    It has four columns: id, name, email, and skills.
    The id column is the primary key.
    The __repr__ method is defined to return a string representation
    of the object.
    """

    __tablename__: str = 'resume'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    skills = Column(String)

    def __repr__(self) -> str:
        return f"Resume(name={self.name}, email={self.email}, skills={self.skills})"


me = Resume(name=Config['name'], email=Config['email'], skills=Config['skills'])
Base.metadata.create_all(engine)
session.add(me)
session.commit()
upload_photos('/home/ofoo/dev/sites/res/static/img/', '/home/ofoo/dev/sites/res/resume.db')


@app.before_request
def before_request() -> None:
    g.session = Session()


@app.after_request
def after_request(response):
    g.session.close()
    return response


@app.route('/gallery')
def gallery() -> str:
    photos = g.session.query(Photo).limit(40).all()
    return render_template('gallery.html', photos=photos)


@app.route("/")
def index() -> str:
    """
    This code defines a function called `index`.
    that returns a string. The function queries a database using SQLAlchemy's `session` object to retrieve all resumes,
    and then renders an HTML template called `index.html` with the retrieved
    resumes.
    """
    res: list[Any] = g.session.query(Resume).all()
    return render_template('index.html', resumes=res)


if __name__ == '__main__':
    app.run(debug=True)
