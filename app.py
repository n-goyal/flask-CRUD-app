from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ngoya:test123@localhost:5432/todoDB'
db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return 'Todo {0} {1}'.format(self.id, self.description)

db.create_all()

# controller - post request listener
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    try:
        # description = request.form.get('description', '')
        description = request.get_json()['description']
        # Instructions for model
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        # updates the view
        # return redirect(url_for('index'))
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()
    if not error:
        return jsonify({
            'description': todo.description
        })


# controller
@app.route('/')
def index():
    # views: index.html
    return render_template('index.html', data=Todo.query.all())

if __name__ == "__main__":
    app.run(host='0.0.0.0')