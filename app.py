from flask import Flask, render_template , request , session
from dbconnection import Db
import Extraction

app = Flask(__name__)
app.secret_key="hello"




@app.route('/')
def log():
    return render_template('public/Login.html')
@app.route('/login', methods=["POST"])
def login():
    user_name=request.form["username"]
    password=request.form["password"]
    a="SELECT*FROM login WHERE username='"+user_name+"' AND PASSWORD='"+password+"'"
    print(a)

    db=Db()
    data=db.selectOne(a)


    if data["type"]=="admin":
        return render_template('admin/admin.html')
    elif data["type"]=="user":
        QR = "SELECT * FROM `registration` WHERE `login_id`='" + str(data["login_id"]) + "'"
        r = db.selectOne(QR)
        if r is not None:
            session["lid"]=data["login_id"]
            return render_template('user/userhome.html')
        else:
            return '''<script>alert("Invalid User");window.location="/"</script>'''

    else:
        return "no"

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')

@app.route('/user')
def adm():
    return render_template('user/userhome.html')



@app.route('/registration')
def reg():
    return render_template('public/index.html')
@app.route('/regist' , methods= ["POST"])
def registration():
    firstname=request.form["firstname"]
    lastname=request.form["lastname"]
    username=request.form["username"]
    password=request.form["password"]
    b="INSERT INTO login (username,PASSWORD,TYPE) values('"+username+"','"+password+"','user')"
    dbb=Db()
    loginid=dbb.insert(b)
    c="INSERT INTO registration (login_id,first_name,last_name,email) values('"+str(loginid)+"','"+firstname+"','"+lastname+"','"+username+"')"
    q=dbb.insert(c)
    return log()

@app.route('/viewusers')
def view():
    v="SELECT registration.*,login.type FROM registration INNER JOIN login ON registration.login_id=login.login_id"
    view=Db()
    users=view.select(v)
    return render_template('admin/viewusers.html', data=users)

@app.route('/blockorunblock/<lid>/<status>')
def block(lid,status):
    bl="UPDATE login set type='"+status+"' WHERE login_id ='"+lid+"'"
    block=Db()
    blk=block.update(bl)
    return view()

@app.route('/viewcomplaints')
def complaints():
    cm="SELECT complaints.*,registration.login_id,registration.first_name,registration.last_name FROM registration INNER JOIN complaints ON complaints.v_lid=registration.login_id"
    cmp=Db()
    compl=cmp.select(cm)
    return render_template('admin/viewcomplaints.html', data=compl)

@app.route('/reply/<cid>')
def reply(cid):
    re="SELECT complaint , complaint_id FROM complaints WHERE complaint_id='"+cid+"'"
    rep=Db()
    reply=rep.selectOne(re)
    return render_template('admin/reply.html',data=reply)
@app.route('/replypost', methods=["POST"])
def rep():
    r=request.form["reply"]
    cid=request.form["cid"]
    repl="UPDATE complaints set reply='"+r+"' WHERE complaint_id='"+str(cid)+"' "
    dbb=Db()
    dbb.update(repl)
    return complaints()

@app.route('/sndcomp')
def comp():
    return render_template('user/sndcompl.html')

@app.route('/snd', methods=["post"])
def com():
    w=request.form["sndcomplaints"]
    uid=session["lid"]
    rply="pending"
    s="INSERT INTO complaints(complaint,reply,DATE,v_lid) VALUES ('"+w+"','"+rply+"',curdate(),'"+str(uid)+"')"
    dbb=Db()
    sn=dbb.insert(s)
    return "ok"

@app.route('/usreply')
def viewreply():
    qr="SELECT * FROM complaints WHERE v_lid='"+str(session["lid"])+"'"
    dbb=Db()
    q=dbb.select(qr)
    return render_template("user/viewrepl.html" , que=q)

@app.route('/search')
def search():
    return render_template('user/search.html')

@app.route('/search_post', methods=["post"])
def search_post():
    name=request.form["search"]
    output=Extraction.getResult(name)

    return render_template('user/search.html',output=output,url=name)

@app.route('/datadetails')
def datadetails():
    import numpy as np
    data = np.loadtxt("C:\\Users\\dragon\\project phishing\\static\\dataset.csv", delimiter=",")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!_____________________________________________________________________")

    print(data)
    return render_template('user/datadetails.html',data=data)


@app.route('/profile')
def profiledata():
    user="SELECT * FROM `registration` WHERE `login_id`='"+str(session["lid"])+"'"
    print(user)
    d=Db()
    res=d.selectOne(user)
    return render_template('user/profile.html',name1=res["first_name"],name2=res["last_name"],name3=res["email"])

if __name__ == '__main__':
    app.run(debug=True)

