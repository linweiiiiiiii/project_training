from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Subject
from extensions import db

subject_bp = Blueprint('subject', __name__)

@subject_bp.route('/subjects')
def subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@subject_bp.route('/subject/add', methods=['GET', 'POST'])
def subject_add():
    if request.method == 'POST':
        subject_name = request.form['SubjectName'].strip()
        
        if not subject_name:
            message = "Please enter all fields"
            message_type = "warning"
            return render_template('subject_add.html', message=message, message_type=message_type)
        
        new_subject = Subject(name=subject_name)
        db.session.add(new_subject)
        
        try:
            
            flash('Subject Successfully Added.', 'success')
            db.session.commit()
            return redirect(url_for('subject.subjects'))
        except Exception as e:
            db.session.rollback()
            message = str(e)
            message_type = "danger"
            exec_sql = f"INSERT INTO Subject (name) VALUES ('{subject_name}')"
            return render_template('subject_add.html', message=message, message_type=message_type, exec_sql=exec_sql)
    
    return render_template('subject_add.html')

@subject_bp.route('/subject/edit/<int:id>', methods=['GET', 'POST'])
def subject_edit(id):
    subject = Subject.query.get_or_404(id)
    
    if request.method == 'POST':
        subject_name = request.form['SubjectName'].strip()
        
        if not subject_name:
            message = "Please enter all fields"
            message_type = "warning"
            return render_template('subject_edit.html', subject=subject, message=message, message_type=message_type)
        
        subject.name = subject_name
        
        try:
            db.session.commit()
            flash('Subject Updated', 'success')
            return redirect(url_for('subject.subjects'))
        except Exception as e:
            db.session.rollback()
            message = str(e)
            message_type = "danger"
            exec_sql = f"UPDATE Subject SET name = '{subject_name}' WHERE subject_id = {id}"
            return render_template('subject_edit.html', subject=subject, message=message, message_type=message_type, exec_sql=exec_sql)
    
    return render_template('subject_edit.html', subject=subject)

@subject_bp.route('/subject/delete/<int:id>', methods=['POST'])
def subject_delete(id):
    subject = Subject.query.get_or_404(id)
    
    if subject.trainings:
        flash("Subject cannot be deleted. All of the Subject's Training data must be deleted first", 'warning')
        return redirect(url_for('subject.subjects'))
    
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject Deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'danger')
    
    return redirect(url_for('subject.subjects'))