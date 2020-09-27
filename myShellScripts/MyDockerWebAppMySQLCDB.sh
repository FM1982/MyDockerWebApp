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
	echo " >> Password		: ${DB_PASS}"
	echo " >> TableLogin		: ${DB_TABLE_LOG}"
	echo " >> TableEntries" : ${DB_TABLE_ENTRY}

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
			-t=*|--table_log=*)
				DB_TABLE_LOG="${arg#*=}";;
		  	-p=*|--table_entry=*)
				DB_TABLE_ENTRY="${arg#*=}";;
			-p=*|--pass=*)
				DB_PASS="${arg#*=}";;
		esac
	done
	[[ -z $DB_NAME ]] && echo "Database name can not be empty." && exit 1
	[[ -z $DB_TABLE_LOG ]] && echo "Tablename for logging can not be empty." && exit 1
	[[ -z $DB_TABLE_ENTRY ]] && echo "Tablename for entries can not be empty." && exit 1
	[[ -z $DB_PASS ]] && echo "Userpassword can not be empty." && exit 1
	[[ $DB_USER ]] || DB_USER=$DB_NAME
	[[ $DB_HOST ]] || DB_HOST='localhost'
}

function createAMySqlDb() {
	SQLCommand1="DROP DATABASE IF EXISTS ${DB_NAME};"
	SQLCommand2="CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
	SQLCommand3="USE ${DB_NAME};"
	SQLCommand4="DROP USER IF EXISTS '${DB_USER}'@'%';"
	SQLCommand5="CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASS}';"
	SQLCommand6="GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';"
	SQLCommand7="FLUSH PRIVILEGES;"

	if [ -f /root/.my.cnf ]; then
		$BIN_MYSQL -e "${SQLCommand1}${SQLCommand2}${SQLCommand3}${SQLCommand4}${SQLCommand5}${SQLCommand6}${SQLCommand7}"
	else
		input "Enter MySQL root user password, please!"
		#read rootPassword
		$BIN_MYSQL -h $DB_HOST -u root -p -e "${SQLCommand1}${SQLCommand2}${SQLCommand3}${SQLCommand4}${SQLCommand5}${SQLCommand6}${SQLCommand7}"
	fi
}

function createLoginTable(){
	SQLCommand1="CREATE TABLE ${DB_NAME}.${DB_TABLE_LOG} (
	myuser_id BIGINT NOT NULL AUTO_INCREMENT,
	myuser_name VARCHAR(30) NOT NULL,
	myuser_username VARCHAR(30) NOT NULL,
	myuser_password VARCHAR(255) NOT NULL,
	PRIMARY KEY(myuser_id) );"

	
	if [ -f /root/.my.cnf ]; then
		$BIN_MYSQL -e "${SQLCommand1}"
	else
		input "Enter MySQL root user password, please!"
		#read rootPassword
		$BIN_MYSQL -h $DB_HOST -u root -p -e "${SQLCommand1}"
	fi
}

function createEntryTable() {
	SQLCommand1="CREATE TABLE ${DB_NAME}.${DB_TABLE_ENTRY}(
	entry_id int(11) NOT NULL AUTO_INCREMENT,
	entry_name VARCHAR(30) DEFAULT NULL,
	entry_surname VARCHAR(30) DEFAULT NULL,
	entry_age int(3) DEFAULT 0,
	entry_email VARCHAR(45) DEFAULT 'fm@bla.com',
	entry_street VARCHAR(30) DEFAULT NULL,
	entry_houseno VARCHAR(30) DEFAULT NULL,
	entry_postalcode VARCHAR(10) DEFAULT NULL,
	entry_phonenumber VARCHAR(30) DEFAULT NULL,
	PRIMARY KEY(entry_id) );"


	if [ -f /root/.my.cnf ]; then
		$BIN_MYSQL -e "${SQLCommand1}"
	else
		input "Enter MySQL root user password, please!"
		#read rootPassword
		$BIN_MYSQL -h $DB_HOST -u root -p -e "${SQLCommand1}"
	fi
}

export LC_CTYPE=C
export LANG=C

VERSION="0.0.1"

BIN_MYSQL=$(which mysql)

DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=
DB_TABLE_LOG=
DB_TABLE_ENTRY=

function main(){

	sucop "Processing arguments ..."
	parseArgs "$@"
	sucop "Done!"

	sucop "Creating MySQL db and user ..."
	createAMySqlDb
	sucop "Done!"

	sucop "Creating MySQL db Table for logging..."
	createLoginTable
	sucop "Done!"

	sucop "Creating MySQL db Table for entries ..."
	createEntryTable
	sucop "Done!"

	printStatusSuccess

	exit 0
}

main "$@"
