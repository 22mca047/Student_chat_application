
import requests
import json

from flask_restful import Resource
from flask import make_response, render_template, request, redirect, url_for, session

s_id = ''


class Login(Resource):
    def get(self):
        return make_response(render_template('login.html'))


class Register(Resource):
    def get(self):
        return make_response(render_template('register.html'))

    def post(self):
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if password == cpassword:
            data = {
                'name': request.form.get('name'),
                'std': request.form.get('std'),
                'email': request.form.get('email'),
                'password': password
            }
            res = requests.post("http://127.0.0.1:2500/addData", json=data)

            if res.status_code == 200:
                return redirect('/')
            else:
                return redirect('/register')
        else:
            return redirect('/register')


class Home(Resource):
    def get(self):
        return make_response(render_template('home.html'))


class Chat(Resource):
    def get(self, friend_id):
        return make_response(render_template('chat-box.html', friend_id=friend_id))


class Bot(Resource):
    def get(self):
        return make_response(render_template('bot.html'))



