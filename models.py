from extensions import db

class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    trainings = db.relationship('Training', back_populates='subject')

class Trainer(db.Model):
    __tablename__ = 'trainer'
    trainer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    trainings = db.relationship('Training', back_populates='trainer')

class Training(db.Model):
    __tablename__ = 'training'
    t_id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    date_training = db.Column(db.Date, nullable=False)
    details = db.Column(db.String(250), nullable=False)

    trainer = db.relationship('Trainer', back_populates='trainings')
    subject = db.relationship('Subject', back_populates='trainings')
