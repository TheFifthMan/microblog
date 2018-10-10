from app import db,create_app
from app.models import User,Post
app = create_app()

@app.shell_context_processor
def shell_context_processor():
    return {'db':db,'User':user,"Post":Post}