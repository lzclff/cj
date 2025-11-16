# Django微信云托管项目部署指南

## 🚀 快速开始

### 1. GitHub仓库设置

#### 创建新仓库
1. 登录GitHub
2. 点击右上角的 "+" → "New repository"
3. 命名仓库（例如：wxcloudrun-django-lottery）
4. 选择 "Public" 或 "Private"
5. 不要初始化README（我们会推送现有代码）
6. 点击 "Create repository"

#### 推送代码到GitHub
```bash
# 安装Git（如果未安装）
# Windows: 下载并安装 Git for Windows
# Ubuntu: sudo apt install git

# 进入项目目录
cd wxcloudrun-django-main

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Django lottery system"

# 添加远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送到GitHub
git push -u origin main
```

### 2. 服务器部署选项

#### 选项A：传统服务器部署（推荐）

##### 系统要求
- Ubuntu 20.04+ / Debian 10+
- Python 3.8+
- Nginx
- 2GB+ RAM
- 10GB+ 存储空间

##### 自动部署
```bash
# 上传项目到服务器
scp -r wxcloudrun-django-main user@your-server:/home/user/

# SSH登录服务器
ssh user@your-server

# 进入项目目录
cd /home/user/wxcloudrun-django-main

# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

##### 手动部署步骤
```bash
# 1. 系统更新
sudo apt update && sudo apt upgrade -y

# 2. 安装必要软件
sudo apt install -y python3-pip python3-venv nginx git curl

# 3. 创建项目目录
sudo mkdir -p /var/www/wxcloudrun-django
sudo chown $USER:$USER /var/www/wxcloudrun-django

# 4. 复制项目文件
cp -r . /var/www/wxcloudrun-django/
cd /var/www/wxcloudrun-django

# 5. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 6. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 7. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 8. 收集静态文件
python manage.py collectstatic --noinput

# 9. 配置Gunicorn
sudo cp gunicorn.conf.py /etc/gunicorn.conf.py

# 10. 创建Gunicorn服务
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# 11. 配置Nginx
sudo cp nginx.conf /etc/nginx/sites-available/wxcloudrun-django
sudo ln -sf /etc/nginx/sites-available/wxcloudrun-django /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 选项B：Docker部署

##### 构建镜像
```bash
# 构建Docker镜像
docker build -t wxcloudrun-django .

# 运行容器
docker run -d -p 80:80 --name wxcloudrun-django wxcloudrun-django
```

##### Docker Compose（推荐）
```bash
# docker-compose.yml
docker-compose up -d
```

#### 选项C：云平台部署

##### 微信云托管
```bash
# 安装微信云托管CLI
npm install -g @wxcloudrun/cli

# 登录
wxcloudrun login

# 部署
wxcloudrun deploy
```

##### 其他云平台
- **阿里云**：使用函数计算或容器服务
- **腾讯云**：使用云开发或容器服务
- **华为云**：使用云容器引擎

### 3. 环境变量配置

创建 `.env` 文件：
```bash
# Django设置
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost

# 微信配置
WECHAT_APPID=your-wechat-appid
WECHAT_APPSECRET=your-wechat-appsecret

# 数据库配置（如果使用外部数据库）
DATABASE_URL=sqlite:///db.sqlite3

# 其他配置
TIME_ZONE=Asia/Shanghai
```

### 4. 域名和SSL配置

#### 域名设置
1. 购买域名
2. 设置DNS解析到服务器IP
3. 等待DNS生效

#### SSL证书（Let's Encrypt）
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 5. 监控和维护

#### 日志监控
```bash
# 查看Gunicorn日志
tail -f /var/log/gunicorn/error.log

# 查看Nginx日志
tail -f /var/log/nginx/error.log

# 查看系统日志
journalctl -u gunicorn -f
journalctl -u nginx -f
```

#### 性能监控
```bash
# 系统资源
htop

# 网络连接
netstat -tulnp

# 磁盘使用
df -h
```

#### 备份策略
```bash
# 数据库备份
sqlite3 db.sqlite3 ".backup backup-$(date +%Y%m%d).db"

# 文件备份
tar -czf backup-$(date +%Y%m%d).tar.gz /var/www/wxcloudrun-django
```

### 6. 故障排除

#### 常见问题

**1. 服务无法启动**
```bash
# 检查端口占用
sudo netstat -tulnp | grep :8000
sudo netstat -tulnp | grep :80

# 检查服务状态
sudo systemctl status gunicorn
sudo systemctl status nginx
```

**2. 静态文件无法访问**
```bash
# 重新收集静态文件
python manage.py collectstatic --noinput

# 检查权限
ls -la /var/www/wxcloudrun-django/staticfiles/
```

**3. 数据库错误**
```bash
# 检查数据库文件
ls -la db.sqlite3

# 重新迁移
python manage.py makemigrations
python manage.py migrate
```

**4. 权限问题**
```bash
# 修复权限
sudo chown -R www-data:www-data /var/www/wxcloudrun-django
sudo chmod -R 755 /var/www/wxcloudrun-django
```

### 7. 更新部署

#### 代码更新
```bash
# 拉取最新代码
git pull origin main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 重启服务
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

#### 回滚操作
```bash
# 查看提交历史
git log --oneline

# 回滚到指定版本
git reset --hard COMMIT_HASH

# 重启服务
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 📞 技术支持

### 相关文件
- [部署脚本](deploy.sh)
- [Nginx配置](nginx.conf)
- [Gunicorn配置](gunicorn.conf.py)
- [GitHub Actions](.github/workflows/deploy.yml)

### 获取帮助
- 查看日志文件
- 检查系统资源
- 验证配置文件
- 测试API接口

## 🎯 下一步

1. 选择合适的部署方案
2. 配置服务器环境
3. 部署项目代码
4. 配置域名和SSL
5. 设置监控和备份
6. 进行最终测试

祝部署顺利！🚀