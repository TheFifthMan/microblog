from app.errors import errors_bp
from flask import render_template


@errors_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404


@errors_bp.app_errorhandler(500)
def server_down(error):
    return render_template('error/500.html'),500