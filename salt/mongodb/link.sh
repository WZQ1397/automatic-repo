for x in `ls /mongo/mongodb-linux-x86_64-3.4.6/bin/`
do
	ln -s /mongo/mongodb-linux-x86_64-3.4.6/bin/$x /usr/bin/$x
done