from flask import Flask, render_template, jsonify, request
from flask import session, redirect, url_for



from pymongo import MongoClient
client = MongoClient('localhost', 27017 )
db = client.dbexhibition


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')




@app.route('/post', methods=['GET'])
def listing():
    result = list(db.exhibitions.find({},{'_id':0}))
    return jsonify({'result':'success' , 'exhibitions':result})
    


@app.route('/review')
def review():
    return render_template('review.html')




if __name__ == '__main__':

    app.run('127.0.0.1', port=5000, debug=True)
