#!/usr/bin/env bash
# 项目初始换脚本
cd `dirname $0`

# 虚拟环境路径 需要修改
env_path="/home/huangxing/python_env/gather-city_env"

echo "${env_path}/bin/activate"
source ${env_path}/bin/activate
pwd
# 安装 python 的第三方依赖库
pip install -r ../requirements.txt
例如:pip install -i http://pypi.douban.com/simple/ -r /srv/requirements.txt

source ./init_db.sh
