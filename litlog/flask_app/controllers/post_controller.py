from fileinput import filename
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.post_model import Post
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/STL1099/OneDrive - SIRVA/Desktop/Coding Dojo/projects_algos/litlog/flask_app/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new/post') # to show the create post page
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("create.html", user=User.get_by_id(data))

@app.route('/create/post', methods=['GET', 'POST']) # to add a new post
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/new/post')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/create/post')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/create/post')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                    "title": request.form["title"],
                    "author": request.form["author"],
                    "date_finished": request.form["date_finished"],
                    "cover_img": "/static/images/"+filename,
                    "rating": request.form["rating"],
                    "thoughts": request.form["thoughts"],
                    "user_id": session['user_id']
            }
            Post.save_post(data)
        return redirect('/dashboard')

@app.route('/view/post/<int:post_id>')
def show_post(post_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":post_id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view.html",post=Post.get_post_with_user(data),user=User.get_by_id(user_data))

@app.route('/edit/post/<int:id>') # show the page to edit the post
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Post.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/post',methods=['POST']) # action of updating the post
def update_post():
    id = request.form['id'] # using the id that's coming in from the form so we need to create a variable to be used in an f string
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect(f'/edit/post/{id}')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/create/post')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect('/create/post')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                "title": request.form["title"],
                "author": request.form["author"],
                "date_finished": request.form["date_finished"],
                "cover_img": "/static/images/"+filename,
                "rating": request.form["rating"],
                "thoughts": request.form["thoughts"],
                "id": request.form["id"]
            }
        Post.update(data)
        return redirect(f'/view/post/{id}')

@app.route('/destroy/post/<int:id>')
def destroy_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Post.destroy(data)
    return redirect('/dashboard')