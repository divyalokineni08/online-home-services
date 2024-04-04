
from flask import Flask, redirect, render_template, request, url_for
from models import create_customer, create_emp, login_customer, login_emp,book_servcie,accept_service,get_all_request

app = Flask(__name__)


@app.route('/')
def main_route():
    return render_template('index.html')

@app.route("/ub_signup", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("ub_signup.html")
    
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    mail = request.form.get("email")
    mobile_no = request.form.get("phone")
    language = request.form.get("language")
    gender = request.form.get("gender")
    # check if all fields are filled
    create_emp(first_name, last_name, password, mail, mobile_no, language,gender)
    return redirect(url_for("ub_login"))

@app.route('/ub_login',methods=["GET", "POST"])
def ub_login():
    
    if request.method == "GET":
        msg = request.args.get('msg')
        return render_template('ub_login.html', msg=msg)
    print("here")
    mail = request.form.get("email")
    password = request.form.get('password')
    user = login_emp(mail, password)
    print(user)
    if not user:
        return redirect(url_for("ub_login", msg="Invalid Credentials"))
    return redirect(url_for('table', empId=user['id']))
    

@app.route('/customer_login', methods=["GET", "POST"])
def customer_login():
    if request.method == "GET":
        msg = request.args.get('msg')
        return render_template('user_login.html', msg = msg)
    mail = request.form.get("email")
    password = request.form.get('password')
    user = login_customer(mail, password)
    if not user:
        return redirect(url_for("customer_login", msg="user does not exist or Invalid credentials"))
    return redirect(url_for('booking', customerId=user['id']))

@app.route('/customer_signup', methods=["GET", "POST"])
def customer_signup():
    if request.method == "GET":
        return render_template('user_signup.html')

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    mail = request.form.get("email")
    mobile_no = request.form.get("phone")
    address = request.form.get("address")
    state = request.form.get("state")
    city = request.form.get("city")
    zip = request.form.get("zip")
    country = request.form.get("country")
    gender = request.form.get("gender")
    
    create_customer(first_name, last_name, password, mail, mobile_no, address, state, city, zip ,country, gender)
    return redirect(url_for('customer_login'))


@app.route('/table')
def table():
    try:
        empId = request.args.get("empId")
        if not empId:
            return "Page Not Found"
        tasks = get_all_request(empId)
        return render_template('ub_dashboard.html', tasks=tasks, empId=empId)
    except Exception as e:
        print(e)
        return render_template('ub_login.html', msg="unable to fetch data")


@app.route('/booking', methods=["GET", "POST"])
def booking():
    customerId = request.args.get('customerId')
    if not customerId:
        return "Please login first"
    if request.method == "GET":
        return render_template('booking.html')
    
    service_type = request.form.get("service_type")
    service_date = request.form.get("service_date")
    service_time = request.form.get("service_time")
    language = request.form.get("language")
    book_servcie(service_type, service_date, service_time, language, customerId)
    return redirect(url_for('booking', customerId=customerId))

@app.route("/accept_service_request")
def accept_service_request():
    empId = request.args.get('empId')
    serviceId = request.args.get('serviceId')
    customerId = request.args.get('customerId')
    accept_service(empId, serviceId, customerId)
    return redirect(url_for('table', empId=empId))


if __name__ == '__main__':
    app.run(debug=True, port="8888")