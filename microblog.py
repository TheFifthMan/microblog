from app import app,db
from app.models import User,Post

@app.shell_context_processor
def shell_context_processor():
    return {'db':db,'User':user,"Post":Post}