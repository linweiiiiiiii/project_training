from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Training, Subject, Trainer
from extensions import db
from datetime import datetime

training_bp = Blueprint('training', __name__)

@training_bp.route('/trainings')
def trainings():
    trainings = Training.query.all()
    now = datetime.now()
    return render_template('trainings.html', trainings=trainings, now=now)

@training_bp.route('/training/add', methods=['GET', 'POST'])
def training_add():
    if request.method == 'POST':
        subject_id = request.form['Subject']
        trainer_id = request.form['Trainer']
        details = request.form['Details'].strip()
        training_date = request.form['TrainingDate']
        
        if not all([subject_id, trainer_id, details, training_date]):
            message = "Please enter all fields"
            message_type = "warning"
            subjects = Subject.query.all()
            trainers = Trainer.query.all()
            return render_template('training_add.html', message=message, message_type=message_type, subjects=subjects, trainers=trainers)
        
        new_training = Training(subject_id=subject_id, trainer_id=trainer_id, details=details, date_training=training_date)
        db.session.add(new_training)
        
        try:
            db.session.commit()
            flash('Training Successfully Added.', 'success')
            return redirect(url_for('training.trainings'))
        except Exception as e:
            db.session.rollback()
            message = str(e)
            message_type = "danger"
            exec_sql = f"INSERT INTO Training (subject_id, trainer_id, details, date_training) VALUES ('{subject_id}', '{trainer_id}', '{details}', '{training_date}')"
            subjects = Subject.query.all()
            trainers = Trainer.query.all()
            return render_template('training_add.html', message=message, message_type=message_type, exec_sql=exec_sql, subjects=subjects, trainers=trainers)
    
    subjects = Subject.query.all()
    trainers = Trainer.query.all()
    return render_template('training_add.html', subjects=subjects, trainers=trainers)

@training_bp.route('/training/edit/<int:id>', methods=['GET', 'POST'])
def training_edit(id):
    training = Training.query.get_or_404(id)
    
    if request.method == 'POST':
        subject_id = request.form['SubjectId']
        trainer_id = request.form['MId']  
        details = request.form['Details'].strip()
        training_date = request.form['dateTraining']
        
        if not all([subject_id, trainer_id, details, training_date]):
            message = "Please enter all fields"
            message_type = "warning"
            subjects = Subject.query.all()
            trainers = Trainer.query.all()
            return render_template('training_edit.html', training=training, message=message, message_type=message_type, subjects=subjects, trainers=trainers)
        
        training.subject_id = subject_id
        training.trainer_id = trainer_id
        training.details = details
        training.date_training = training_date
        
        try:
            db.session.commit()
            flash('Training Updated', 'success')
            return redirect(url_for('training.trainings'))
        except Exception as e:
            db.session.rollback()
            message = str(e)
            message_type = "danger"
            exec_sql = f"UPDATE Training SET subject_id = '{subject_id}', trainer_id = '{trainer_id}', details = '{details}', date_training = '{training_date}' WHERE t_id = {id}"
            subjects = Subject.query.all()
            trainers = Trainer.query.all()
            return render_template('training_edit.html', training=training, message=message, message_type=message_type, exec_sql=exec_sql, subjects=subjects, trainers=trainers)
    
    subjects = Subject.query.all()
    trainers = Trainer.query.all()
    return render_template('training_edit.html', training=training, subjects=subjects, trainers=trainers)

@training_bp.route('/training/delete/<int:id>', methods=['GET'])
def training_delete(id):

    return redirect(url_for('training.trainings'))

    training = Training.query.get_or_404(id)
    
    try:
        db.session.delete(training)
        db.session.commit()
        flash('Training Deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'danger')
    
    return redirect(url_for('training.trainings'))