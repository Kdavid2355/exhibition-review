from flask import Flask, render_template, jsonify, request
from flask import session, redirect, url_for
from flask_session import Session



from pymongo import MongoClient
client = MongoClient('localhost', 27017 )
db = client.dbexhibition


app = Flask(__name__)
sess = Session()
SESSION_TYPE=['redis']

app.config.from_object(__name__)
Session(app)




@app.route('/')
def home():
    userid = session.get('userid',None)
    return render_template('home.html', userid=userid)





@app.route('/post', methods=['GET'])
def listing():
    result = list(db.exhibitions.find({},{'_id':0}))
    return jsonify({'result':'success' , 'exhibitions':result})

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')


@app. route('/login', methods=['POST','GET'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    userid_receive = request.form['userid']
    password_receive = request.form['password']

    result_id = db.users.find_one({'password':password_receive})
    
    try : 
        if userid_receive == result_id['userid '] and password_receive == result_id['password']:
            session['userid'] = request.form['userid']
            return redirect('/') 

    except TypeError:
        print('다시입력하세요!')
        return render_template('login.html')      



    #print(db.users.find({},{'_id':0},{'userid':userid_receive, 'password':password_receive}))
    # print(result_id['userid '])
    # if userid_receive == result_id['userid '] and password_receive == result_id('password'): 
    #     return render_template('home.html')
    #     #return render_template('home.html') 

    return render_template('login.html')

@app.route('/register',  methods=['POST','GET'])
def register():

    if request.method == 'GET':
        return render_template('register.html')
    
    userid = request.form['userid']
    password = request.form['password']
    repassword = request.form['re-password']

    if password == repassword :

        doc = {
            'userid ' : userid,
            'password' : password
        }

        db.users.insert_one(doc)

        db.session.add(users)
        db.session.commit()
        print('SUCCESS')

        return redirect('/')

    return render_template('register.html')
    



@app.route('/review')
def review():
    return render_template('review.html')



if __name__ == '__main__':

    app.secret_key = 'qwertyu'
    
    sess.init_app(app)
    
    app.run('127.0.0.1', port=5000, debug=True)
