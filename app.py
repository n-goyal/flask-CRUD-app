from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ngoya:test123@localhost:5432/todoDB'
db = SQLAlchemy(app)

# migrate - bootstrp database migrate commands
migrate = Migrate(app, db)

# commit changes before migrate
db.create_all()

# Parent Model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False,
    default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)


    def __repr__(self):
        return 'Todo {0} {1}'.format(self.id, self.description)

# Child Model
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)






# db.create_all() # Now using migrate

# controller - post request listener
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # description = request.form.get('description', '')
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        # Instructions for model
        todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        # updates the view
        # return redirect(url_for('index'))
    except: 
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)
        # return redirect(url_for('index'))

# controller for update
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

#controller for delete
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_item(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})

# controller
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template('index.html',
  lists=TodoList.query.all(),
  active_list=TodoList.query.get(list_id),
  todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
)

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))

if __name__ == "__main__":
    app.run(host='0.0.0.0')