#!/usr/bin/env bash

function read_ini_file()
{
	Key=$1
	Section=$2
  	Configfile=$3
	ReadINI=`awk -F '=' '/\['$Section'\]/{a=1}a==1&&$1~/'$Key'/{print $2;exit}' $Configfile`
 	echo "$ReadINI"
}
