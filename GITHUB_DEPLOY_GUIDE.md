# 🚀 Django抽奖系统 - GitHub部署指南

## 📋 快速部署清单

### ✅ 已准备的文件
- [x] `Dockerfile` - Docker镜像构建文件
- [x] `Dockerfile.production` - 生产环境Dockerfile
- [x] `docker-compose.yml` - Docker Compose配置
- [x] `deploy.sh` - 自动部署脚本
- [x] `nginx.conf` - Nginx配置文件
- [x] `nginx-docker.conf` - Docker环境Nginx配置
- [x] `gunicorn.conf.py` - Gunicorn配置文件
- [x] `.github/workflows/deploy.yml` - GitHub Actions自动部署
- [x] `DEPLOYMENT_GUIDE.md` - 详细部署文档

### 🎯 部署选项

## 方案1：GitHub + 传统服务器（推荐）

### 步骤1：创建GitHub仓库
```bash
# 进入项目目录
cd wxcloudrun-django-main

# 初始化Git仓库（如果未安装Git，请先安装）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Django lottery system with WeChat integration"

# 添加远程仓库（替换为你的GitHub仓库URL）
git remote add origin https://github.com/YOUR_USERNAME/wxcloudrun-django-lottery.git

# 推送到GitHub
git push -u origin main
```

### 步骤2：服务器部署
```bash
# 1. 登录你的服务器
ssh user@your-server-ip

# 2. 安装Git（如果未安装）
sudo apt update && sudo apt install git -y

# 3. 克隆项目
git clone https://github.com/YOUR_USERNAME/wxcloudrun-django-lottery.git

# 4. 进入项目目录
cd wxcloudrun-django-lottery

# 5. 运行自动部署脚本
chmod +x deploy.sh
./deploy.sh
```

## 方案2：GitHub + Docker部署

### 步骤1：推送到GitHub（同上）

### 步骤2：Docker部署
```bash
# 1. 登录服务器并克隆项目
ssh user@your-server-ip
git clone https://github.com/YOUR_USERNAME/wxcloudrun-django-lottery.git
cd wxcloudrun-django-lottery

# 2. 安装Docker和Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo apt install docker-compose -y

# 3. 启动Docker容器
docker-compose up -d

# 4. 查看状态
docker-compose ps
docker-compose logs
```

## 方案3：GitHub Actions自动部署

### 步骤1：设置GitHub Secrets
在GitHub仓库设置中添加以下Secrets：
- `SERVER_HOST` - 服务器IP地址
- `SERVER_USERNAME` - SSH用户名
- `SERVER_PASSWORD` - SSH密码
- `SERVER_PORT` - SSH端口（默认22）

### 步骤2：推送代码触发部署
```bash
# 推送代码到GitHub后，GitHub Actions会自动部署
git add .
git commit -m "Update: trigger auto deployment"
git push origin main
```

## 🌍 域名和SSL配置

### 域名设置
1. 购买域名（如：your-domain.com）
2. 设置DNS A记录指向你的服务器IP
3. 等待DNS生效（通常几分钟到几小时）

### SSL证书（Let's Encrypt）
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 设置自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 环境变量配置

### 创建.env文件
```bash
# 在项目目录创建.env文件
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
WECHAT_APPID=your-wechat-appid
WECHAT_APPSECRET=your-wechat-appsecret
DATABASE_URL=sqlite:///db.sqlite3
TIME_ZONE=Asia/Shanghai
EOF
```

### 重要配置项
- `SECRET_KEY`：Django安全密钥（必须修改）
- `WECHAT_APPID`：微信应用ID
- `WECHAT_APPSECRET`：微信应用密钥
- `ALLOWED_HOSTS`：允许访问的域名

## 📊 监控和维护

### 查看服务状态
```bash
# 查看Gunicorn状态
sudo systemctl status gunicorn

# 查看Nginx状态
sudo systemctl status nginx

# 查看日志
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/error.log
```

### 更新部署
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

## 🚨 故障排除

### 常见问题解决

**1. 端口冲突**
```bash
# 检查端口占用
sudo netstat -tulnp | grep :80
sudo netstat -tulnp | grep :8000

# 停止占用进程
sudo systemctl stop apache2  # 如果Apache占用80端口
```

**2. 权限问题**
```bash
# 修复文件权限
sudo chown -R www-data:www-data /var/www/wxcloudrun-django
sudo chmod -R 755 /var/www/wxcloudrun-django
```

**3. 数据库错误**
```bash
# 重新创建数据库
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

**4. 静态文件问题**
```bash
# 重新收集静态文件
python manage.py collectstatic --noinput
```

## 📞 获取帮助

### 检查日志文件
- Gunicorn日志：`/var/log/gunicorn/error.log`
- Nginx日志：`/var/log/nginx/error.log`
- 系统日志：`journalctl -u gunicorn -f`

### 测试API接口
```bash
# 测试授权URL接口
curl -X POST http://your-domain.com/api/wechat/auth_url \
  -H "Content-Type: application/json" \
  -d '{"redirect_uri":"http://your-domain.com/wechat/callback","state":"test","scope":"snsapi_userinfo"}'

# 测试计数器接口
curl -X POST http://your-domain.com/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"inc"}'
```

## 🎯 验证部署成功

### 访问测试
1. 主页：`http://your-domain.com`
2. API测试：`http://your-domain.com/api/count`
3. 微信授权：`http://your-domain.com/api/wechat/auth_url`

### 成功标志
- ✅ 主页正常显示
- ✅ API接口返回JSON数据
- ✅ 静态文件加载正常
- ✅ 微信授权URL生成成功
- ✅ 抽奖功能正常工作

## 🚀 恭喜！部署完成

你的Django抽奖系统已成功部署到服务器！

### 下一步建议
1. 配置微信开放平台
2. 设置数据库备份
3. 配置监控告警
4. 优化性能
5. 添加更多功能

### 相关文件
- 📋 [详细部署文档](DEPLOYMENT_GUIDE.md)
- 🔧 [部署脚本](deploy.sh)
- 🐳 [Docker配置](docker-compose.yml)
- ⚙️ [Nginx配置](nginx.conf)

祝你的抽奖系统运行顺利！🎉