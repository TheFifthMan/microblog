from app import create_app,db
from app.models import User,Post
app = create_app('default')

@app.shell_context_processor
def shell_context_processor():
    return {'db':db,'User':user,"Post":Post}