from datetime import datetime
# from symbol import try_stmt

from flask import Flask, render_template, request, json, session, redirect  # , jsonify
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

myDockerWebAppFlask: Flask = Flask(__name__, template_folder='myTemplates',  static_folder='myStatic')

myDockerWebAppFlask.secret_key = 'Say hello to my little friend!'


@myDockerWebAppFlask.template_filter()
def date_time_filter(value, my_format='%d/%m/%Y %H:%M:%S'):
    return value.strftime(my_format)


myDockerWebAppFlask.jinja_env.filters['datetimefilter'] = date_time_filter


mysql = MySQL()

myDockerWebAppFlask.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
myDockerWebAppFlask.config['MYSQL_DATABASE_USER'] = 'fox'
myDockerWebAppFlask.config['MYSQL_DATABASE_PASSWORD'] = 'LLCTR001'
myDockerWebAppFlask.config['MYSQL_DATABASE_DB'] = 'DockerWebApp'
myDockerWebAppFlask.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(myDockerWebAppFlask)

myConnection = mysql.connect()
myCursor = myConnection.cursor()


DB_EXISTS_DATA = 'false'


@myDockerWebAppFlask.route('/my_db_entry_check')
def my_db_entry_check():
    try:
        if session.get('user'):
            global DB_EXISTS_DATA

            my_user = session.get('user')

            my_connection = mysql.connect()
            my_db_cursor = my_connection.cursor()
            my_db_cursor.callproc('RetrieveDataWebApp', (my_user,))
            my_db_data = my_db_cursor.fetchall()

            if len(my_db_data) > 0:
                DB_EXISTS_DATA = 'true'
                my_connection.close()
                my_db_cursor.close()
                return DB_EXISTS_DATA
            else:
                DB_EXISTS_DATA = 'false'
                my_connection.close()
                my_db_cursor.close()
                return DB_EXISTS_DATA
        else:
            return render_template('error.html', error='Unauthorized Access', current_date_time=datetime.now())
            # , 'Unauthorized Access'
    except Exception as ex:
        return render_template('error.html', error=str(ex), current_date_time=datetime.now())


@myDockerWebAppFlask.route('/index.html')
def index():
    if session.get('user'):
        return render_template('index.html', current_date_time=datetime.now())
        # 'Hello World! It Works!' , current_date_time=datetime.now()
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
        global DB_EXISTS_DATA

        my_email = request.form['inputEmail']
        my_password = request.form['inputPassword']

        vul_connection = mysql.connect()
        my_cursor = vul_connection.cursor()
        my_cursor.callproc('ValidateUserLogin', (my_email,))
        my_data = my_cursor.fetchall()

        if len(my_data) > 0:
            if check_password_hash(str(my_data[0][3]), my_password):
                session['user'] = my_data[0][0]
                my_db_entry_check()
                if DB_EXISTS_DATA == 'false':
                    return redirect('/formular.html')
                else:
                    return redirect('/show_current_db_entries.html')
            else:
                return render_template('error.html', error='Wrong password or email', current_date_time=datetime.now())
        else:
            return render_template('error.html', error='Wrong password or email', current_date_time=datetime.now())

    except Exception as ex:
        return render_template('error.html', error=str(ex), current_date_time=datetime.now())
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
        myCursor.close()
        myConnection.close()
        return json.dumps({'error': str(my_data[0])})

    # myCursor.close()
    # myConnection.close()


@myDockerWebAppFlask.route('/db_entry_adds', methods=['POST'])
def db_entry_adds():
    try:
        if session.get('user'):
            global DB_EXISTS_DATA

            # my_entry_id = request.form['inputPersonelId']
            my_entry_name = request.form['inputNames']
            my_entry_surname = request.form['inputSurname']
            my_entry_age = request.form['inputAge']
            my_entry_email = request.form['inputEMails']
            my_entry_street = request.form['inputStreet']
            my_entry_houseno = request.form['inputHouseNo']
            my_entry_postalcode = request.form['inputPostalCode']
            my_entry_city = request.form['inputCity']
            my_entry_country = request.form['inputCountry']
            my_entry_phonenumber = request.form['inputPhoneNumber']
            my_entry_user_id = session.get('user')

            my_connection = mysql.connect()
            my_cursor = my_connection.cursor()
            my_cursor.callproc('EntryWebApp', (my_entry_name, my_entry_surname, my_entry_age,
                                               my_entry_email, my_entry_street, my_entry_houseno, my_entry_postalcode,
                                               my_entry_city, my_entry_country, my_entry_phonenumber,
                                               my_entry_user_id))
            my_data = my_cursor.fetchall()

            if len(my_data) == 0:
                my_connection.commit()
                DB_EXISTS_DATA = 'true'
                return render_template('db_entries.html', current_date_time=datetime.now())
            else:
                return render_template('error.html', error='An error occurred!', current_date_time=datetime.now())
                # , 'An error occurred!'
        else:
            return render_template('error.html', error='Unauthorized Access', current_date_time=datetime.now())
            # , 'Unauthorized Access'
    except Exception as ex:
        return render_template('error.html', error=str(ex), current_date_time=datetime.now())
    # finally:
        # my_cursor.close()
        # my_connection.close()


@myDockerWebAppFlask.route('/db_entries.html')
def db_entries():
    return render_template('db_entries.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/show_current_db_entries.html')
def show_current_db_entries():
    return render_template('show_current_db_entries.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/error.html')
def error():
    return render_template('error.html', current_date_time=datetime.now())


@myDockerWebAppFlask.route('/formular.html')
def formular():
    global DB_EXISTS_DATA

    if DB_EXISTS_DATA == 'false':
        return render_template('formular.html', current_date_time=datetime.now(), DB_EXISTS_DATA=False)
    elif DB_EXISTS_DATA == 'true':
        return render_template('formular.html', current_date_time=datetime.now(), DB_EXISTS_DATA=True)


'''@myDockerWebAppFlask.route('/show_db_entries.html', methods=['POST'])
def show_db_entries():
    try:
        if session.get('user'):
            my_user = session.get('user')

            my_connection = mysql.connect()
            my_cursor = my_connection.cursor()
            my_cursor.callproc('RetrieveDataWebApp', my_user)
            # my_cursor.execute("select * from DockerWebApp.dbentries;", (my_user,))
            current_db_entries = my_cursor.fetchall()

            my_current_db_entries_list = []
            for each_db_entry in current_db_entries:
                my_current_db_entry_dict = {
                    'Names': each_db_entry[1],
                    'Surname': each_db_entry[2],
                    'Age': each_db_entry[3],
                    'EMail': each_db_entry[4],
                    'Street': each_db_entry[5],
                    'HouseNo': each_db_entry[6],
                    'PostalCode': each_db_entry[7],
                    'Country': each_db_entry[8],
                    'PhoneNumber': each_db_entry[9],
                }
                my_current_db_entries_list.append(my_current_db_entry_dict)

            return json.dumps(my_current_db_entries_list)  # json.dumps(my_current_db_entries_list)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))
'''


@myDockerWebAppFlask.route('/retrieve_entries')
def retrieve_entries():
    try:
        if session.get('user'):
            my_user = session.get('user')

            my_connection = mysql.connect()
            my_cursor = my_connection.cursor()
            my_cursor.callproc('RetrieveDataWebApp', (my_user,))
            the_db_entries = my_cursor.fetchall()

            my_db_entries_list = []
            for each_db_entry in the_db_entries:
                my_db_entry_dict = {
                    'Names': each_db_entry[1],
                    'Surname': each_db_entry[2],
                    'Age': each_db_entry[3],
                    'EMails': each_db_entry[4],
                    'Street': each_db_entry[5],
                    'HouseNo': each_db_entry[6],
                    'PostalCode': each_db_entry[7],
                    'City': each_db_entry[8],
                    'Country': each_db_entry[9],
                    'PhoneNumber': each_db_entry[10],
                    # 'PersonelId': each_db_entry[10]
                }
                my_db_entries_list.append(my_db_entry_dict)

            return json.dumps(my_db_entries_list)  # jsonify({'Entry_List': my_db_entries_list})
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))


@myDockerWebAppFlask.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    myDockerWebAppFlask.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
