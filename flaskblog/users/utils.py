import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_login import current_user
from flaskblog import mail

def save_picture(form_picure):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picure.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profilepics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picure)
    i.thumbnail(output_size)
    prev_picture = os.path.join(current_app.root_path, 'static/profilepics', current_user.img_file)
    if os.path.exists(prev_picture) and  os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
'''
    mail.send(msg)