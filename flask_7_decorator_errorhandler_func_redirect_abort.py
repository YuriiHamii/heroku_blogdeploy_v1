# Flask #7: Декоратор errorhandler, функции redirect и abort
#           Важно при разработке сайта - отлавить ошибки - ответ от сервера
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort


app = Flask(__name__)

# Secret key - для начала работы с мгновенными сообщениями, шифрование данных, перед тем как сохранить данные
# чтобы пользователь браузера, если посмотрит на эти данные ничего не понял, что там записано
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hxg6h7f'

# Для отображения меню как ссылки прописываем список из словарей: ключ-name:название меню, ключ-url:соответствующий адресс url
menu = [{"name": "Downloading", "url": "install-flask"},
        {"name": "First application", "url": "first-app"},
        {"name": "Feedback", "url": "contact"}]

# с помощью декоратора .route() мы можем создавать привязку функции к определенному url адрессу
@app.route("/")
def index():
    return render_template('index.html', menu=menu)

@app.route("/about")
def about():
    return render_template('about.html', title="About website", menu=menu)

# contact - обработчик формы. Когда пользователь отправил данные формы мы сделаем проверку
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        print(request.form)
        print(request.form['username'])
        # данные должны передаватьсяпо методу POST, внутри которого делаем проверки и формируем сообщения
        if len(request.form['username']) > 2:
            flash('message sent successfully', category='success')
        else:
            flash('message sending error', category='error')
            #                              category - название как расширение классов стилей

    return render_template('contact.html', title="Feedback", menu = menu)


# пропишем обработчик формы пароля profile - перенаправление
# мы сохранили все в сессию и если выберем login и попытаемся перейти в форму авторизации автоматически будем перенаправлены в наш profile
# если пользователь самостоятельно в браузере набирает путь ошибочно http://127.0.0.1:5000/profile/selfedu2 ,
# то мы не должны давать ему доступа к этому profile, это не его profile, в его профайле записано selfedu, все другие адреса, должны быть ему не доступны
# для этого делается проверка
# if - проверка если пользователь не залогинился или свойство в сессии не соответствует username, который набран в строке запроса
#      то мы вернем ошибку сервера 401, которая означает, что доступ к странице завершен
# abort - функция прерывание запроса с ошибкой 401
@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"User profile: {username}"


# обработчик перенаправления запроса пользователя после авторизации
# обработчик привязан к адресу login, по этому адресу можем принимать данные по POSt GET запросу
# if - если свойство userLogged существует в нашей сессии, то мы делаем переадрессацию на соответств. profile с тем username который находится в сессии
# elif - берем данные из формы, если данные из формы соответствуют такому username и паролю 123, то
#        мы сохраняем данные в сессии и делаем переадресацию
#        request.method == 'POST' - условие, что вообще были переданы данные, иначе
# return - если все это не проходит отображаем данные формы - render_template
# чтоб воспользоваться сеесией и функцией redirect необходимо их импортировать
# пропишем шаблон login.html
@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)

# декоратор
@app.errorhandler(404)
# обработчик - функция принимает один аргумент error(ошибка сервера), далее возвратим шаблон page404, обработчик будет возвращать более понятную страницу для user
# сформируем шаблон в каталоге templates - pag404.html
# Теперь код возвращает 200 - [25/Mar/2022 12:43:36] "GET /page404.png HTTP/1.1" 200, исправим допишем параметр 404
def pageNotFount(error):
    return render_template('page404.html', title="Page not found", menu=menu), 404

# webserver start
if __name__ == "__main__":
    app.run(debug=True)


# 7. например отсутствует страница по адресу http://127.0.0.1:5000/456457
#    Not Found The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
#    404 Not Found - мы хотим создать пользователю создать более дружественную информацию
#    для этого используется декоратор errorhandler(404) в который мы указываем ту ошибку, которую нам вернет сервер и свяжем с ней наш обработчик

# 7. реализация перенаправления запроса, часто нужно перенаправить пользователя на другую страницу
#    например после успешной авторизации формы мы переходим автоматически на другую ссылку страницу
#    если пользователь уже авторизован, то второй раз ему уже авторизовывать страницу не нужно, поэтому сразу идет перенаправление
#    http://127.0.0.1:5000/profile/<username>

# Таким образом позьзователь может смотреть свой profile после авторизации login parol

# Test
# http://127.0.0.1:5000/76765656 - 404 as 500 - Page not found
# http://127.0.0.1:5000/login - 200 - "GET /login HTTP/1.1"
# http://127.0.0.1:5000/profile/selfedu - 302 - "POST /login HTTP/1.1"
# http://127.0.0.1:5000/profile/selfedu856 - 401 - "GET /profile/selfedu856 HTTP/1.1"
# http://127.0.0.1:5000/profile/selfedu - 200 - "GET /profile/selfedu HTTP/1.1" 200