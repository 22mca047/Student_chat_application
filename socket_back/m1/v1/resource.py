import datetime
import json
import requests
import openai
from flask import request, session
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from flask_socketio import Namespace, join_room, emit
from sqlalchemy import text
from m1 import redis, es


class CheckLogin(Resource):
    def post(self):
        data = request.json
        email = data['student_email']
        password = data['student_password']
        from m1.v1.models import connection
        query = text('select * from student where student_email=:email')
        result = connection.execute(query, {'email': email})
        key = list(result.keys())
        value = list(result.fetchone())
        res = {}
        for i in range(len(key)):
            res[key[i]] = value[i]
        if res['student_password'] == password:
            token = create_access_token(identity=res['student_id'])
            data = {
                'student_id': res['student_id'],
                'student_name': res['student_name'],
                'student_email': res['student_email'],
                'student_std': res['student_std'],
                'token': token
            }
            return {'token': token, 'student_id': res['student_id']}, 200
        else:
            return redirect('/')


class Adddata(Resource):
    # @jwt_required()
    def post(self):
        data = request.json
        print(data)
        name = data.get('name')
        std = data.get('std')
        email = data.get('email')
        password = data.get('password')
        from m1.v1.models import connection
        query = text("insert into student (student_name, student_std, student_email, student_password) values(:name, "
                     ":std, :email, :password)")
        connection.execute(query, {'name': name, 'std': std, 'email': email, 'password': password})
        connection.commit()
        return True, 200


class Getall(Resource):
    # @jwt_required()
    def post(self):
        a = "name"
        b = reversed(a)
        data = request.json
        print('hii')
        id = data['student_id']
        from m1.v1.models import connection
        query = text("select * from teacher")
        result = connection.execute(query)
        key = list(result.keys())
        value = list(result.fetchall())

        query2 = text("select * from student where student_id not in (:id)")
        result2 = connection.execute(query2, {'id': id})
        key2 = list(result2.keys())
        value2 = list(result2.fetchall())
        k = []
        l = []
        for i in range(len(value)):
            data = {}
            for j in range(len(key)):
                data[key[j]] = value[i][j]
            l.append(data)

        for i in range(len(value2)):
            data = {}
            for j in range(len(key2)):
                data[key2[j]] = value2[i][j]
            k.append(data)
        return {'teacher_data': l, 'student_data': k}, 200


class Fsdata(Resource):
    # @jwt_required()
    def post(self):
        data = request.json
        friend_id = data['friend_id']
        student_id = data['student_id']
        from m1.v1.models import connection
        query = text("select * from student where student_id=:student_id")
        result1 = connection.execute(query, {'student_id': student_id})
        query2 = text("select * from student where student_id=:friend_id")
        result2 = connection.execute(query2, {'friend_id': friend_id})
        key1 = list(result1.keys())
        value1 = list(result1.fetchone())
        key2 = list(result2.keys())
        value2 = list(result2.fetchone())
        s = {}
        f = {}
        for i in range(len(key1)):
            s[key1[i]] = value1[i]
        for j in range(len(key2)):
            f[key2[j]] = value2[j]
        data = {
            'student_detail': s,
            'friend_detail': f
        }
        return data, 200


socket_ids = {}


class Bot(Resource):
    def post(self):
        url = "https://simple-chatgpt-api.p.rapidapi.com/ask"

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "ca114b6e0emshe44af04ecab6a12p1109b3jsn46872d1977ab",
            "X-RapidAPI-Host": "simple-chatgpt-api.p.rapidapi.com"
        }

        data = request.json
        payload = {
            'question': data['msg']
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json().get("answer"))
        ans = {
            'response': response.json().get("answer")
        }
        return ans


class Chat(Namespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.convo = []

    def on_connect(self):
        friend_id = request.args.get('friend_id')
        uid = request.args.get('student_id')
        from m1.v1.models import connection

        query = text("select * from student where student_id = :fr_id")
        result = connection.execute(query, {'fr_id': friend_id})
        key = list(result.keys())
        value = list(result.fetchone())
        friend_data = dict(zip(key, value))

        room = f'chat_{min(int(friend_id), int(uid))}_{max(int(friend_id), int(uid))}'
        if not es.indices.exists(index='chat'):
            es.indices.create(index='chat')

        query = {
            "query": {
                "term": {
                    "room.keyword": room
                }
            }
        }

        try:
            result = es.search(index='chat', body=query)
            hits = result['hits']['hits']
            chat_data = []
            if hits:
                for hit in hits:
                    chat_data.extend(hit['_source'].get('chat', []))
                redis.set(room, json.dumps(chat_data))
                emit('history', {'response': chat_data})
        except Exception as e:
            print(f"Error searching Elasticsearch: {e}")

        join_room(room)

    def on_handlesocket(self, data):
        socket_id = data.get('socket_id')
        uid = data.get('student_id')
        friend_id = data.get('friend_id')

        from m1.v1.models import connection
        query = text("call new_chat(:socket_id, :sender_id, :receiver_id)")
        connection.execute(query, {'socket_id': socket_id, 'sender_id': uid, 'receiver_id': friend_id})
        connection.commit()

    def on_message(self, data):
        socket_id = data.get('socket_id')
        msg = data.get('msg')
        from m1.v1.models import connection

        query = text("select * from manage_chat where socket_id=:socket_id")
        result = connection.execute(query, {'socket_id': socket_id})
        key = list(result.keys())
        value = list(result.fetchone())
        ans = dict(zip(key, value))

        uid = ans['sender_id']
        friend_id = ans['receiver_id']
        room = f'chat_{min(int(friend_id), int(uid))}_{max(int(friend_id), int(uid))}'

        message_data = {
            'sender_id': uid,
            'receiver_id': friend_id,
            'msg': msg,
            'Time': str(datetime.datetime.now())[:19]
        }

        self.convo = redis.get(room)
        if self.convo is None:
            self.convo = []
        else:
            self.convo = json.loads(self.convo)

        if not isinstance(self.convo, list):
            self.convo = []

        self.convo.append(message_data)
        redis.set(room, json.dumps(self.convo))

        query = {
            "query": {
                "term": {
                    "room.keyword": room
                }
            }
        }
        try:
            result = es.search(index='chat', body=query)
            hits = result['hits']['hits']
            if hits:
                for hit in hits:
                    doc_id = hit['_id']
                    update_body = {
                        "doc": {
                            "chat": self.convo
                        }
                    }
                    es.update(index='chat', id=doc_id, body=update_body)
            else:
                # If no hits, create a new document
                es.index(index='chat', body={
                    "room": room,
                    "chat": self.convo
                })
        except Exception as e:
            print(f"Error updating Elasticsearch: {e}")

        emit('message', {
            'student_id': uid,
            'student_name': session.get('student_name'),
            'friend_id': friend_id,
            'friend_name': session.get('friend_name'),
            'msg': msg,
            'time': str(datetime.datetime.now())[:19]
        }, room=room)
