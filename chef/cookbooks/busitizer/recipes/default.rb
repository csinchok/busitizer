#
# Cookbook Name:: busitizer
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe "database"
include_recipe "python"

user "busitizer" do
  action :create
  system true
end

directory "/var/venv" do
	owner "busitizer"
	group "www-data"
	mode 00744
	action :create
end

python_virtualenv "/var/venv" do
  options "--system-site-packages"
  action :create
  owner "busitizer"
  group "www-data"
end

package "libpq-dev"
package "libjpeg-dev"
package "libpng12-dev"

execute "install_requirements" do
	cwd "/www/busitizer"
	path ["/var/venv/bin"]
	environment ({'VIRTUAL_ENV' => '/var/venv', 'HOME' => '/tmp/.pip'})
	command "/var/venv/bin/pip install -r requirements.txt"
	user "busitizer"
end

# execute "sync_db" do
# 	cwd "/www/busitizer"
# 	path ["/var/venv/bin"]
# 	environment ({'VIRTUAL_ENV' => '/var/venv', 'HOME' => '/tmp/.pip'})
# 	command "/var/venv/bin/python manage.py syncdb"
# 	user "busitizer"
# end
