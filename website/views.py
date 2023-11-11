from flask import Flask , Blueprint , render_template , request,jsonify,flash
from .modules import User , Note
from . import db
from flask_login import current_user, login_required
import json

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method =='POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash("Note is too short!",category = 'error')
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category ='success')        
    return render_template('home.html',user=current_user)


@views.route('/delete-note' , methods = ['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    del_noteId=note['noteId']
    del_data = Note.query.get(del_noteId)
    print(del_data)
    print(type(del_data))
    
    if note:
        if del_data.user_id == current_user.id:
            db.session.delete(del_data)
            db.session.commit()
    
    return jsonify({})
    
    