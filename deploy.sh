#!/bin/bash

# Django项目部署脚本
# 适用于Ubuntu/Debian系统

set -e

echo "🚀 开始部署Django项目..."

# 更新系统
echo "📦 更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装必要软件
echo "🔧 安装必要软件..."
sudo apt install -y python3-pip python3-venv nginx git curl

# 创建项目目录
echo "📁 创建项目目录..."
PROJECT_DIR="/var/www/wxcloudrun-django"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 克隆项目（如果使用Git）
# echo "📥 克隆项目..."
# git clone YOUR_GITHUB_URL $PROJECT_DIR

# 复制项目文件（如果使用本地文件）
echo "📂 复制项目文件..."
cp -r . $PROJECT_DIR/

# 进入项目目录
cd $PROJECT_DIR

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 数据库迁移
echo "🗄️ 数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
echo "📋 收集静态文件..."
python manage.py collectstatic --noinput

# 创建日志目录
echo "📝 创建日志目录..."
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/log/nginx
sudo chown $USER:$USER /var/log/gunicorn
sudo chown $USER:$USER /var/log/nginx

# 配置Gunicorn
echo "⚙️ 配置Gunicorn..."
sudo cp gunicorn.conf.py /etc/gunicorn.conf.py
sudo sed -i "s|/path/to/your/project|$PROJECT_DIR|g" /etc/gunicorn.conf.py

# 创建Gunicorn systemd服务
echo "🔧 创建Gunicorn服务..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config /etc/gunicorn.conf.py wxcloudrun.wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 配置Nginx
echo "🌐 配置Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/wxcloudrun-django
sudo sed -i "s|/path/to/your/project|$PROJECT_DIR|g" /etc/nginx/sites-available/wxcloudrun-django
sudo sed -i "s|your-domain.com|localhost|g" /etc/nginx/sites-available/wxcloudrun-django

# 启用Nginx配置
sudo ln -sf /etc/nginx/sites-available/wxcloudrun-django /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
echo "🔍 测试Nginx配置..."
sudo nginx -t

# 启动服务
echo "🚀 启动服务..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx

# 防火墙配置（如果需要）
# sudo ufw allow 'Nginx Full'

echo "✅ 部署完成！"
echo "📊 服务状态："
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager

echo "🌐 访问地址：http://localhost"
echo "📋 日志文件："
echo "  - Gunicorn: /var/log/gunicorn/error.log"
echo "  - Nginx: /var/log/nginx/error.log"