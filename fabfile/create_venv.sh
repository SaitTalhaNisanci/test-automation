#This should point to where python 2 is.
PYTHON_2_PATH = '/usr/bin/python2.7'

#install virtualenv
python3 -m pip install --user virtualenv

#create the directory where virtualenv will be. 
mkdir env

# create virtualenv with python2 because we use fabric1.14 api and it is supported by python 2 
virtualenv --python=$PYTHON_2_PATH env/

# Activate the environment
source ./env/bin/activate

# Install requirements
pip install -r requirements.txt
