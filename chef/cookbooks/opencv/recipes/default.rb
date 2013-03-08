#
# Cookbook Name:: opencv
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

package "cmake"

python_pip "numpy" do
  action :install
end

remote_file "/tmp/opencv.tar.gz" do
  not_if "test -d /usr/local/include/opencv/"
  source "https://github.com/Itseez/opencv/archive/2.4.4.tar.gz"
  notifies :run, "bash[install_opencv]", :immediately
end

bash "install_opencv" do
  cwd "/tmp"
  code <<-EOH
    tar -zxf opencv.tar.gz
    cd opencv-2.4.4
    mkdir release
    cd release
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON ..
    make
    make install
  EOH
  action :nothing
end