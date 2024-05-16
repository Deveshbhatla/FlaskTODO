from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

db=SQLAlchemy(app)

class TODO(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id



@app.route('/',methods=['POST','GET'])
def index():
    #if form submitted
    if request.method=='POST':
        task_content=request.form['content']#task content is content of form
        new_task=TODO(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue adding task to the dabase"

    else:
        tasks=TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)#get the task by id, if it doesn't get it is gonna return 404
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue deleting the task'

@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    task_to_update = TODO.query.get_or_404(id)#get the task by id, if it doesn't get it is gonna return 404
    
    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating the task'

    else:
        return render_template('update.html', task=task_to_update)


if __name__=="__main__":
    app.run(debug=True)

