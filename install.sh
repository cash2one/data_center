#!/bin/sh
currDir=$(cd "$(dirname "$0")"; pwd)
proPath="${currDir}"/../

if [ $1_ == "_" ]
then
    echo "Usage: sh install.sh clean    清除当前环境中的配置及中间文件"
    echo "       sh install.sh prd      安装线上环境"
    echo "       sh install.sh dev      安装开发环境"
    exit 1
fi

if [ $1_ == "dev_" ]
then
    ln -s "${proPath}/data_center/data_spider/conf/dev/set_env.py" "${proPath}/data_center/data_spider/conf/"
    ln -s "${proPath}/data_center/user_center/conf/dev/settings.py" "${proPath}/data_center/user_center/conf/"

elif [ $1_ == "prd_" ]
then
    ln -s "${proPath}/data_center/user_center/conf/prd/set_env.py" "${proPath}/data_center/user_center/conf/"
    ln -s "${proPath}/data_center/user_center/conf/prd/settings.py" "${proPath}/data_center/user_center/conf/"


elif [ $1_ == "clean_" ]
then
    find $proPath -name "*.pyc" | xargs rm -f

    rm -f "${proPath}/data_center/data_spider/conf/set_env.py"
    rm -f "${proPath}/data_center/user_center/conf/settings.py"
elif [ "" == "" ]
then
    echo "警告: 参数1非法"
    exit 1
fi
