#!/bin/bash

#prime-browse variables
PRIME_REPOSITORY_URL="https://raw.githubusercontent.com/DaS-Wunder/prime-browse/master/"
PRIME_FILES[0]="webapp/index.html"
PRIME_FILES[1]="webapp/search.app.js"
PRIME_FILES[2]="webapp/style.css"
PRIME_FILES[3]="webapp/widget.filter.js"
PRIME_FILES[4]="webapp/widget.multi-facet-viewer.js"

#recline variables
RECLINE_VERSION="v0.6"
RECLINE_REPOSITORY_URL="https://github.com/okfn/recline.git"
RECLINE_FOLDERNAME="recline"

#elasticsearchjs variable
ELASTICSEARCH_JS_REPOSITORY_URL="https://raw.githubusercontent.com/okfn/elasticsearch.js/gh-pages/"
ELASTICSEARCH_JS_FILE="elasticsearch.js"

if [ $# -ne 2 ]
then
	echo -e "\n
		 $0 USERNAME INSTALLPATH \n
		 Some parameter are missing. \n
		 This program needs two parameter.\n 
		 The first is the username of the user under which the webserver runs,\n
		 normaly apache or nginx.\n 
		 The second parameter is the installation dir, where this user had to have write access. \n
		"
	exit -1

else
	USERNAME=$1
	USERGROUP=`id -g $USERNAME`
	INSTALLDIR=$2	

fi

	
######################################################################
# Enter installation directory and create expected directory. 
######################################################################

cd -- "$INSTALLDIR" 2>/dev/null || { echo -e "\n Can't enter $INSTALLDIR. Does the Path exists or have you the permissions to enter ?\n Installation aborted.\n"; exit 1; }

echo -e "\n	Entering $INSTALLDIR"

mkdir -p lib 2>/dev/null || { echo -e "\n Can't create $INSTALLDIR/lib. Do you have the right to write access in $INSTALLDIR ?\n Installation aborted.\n"; exit 1; }

echo  -e "\n	Creating directory lib"


######################################################################
# Download all repositry files
######################################################################
cd -- "$INSTALLDIR/lib" 2>/dev/null || { echo -e "\n Can't enter $INSTALLDIR/lib. Does the Path exists or have you the permissions to enter ?\n Installation aborted.\n"; exit 1; }

echo -e "\n	Entering $INSTALLDIR/lib \n	Beginn to download repositry files ...\n"



######################################################################
# Download all Prime-browse repositry files for webaccess
######################################################################

echo -e "\n	...try to get all files from prime-browse...."

cd $INSTALLDIR
for FILE in "${PRIME_FILES[@]}"
do
	wget -N $PRIME_REPOSITORY_URL$FILE
	
done

echo -e "\n	...downloaded all files from prime-browse for the website ..."
cd $INSTALLDIR/lib

######################################################################
# Download all recline files which are needed 
######################################################################

echo -e "\n     ...try to get all files from recline...."

git clone --branch $RECLINE_VERSION $RECLINE_REPOSITORY_URL $RECLINE_FOLDERNAME

echo -e "\n     ...downloaded all files from $RECLINE_FOLDERNAME ..."


######################################################################
# Download elasticsearch.js file 
######################################################################

echo -e "\n	...try to get elasticsearch.js...."

	wget -N $ELASTICSEARCH_JS_REPOSITORY_URL$ELASTICSEARCH_JS_FILE

echo -e "\n	...downloaded elasticsearch.js ..."
echo -e "\n	... all files downloaded \n"


######################################################################
# Changing ownership of files in folder
######################################################################
echo -e "\n	Changing ownership and executive rights of files in $INSTALLDIR..."

cd ..
chown -R $USERNAME:$USERGROUP .
chmod -R 744 .

echo -e "\n 	.... all done.\n"
echo -e "\n	Installation complete. Only thing you have to do now is to let your webserver point to $INSTALLDIR.\n
Good luck :-)"
exit 
