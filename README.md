# Busitizer

From the about page:

    THE BUSITIZER applies star of stage and screen Gary Busey to your very own Facebook photos.
    Connect your Facebook profile and let THE BUSITIZER discover which of your memories best deserves a little more Gary Busey.

Basically, this app connects to Facebook, grabs some pictures, and pastes Gary Busey on the faces that it finds.

There's also a twitter bot component (the original inspiration of busitizer), allowing people to tweet links at the bot, but it can then busitize.

*Development setup*

If you want to run EVERYTHING locally, you'll want to do these, but the compilation will take a while:

    > brew install rabbitmq
    > brew install opencv
	
OpenCV is a problem, because there's not a good install on Debian for it. I was able to get it compiled and in the virtualenv, and if you're interested in how that happened, check the server_setup.md file in this directory.

With or without those steps, you can get startd with this:

    > git clone git@github.com:csinchok/busitizer.git
	> cd busitizer
	> virtualenv .env
	> source .env/bin/activate
	> pip install -r requirements.txt
	> python manage.py syncdb
	> python manage.py migrate
	> python mange.py runserver

We had great plans of coverage reports, unit tests, etc. These plans did not go great.	

Coverage reports are here: http://busitizer.com/coverage/index.html

Pylint reports are here: http://busitizer.com/pylint.html