#!/usr/bin/env bash

source libs.sh

cur_dir=`dirname $0`
cd ${cur_dir}
pwd

sql_dir="${cur_dir}/sql"

# 定义配置文件和项目路径
project_dir="${cur_dir}/../python-framework"
db_ini_path="$project_dir/config/db.ini"
env_ini_path="$project_dir/config/env.ini"


# 读取配置文件中 mysql 的配置;
sql_host=`read_ini_file "host" "db" ${db_ini_path}`
sql_port=`read_ini_file "port" "db" ${db_ini_path}`
sql_user=`read_ini_file "user" "db" ${db_ini_path}`
sql_pass=`read_ini_file "pass" "db" ${db_ini_path}`

# 执行sql 初始化数据库;
sql="mysql -u${sql_user} -p${sql_pass} -h${sql_host} -P${sql_port}"

is_init_db=`${sql} < ${sql_dir}/create_db.sql`
is_gather_city_db=`${sql} --database=python-framework < ${sql_dir}/gather_city.sql`
is_init_admin_user=`${sql} --database=python-framework < ${sql_dir}/init_admin_user.sql`
is_init_admin_user=`${sql} --database=python-framework < ${sql_dir}/city.sql`

if [[ "$?" == "0" ]];
then
   echo "init_db ok."
fi
