from flask import Blueprint, render_template
from models import Training, Trainer
from sqlalchemy import func
from extensions import db

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/summaries')
def summaries():
    summary_data = db.session.query(
        Trainer.first_name,
        Trainer.family_name,
        Trainer.trainer_id.label('tr_id'),
        func.count(Training.t_id).label('frequency')
    ).join(Training).group_by(Trainer.trainer_id, Trainer.first_name, Trainer.family_name).all()

    training_sessions = 1  

    return render_template('summaries.html', summary_data=summary_data, training_sessions=training_sessions)