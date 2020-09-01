from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

myDockerWebAppFlask: Flask = Flask(__name__, template_folder='myTemplates', static_folder='myStatic')

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
    return render_template('index.html')  # 'Hello World! It Works!'


@myDockerWebAppFlask.route('/contact.html')
def contact():
    return render_template('contact.html')


@myDockerWebAppFlask.route('/about.html')
def about():
    return render_template('about.html')


@myDockerWebAppFlask.route('/sign_in.html')
def sign_in():
    return render_template('sign_in.html')


@myDockerWebAppFlask.route('/sign_up.html')
def sign_up():
    return render_template('sign_up.html')


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
    return render_template('error.html')


if __name__ == '__main__':
    myDockerWebAppFlask.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
