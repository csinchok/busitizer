Server setup is a bitch.

	sudo aptitude -y install build-essential
	sudo aptitude -y install cmake
	sudo aptitude -y install pkg-config
	sudo aptitude -y install libpng12-0 libpng12-dev libpng++-dev libpng3
	sudo aptitude -y install libpnglite-dev libpngwriter0-dev libpngwriter0c2
	sudo aptitude -y install zlib1g-dbg zlib1g zlib1g-dev
	sudo aptitude -y install libjasper-dev libjasper-runtime libjasper1
	sudo aptitude -y install pngtools libtiff4-dev libtiff4 libtiffxx0c2 libtiff-tools
	sudo aptitude -y install libjpeg8 libjpeg8-dev libjpeg8-dbg libjpeg-prog
	sudo aptitude -y install ffmpeg libavcodec-dev libavcodec52 libavformat52 libavformat-dev
	sudo aptitude -y install libgstreamer0.10-0-dbg libgstreamer0.10-0  libgstreamer0.10-dev
	sudo aptitude -y install libxine1-ffmpeg  libxine-dev libxine1-bin
	sudo aptitude -y install libunicap2 libunicap2-dev
	sudo aptitude -y install libdc1394-22-dev libdc1394-22 libdc1394-utils
	sudo aptitude -y install swig
	sudo aptitude -y install libv4l-0 libv4l-dev
	sudo aptitude -y install python-numpy
	sudo aptitude -y install libpython2.6 python-dev python2.6-dev

	# Debian cmake doesn't work with the current version of opencv...
	wget http://www.cmake.org/files/v2.8/cmake-2.8.8.tar.gz
	tar xfvz cmake-2.8.8.tar.gz
	cd cmake-2.8.8
	cmake . 
	make 
	sudo make install
	cd ..

	# Install opencv
	wget http://superb-sea2.dl.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.2/OpenCV-2.4.2.tar.bz2
	tar -xzf ./OpenCV-2.4.2.tar.bz2
	cd OpenCV-2.4.2/
	mkdir release
	cd release
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D BUILD_EXAMPLES=ON ..
	make
	sudo make install
