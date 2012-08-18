==Busitizer==

If you want to run EVERYTHING locally, you'll want to do these, but the compilation will take a while:

    > brew install rabbitmq
	> brew install opencv
	
With or without those steps, you can get startd with this:

    > git clone git@github.com:csinchok/busitizer.git
	> cd busitizer
	> virtualenv .env
	> source .env/bin/activate
	> pip install -r requirements.txt
	> python manage.py syncdb
	> python mange.py runserver
	
Coverage reports are here: http://busitizer.com/coverage/index.html

Pylint reports are here: http://busitizer.com/pylint.html