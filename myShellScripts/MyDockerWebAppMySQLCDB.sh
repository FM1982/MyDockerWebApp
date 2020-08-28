#!/bin/bash

reset=$(tput sgr0)
green=$(tput setaf 76)

function input(){
	printf "> $@\n"
}

function sucop(){
	printf "${green}==> %s${reset}\n" "$@"
}

function printStatusSuccess(){
	sucop "MySQL DB creation completed!"

	echo " >> Host		: ${DB_HOST}"
	echo " >> Database		: ${DB_NAME}"
	echo " >> User		: ${DB_USER}"

	echo "Done by Mario Luensmann"
}

function parseArgs(){
	for arg in "$@"
	do
		case $arg in
			-h=*|--host=*)
				DB_HOST="${arg#*=}";;
			-d=*|--database=*)
				DB_NAME="${arg#*=}";;
			-u=*|--user=*)
				DB_USER="${arg#*=}";;
			esac
		done
		[[ -z $DB_NAME ]] && echo "Database name can not be empty." && exit 1
		[[ $DB_USER ]] || DB_USER=$DB_NAME
}

function createAMySqlDb() {
	SQLCommand1="DROP DATABASE IF EXISTS ${DB_NAME};"
	SQLCommand2="CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
	SQLCommand3="USE ${DB_NAME};"
	SQLCommand4="DROP USER IF EXISTS '${DB_USER}'@'localhost';"
	SQLCommand5="CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY 'LLCTR001';"
	SQLCommand6="GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
	SQLCommand7="FLUSH PRIVILEGES;"

	if [ -f /root/.my.cnf ]; then
		$BIN_MYSQL -e "${SQLCommand1}${SQLCommand2}${SQLCommand3}${SQLCommand4}${SQLCommand5}${SQLCommand6}${SQLCommand7}"
	else
		input "Enter database name, please!"
		read rootPassword
		$BIN_MYSQL -h $DB_HOST -u root -p ${rootPassword} -e "${SQLCommand1}${SQLCommand2}${SQLCommand3}${SQLCommand4}${SQLCommand5}${SQLCommand6}${SQLCommand7}"
	fi
}

function createLoginTable(){
	SQLCommand1="CREATE TABLE ${DB_NAME}.credentials (
	myuser_id BIGINT NOT NULL AUTO_INCREMENT,
	myuser_name VARCHAR(30) NOT NULL,
	myuser_username VARCHAR(30) NOT NULL,
	myuser_password VARCHAR(255) NOT NULL,
	PRIMARY KEY(myuser_id) );"

	
	if [ -f /root/.my.cnf ]; then
		$BIN_MYSQL -e "${SQLCommand1}"
	else
		input "Enter database name, please!"
		read rootPassword
		$BIN_MYSQL -h $DB_HOST -u root -p ${rootPassword} -e "${SQLCommand1}"
	fi
}

export LC_CTYPE=C
export LANG=C

VERSION="0.0.1"

BIN_MYSQL=$(which mysql)

DB_HOST='localhost'
DB_NAME=
DB_USER=

function main(){

	sucop "Processing arguments ..."
	parseArgs "$@"
	sucop "Done!"

	sucop "Creating MySQL db ..."
	createAMySqlDb
	sucop "Done!"

	sucop "Creating MySQL db Table ..."
	createLoginTable
	sucop "Done!"

	printStatusSuccess

	exit 0
}

main "$@"
