
# Todo-Piranha

This is a simple Todo Pyramind application.

[![](https://travis-ci.org/areski/todo-piranha.svg)](https://travis-ci.org/areski/todo-piranha)

We will have 2 versions one using Forms and Views and an other one built with
ReactJS:

* todo-piranha-form: Forms / Views Todo App

* todo-piranha-react: ReactJs Todo App

Todo-Piranha try to be minimilastic for new pyramid comers to learn about
Pyramid.

The following packages will be used:

* Pyramid
* Deform
* SQLalchemy
* Jinja2
* Colander
* WebOb
* Cornice
* Authentication with Twitter - https://github.com/cd34/apex
* WTForms-Alchemy


![todo login](https://github.com/areski/todo-piranha/raw/master/images/todo-login.png "Todo Login")

![todo view](https://github.com/areski/todo-piranha/raw/master/images/todo-view.png "Todo View")


## Install with Python 2.7

You can follow the instructions in the [Pyramid docs on installation][install].

Once you have Python and virtualenv installed, you can do the following:

```
$ mkdir ~/.virtualenvs
$ cd ~/.virtualenvs
$ virtualenv -p python2.7 todo-piranha
$ cd todo-piranha
$ source bin/activate
```

## Install with Python 3.4

Once you have Python3.4 installed, you can do the following:

```
$ cd todo-piranha
$ export VENV=`pwd`/env34
```

Create and activate the virtualenv:

```
$ python3.4 -m venv $VENV --without-pip
$ source $VENV/bin/activate
$ python3.4 -m ensurepip
```

Install Pyramid and [Sphinx][sphinx-doc] (Documentation):

```
$ $VENV/bin/pip3.4 install pyramid
$ $VENV/bin/pip3.4 install sphinx
```

## Install requirements and Init the DB

This creates the new virtual environment, now you can install the app.

```
(todo-piranha)$ cd project_directory
(todo-piranha)$ git clone https://github.com/areski/todo-piranha.git
(todo-piranha)$ cd todo-piranha/todopiranhaform
(todo-piranha)$ pip install -r requirements.txt -e .
```

This gives us the end result of the finished app. If it is the first time you are running the app, you will need to initialize the database.

```
(todo-piranha)$ initialize_todo-piranha-form_db development.ini
```

It can now be started up by doing the following.

```
(todo-piranha)$ pserve development.ini --reload
```

Now go to <http://localhost:6543> and enjoy!

## Run Tests

You can run tests with:
```
$VENV/bin/nosetests todopiranhaform -v
```
or
```
python setup.py test
```

## Contribute

If you want to contribute to this project, please feel free to fork away and
send pull request.


[install]: http://pyramid.readthedocs.org/en/latest/narr/install.html
[sphinx-doc]: http://sphinx-doc.org/
[deform]: http://docs.pylonsproject.org/projects/deform/en/latest/
[deform_bootstrap]: http://pypi.python.org/pypi/deform_bootstrap
[customux]: http://docs.pylonsproject.org/projects/pyramid_tutorials/en/latest/humans/creatingux/step05/index.html
[notfound]: http://docs.pylonsproject.org/projects/pyramid/en/latest/api/view.html#pyramid.view.notfound_view_config
[sqlalchemy]: http://www.sqlalchemy.org/
