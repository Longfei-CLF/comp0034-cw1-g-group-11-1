
# from threading import Thread
#
# from flask_mail import Message
# from flask import current_app
#
# from volcano_stats_flask import mail
#
#
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_password_reset_email(user):
#     """
#     Resent the request email
#     """
#     token = user.get_jwt_token()
#     send_email('please reset your password',
#                sender=current_app.config['MAIL_USERNAME'],
#                recipients=[user.email],
#                text_body=render_template('email/reset_password.txt', user=user, token=token),
#                html_body=render_template('email/reset_password.html', user=user, token=token))







