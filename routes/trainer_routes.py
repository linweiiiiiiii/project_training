from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Trainer
from extensions import db
from flask import current_app as app

trainer_bp = Blueprint('trainer', __name__)

@trainer_bp.route('/trainers')
def trainers():
    trainers = Trainer.query.all()
    return render_template('trainers.html', trainers=trainers)

@trainer_bp.route('/trainer/add', methods=['GET', 'POST'])
def trainer_add():
    if request.method == 'POST':
        first_name = request.form['name1'].strip()
        family_name = request.form['name2'].strip()
        
        if not first_name or not family_name:
            message = "Please enter all fields"
            message_type = "warning"
            return render_template('trainer_add.html', message=message, message_type=message_type)
        
        new_trainer = Trainer(first_name=first_name, family_name=family_name)
        db.session.add(new_trainer)
        
        try:
            db.session.commit()
            flash('Trainer Successfully Added.', 'success')
            return redirect(url_for('trainer.trainers'))
        except Exception as e:
            db.session.rollback()
            message = str(e)
            message_type = "danger"
            return render_template('trainer_add.html', message=message, message_type=message_type)
    
    return render_template('trainer_add.html')

@trainer_bp.route('/trainer/edit/<int:id>', methods=['GET', 'POST'])
def trainer_edit(id):
    trainer = Trainer.query.get_or_404(id)
    
    if request.method == 'POST':
        first_name = request.form['FirstName'].strip()
        family_name = request.form['FamilyName'].strip()
        
        if not first_name or not family_name:
            message = "Please enter all fields"
            message_type = "warning"
            return render_template('trainer_edit.html', trainer=trainer, message=message, message_type=message_type)
        
        trainer.first_name = first_name
        trainer.family_name = family_name
        
        try:
            db.session.commit()
            flash('Trainer Updated', 'success')
            return redirect(url_for('trainer.trainers'))
        except Exception as e:
            db.session.rollback()
            message = "An error occurred while updating the trainer."
            message_type = "danger"
            app.logger.error(f"Error updating trainer {id}: {e}")
            return render_template('trainer_edit.html', trainer=trainer, message=message, message_type=message_type)
    
    return render_template('trainer_edit.html', trainer=trainer)

@trainer_bp.route('/trainer/delete/<int:id>', methods=['POST'])
def trainer_delete(id):
    trainer = Trainer.query.get_or_404(id)
    
    if trainer.trainings:
        flash("Trainer cannot be deleted. All of the Trainer's Trainings must be deleted first", 'warning')
        return redirect(url_for('trainer.trainers'))
    
    try:
        db.session.delete(trainer)
        db.session.commit()
        flash('Trainer Deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'danger')
    
    return redirect(url_for('trainer.trainers'))
