from datetime import datetime

from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

myDockerWebAppFlask: Flask = Flask(__name__, template_folder='myTemplates', static_folder='myStatic')


@myDockerWebAppFlask.template_filter()
def datetimefilter(value, format='%d/%m/%Y %H:%M:%S'):
    """Convert a datetime to a different format."""
    return value.strftime(format)


myDockerWebAppFlask.jinja_env.filters['datetimefilter'] = datetimefilter

myDockerWebAppFlask.secret_key = 'Say hello to my little friend!'

mysql = MySQL()

myDockerWebAppFlask.config['MYSQL_DATABASE_USER'] = 'FoxMulder'
myDockerWebAppFlask.config['MYSQL_DATABASE_PASSWORD'] = 'llctrMP001'
myDockerWebAppFlask.config['MYSQL_DATABASE_DB'] = 'LoginWebApp'
myDockerWebAppFlask.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(myDockerWebAppFlask)

myConnection = mysql.connect()
myCursor = myConnection.cursor()


@myDockerWebAppFlask.route('/index.html')
def index():
    if session.get('user'):
        return render_template('index.html', current_date_time=datetime.now())  # 'Hello World! It Works!'
    else:
        return render_template('error.html', error='Unauthorized User Access', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/contact.html')
def contact():
    return render_template('contact.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/about.html')
def about():
    return render_template('about.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/sign_in.html')
def sign_in():
    return render_template('sign_in.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/ValidateUserLogin', methods=['POST'])
def validate_user_login():
    try:
        my_email = request.form['inputEmail']
        my_password = request.form['inputPassword']

        vul_connection = mysql.connect()
        my_cursor = vul_connection.cursor()
        my_cursor.callproc('ValidateUserLogin', (my_email,))
        my_data = my_cursor.fetchall()

        if len(my_data) > 0:
            if check_password_hash(str(my_data[0][3]), my_password):
                session['user'] = my_data[0][0]
                return redirect('/formular.html')
            else:
                return render_template('error.html', error='Wrong password or email', current_date_time=datetime.now())
        else:
            return render_template('error.html', error='Wrong password or email', current_date_time=datetime.now())

    except Exception as ex:
        return render_template('error.html', error=str(ex))
    finally:
        myCursor.close()
        vul_connection.close()


@myDockerWebAppFlask.route('/sign_up.html')
def sign_up():
    return render_template('sign_up.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/sign_ups', methods=['POST'])
def sign_ups():
    my_name = request.form['inputName']
    my_email = request.form['inputEmail']
    my_password = request.form['inputPassword']

    my_hashed_password = generate_password_hash(my_password)

    myCursor.callproc('LoginWebAppCU', (my_name, my_email, my_hashed_password))

    my_data = myCursor.fetchall()

    if len(my_data) == 0:
        myConnection.commit()
        return json.dumps({'message': 'The User has been created successfully!'})
    else:
        # myCursor.close()
        # myConnection.close()
        return json.dumps({'error': str(my_data[0])})

    # myCursor.close()
    # myConnection.close()


@myDockerWebAppFlask.route('/error.html')
def error():
    return render_template('error.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/formular.html')
def formular():
    return  render_template('formular.html', current_date_time=datetime.now())


if __name__ == '__main__':
    myDockerWebAppFlask.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
