from app import create_app,db
app = create_app('default')

from app.models import User,Post
@app.shell_context_processor
def shell_context_processor():
    return {'db':db,'User':user,"Post":Post}