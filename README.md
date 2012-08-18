For now, this is just a placeholder for our Django Dash repo.

Setup:

    > git clone git@github.com:csinchok/busitizer.git
	> cd busitizer
	> virtualenv .env
	> source .env/bin/activate
	> pip install -r requirements.txt
	> python manage.py syncdb
	> python mange.py runserver