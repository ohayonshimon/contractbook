#!/bin/bash

base_folder="$(dirname $0)"
virtualenv_folder="${base_folder}/.reports_env"
requirements_path="${base_folder}/../requirements.txt"
script_path="${base_folder}/../src/OWIDReports.py"
 
# set virtualenv
if [ ! -d ${virtualenv_folder} ]; then
  virtualenv ${virtualenv_folder}
fi

source ${virtualenv_folder}/bin/activate

# install dependencies
pip install -r ${requirements_path}

python ${script_path}