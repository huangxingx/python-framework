
### 初始化项目 ###
1. 修改 gather_city/config/db.ini 配置文件，改好数据库配置;
2. 修改 gather_city/scripts/init.sh 中 env_path 变量;
2. 执行 gather_city/scripts/init.sh ;


### 文件详解 ###
* init.sh 初始化项目脚本;
* libs.sh shell 库脚本
* init_db.sh 初始化数据库脚本;
* sql/city.sql 城市表数据sql;
* sql/create_db.sql 创建数据库sql;
* sql/gather_city.sql 项目表结构sql;
* sql/init_admin_user.sql 初始化admin sql;
* sql/migration/* 数据库迁移sql;
