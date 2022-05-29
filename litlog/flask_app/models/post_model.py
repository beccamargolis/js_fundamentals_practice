from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Post:
    db_name = 'litlog_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.author = db_data['author']
        self.date_finished = db_data['date_finished']
        self.cover_img = db_data['cover_img']
        self.rating = db_data['rating']
        self.thoughts = db_data['thoughts']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save_post(cls,data):
        query = "INSERT INTO posts (user_id,title,author,date_finished,cover_img,rating,thoughts) VALUES (%(user_id)s,%(title)s,%(author)s,%(date_finished)s,%(cover_img)s,%(rating)s,%(thoughts)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_posts(cls,data):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def get_users_with_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        posts_list = []
        for row_from_db in results:
            posts_list.append(cls(row_from_db))
        return posts_list

    @classmethod
    def get_post_with_user(cls,data):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_user_with_post(cls,data):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE posts SET title=%(title)s, author=%(author)s, date_finished=%(date_finished)s, cover_img=%(cover_img)s, rating=%(rating)s, thoughts=%(thoughts)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
            query = "DELETE FROM posts WHERE posts.id = %(id)s;"
            return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['title']) < 1:
            is_valid = False
            flash("Title must be at least 1 character.","post")
        if len(post['author']) < 3:
            is_valid = False
            flash("Author name must be at least 3 characters.","post")
        if len(post['thoughts']) < 3:
            is_valid = False
            flash("Thoughts must be at least 3 characters.","post")

        return is_valid