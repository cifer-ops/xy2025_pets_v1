#!/bin/bash
set -e

# 设置变量
PROJECT_NAME="xy_pets"
PROJECT_PATH="/var/www/$PROJECT_NAME"
NGINX_AVAILABLE="/etc/nginx/sites-available/$PROJECT_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$PROJECT_NAME"

echo "开始部署 $PROJECT_NAME..."

# 1. 创建项目目录
echo "创建项目目录..."
mkdir -p $PROJECT_PATH
cd $PROJECT_PATH

# 2. 设置目录权限
echo "设置目录权限..."
chown -R www-data:www-data $PROJECT_PATH
chmod -R 755 $PROJECT_PATH

# 3. 创建并激活虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 4. 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 5. 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 6. 配置MySQL数据库
echo "创建数据库..."
mysql -u root -p020117Xyz -e "CREATE DATABASE IF NOT EXISTS xy_pets_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 7. 执行迁移
echo "执行数据库迁移..."
python manage.py migrate

# 8. 创建超级用户（可选）
# python manage.py createsuperuser

# 9. 设置Gunicorn服务
echo "设置Gunicorn服务..."
cp gunicorn.service /etc/systemd/system/$PROJECT_NAME.service
systemctl daemon-reload
systemctl start $PROJECT_NAME
systemctl enable $PROJECT_NAME

# 10. 设置Nginx
echo "设置Nginx..."
cp xy_pets_nginx.conf $NGINX_AVAILABLE
if [ ! -f "$NGINX_ENABLED" ]; then
    ln -s $NGINX_AVAILABLE $NGINX_ENABLED
fi

# 11. 测试Nginx配置
echo "测试Nginx配置..."
nginx -t

# 12. 重启Nginx
echo "重启Nginx..."
systemctl restart nginx

echo "部署完成！项目可通过 http://134.209.40.24:3333 访问" 