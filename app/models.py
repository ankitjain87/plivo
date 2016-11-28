from app import db


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(40))
    username = db.Column(db.String(30))


class PhoneNumber(db.Model):
    __tablename__ = "phone_number"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(40))
    account_id = db.Column(
        db.Integer, db.ForeignKey('account.id'))
    account = db.relationship(
        "Account", backref=db.backref("phone_number", uselist=False))
