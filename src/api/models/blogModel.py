from api import app, db, bcrypt
import datetime


class BlogpostModel(db.Model):
    """
    Blog Model
    """
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    tags = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, content, photo, tags, owner_id):
        self.title = title
        self.description = description
        self.content = content
        self.photo = photo
        self.tags = tags
        self.created_at = datetime.datetime.now()
        self.owner_id = owner_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title, description, content, photo, tags):
        self.title = title
        self.description = description
        self.content = content
        self.photo = photo
        self.tags = tags

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogpost(self):
        return BlogpostModel.query.all()

    @staticmethod
    def get_one_blogpost(self, id):
        return BlogpostModel.query.get(id)

    def __repr__(self):
        return "<id: {}>".format(self.id)
