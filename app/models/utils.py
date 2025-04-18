from main import db


class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def refresh(self):
        db.session.refresh(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
