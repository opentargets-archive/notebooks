# notebooks
assorted set of ipython notebooks

Trying to follow a somewhat [organized directory structure](https://drivendata.github.io/cookiecutter-data-science/#directory-structure)

## to run them locally

If you don't have virtualenv installed, use pip to install it:
```sh
pip install virtualenv
```

clone and create a virtualenv running python 3
```sh
virtualenv env -p python3
```

and install the packages specified in the `requirements.txt` file after activating the virtualenv
```sh
source env/bin/activate
pip install -r requirements.txt
```
