from app import db


class Pdf(db.Model):
    __tablename__ = 'pdf_data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact_number = db.Column(db.String(150))
    policy_number = db.Column(db.String(100))

    def __init__(self, name, contact_number, policy_number):
        self.name = name
        self.contact_number = contact_number
        self.policy_number = policy_number

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_number': self.contact_number,
            'policy_number':self.policy_number
        }
