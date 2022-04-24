from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from buggybus.forms import JourneyForm, LoginForm, RegisterForm,SelectionForm
from datetime import date,datetime
from buggybus import db
from flask_login import login_user,login_required,logout_user
from buggybus.models import User


core = Blueprint('core',__name__)

@core.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        if request.form.get('From') and request.form.get('To') and request.form.get('Date'):
            req = request.form
            session['from'] = req.get("From")
            session['to'] = req["To"]
            Dat = req["Date"]  
            year= Dat[0:4]
            month= Dat[5:7]
            day= Dat[8:10]
            d=str(year) + "-" + str(month) + "-" + str(day)
            session['journy_date']=datetime.strptime(d,'%Y-%m-%d')
            if session['from']!='Select' and session['to']!='Select' and session['journy_date']>=datetime.now():
                return redirect(url_for("core.buslist"))
            elif session['journy_date']<datetime.now():
                return redirect(url_for("core.nobus"))
        else:
            flash("Please enter all the feilds required.")
    return render_template('index.html')

@core.route('/nobus')
def nobus():
    return render_template('nobus.html',date=session.get('journy_date').strftime('%d-%b-%Y'))

@core.route('/contact', methods=['GET','POST'])
def contact():
    if request.method =="POST":
        flash("You query has been submitted to us. Please wait while we respond to it.")
        return redirect(url_for("core.index"))
    return render_template('contact.html')

@core.route('/script')
@login_required
def script():
    if "msg" in session:
       return render_template('script.html')
    else:
        return redirect(url_for("core.user_review"))

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@core.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        reg_name=request.form.get('name')
        Dat = request.form.get('date')  
        year= Dat[0:4]
        month= Dat[5:7]
        day= Dat[8:10]
        d=str(year) + "-" + str(month) + "-" + str(day)
        dob=datetime.strptime(d,'%Y-%m-%d')
        age=calculate_age(dob)+2
        flash(f'Thankyou {reg_name} of age {age} for registration. Proceed to login.')
        return redirect(url_for('core.login'))
        
    return render_template('register.html')

@core.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=form.user_id.data
        passwd=form.password.data
        sql= f"SELECT * FROM users where username = '{user}' AND password = '{passwd}'"
        r=list(db.engine.execute(sql))
        if len(r)!=0:

            admin=User.query.filter_by(username='admin').first()
            login_user(admin)
            flash('Logged in successfully.Screenshot and send this to get your points(if you have not already done it).')
            
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
        else:
            flash("Sorry, Unable to find the user. If you haven't register please register else if you have registered and unable to login find other ways to login!!.")
    
    return render_template('login.html',form=form)

@core.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ï̶͚͐̕ͅt̴̳̙̍ ̵̜̍̆͊ͅa̷̙̮̽̚ ̶̹̼͐b̶̻͉̰̎̎ư̸̠͇̱̮͆̔g̶̯̍̒̋̕')
    return redirect(url_for('core.index'))

@core.route('/buslist',methods=['GET', 'POST'])
def buslist():
    from_city=session.get('to')
    to_city=session.get('from')
    if request.method == 'POST':
        passen=abs(int(request.form.get('Passengers')))
        if passen==0:
            passen=1
        session['Passengers']=passen
        return redirect(url_for('core.review'))
    # date=session.get('date')
    return render_template('buslist.html',from_city=from_city,to_city=to_city,date=session.get('journy_date').strftime('%d-%b-%Y'))

@core.route('/review')
@login_required
def review():
    from_city=session.get('to')
    to_city=session.get('from')
    size=session['Passengers']
    cost=int(size)*3000
    return render_template('review.html',from_city=from_city,to_city=to_city,cost=cost,date=session.get('journy_date').strftime('%d-%b-%Y'))

@core.route('/payment',methods=['GET','POST'])
@login_required
def payment():
    if request.method == "POST":
        username = request.form.get('username')
        password=request.form.get('password')
        session['user']=username
        lst=['Admin','Hemanth','Amit']
        if username in lst:
            sql= f"SELECT * FROM users where username = '{username}' AND password = '{password}'"
            r=list(db.engine.execute(sql))
            if len(r)!=0:
                return redirect(url_for('core.finalticket'))
        
    return render_template('payment.html')

@core.route('/finalticket')
@login_required
def finalticket():
    if "user" in session:
        return render_template('finalticket.html')
    else:
        return redirect(url_for('core.payment'))

@core.route('/user_review',methods=['GET','POST'])
@login_required
def user_review():
    if request.method =="POST":
        session['msg']=request.form.get('feedback')
        if "<script>" in request.form.get('feedback'):
            return redirect(url_for("core.script"))
        flash("You query has been submitted to us. Please wait while we respond to it.")
        return redirect(url_for("core.index"))
    
    return render_template('user_review.html')