# Django抽奖系统部署包

## 📦 包含的文件

### 核心配置文件
- `Dockerfile` - Docker镜像构建文件
- `Dockerfile.production` - 生产环境Dockerfile
- `docker-compose.yml` - Docker Compose配置
- `requirements.txt` - Python依赖包

### 部署脚本
- `deploy.sh` - 自动部署脚本（Ubuntu/Debian）
- `nginx.conf` - Nginx服务器配置
- `nginx-docker.conf` - Docker环境Nginx配置
- `gunicorn.conf.py` - Gunicorn WSGI配置

### GitHub集成
- `.github/workflows/deploy.yml` - GitHub Actions自动部署
- `.gitignore` - Git忽略文件

### 部署文档
- `GITHUB_DEPLOY_GUIDE.md` - GitHub部署快速指南
- `DEPLOYMENT_GUIDE.md` - 详细部署文档

## 🚀 快速部署步骤

### 1. 推送到GitHub
```bash
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

### 2. 服务器部署（选择一种方案）

#### 方案A：自动脚本部署（推荐）
```bash
# 登录服务器
ssh user@your-server-ip

# 克隆项目
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 进入项目目录
cd YOUR_REPO_NAME

# 运行自动部署脚本
chmod +x deploy.sh
./deploy.sh
```

#### 方案B：Docker部署
```bash
# 安装Docker和Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo apt install docker-compose -y

# 启动容器
docker-compose up -d
```

#### 方案C：手动部署
按照 `DEPLOYMENT_GUIDE.md` 中的详细步骤进行手动部署。

## 🔧 配置说明

### 环境变量
创建 `.env` 文件并配置：
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost
WECHAT_APPID=your-wechat-appid
WECHAT_APPSECRET=your-wechat-appsecret
```

### 域名配置
1. 修改 `nginx.conf` 中的 `server_name`
2. 配置DNS解析到服务器IP
3. 设置SSL证书（可选但推荐）

## 📊 服务验证

### 测试API接口
```bash
# 测试计数器接口
curl -X POST http://your-domain.com/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"inc"}'

# 测试微信授权接口
curl -X POST http://your-domain.com/api/wechat/auth_url \
  -H "Content-Type: application/json" \
  -d '{"redirect_uri":"http://your-domain.com/wechat/callback","state":"test"}'
```

### 访问地址
- 主页：`http://your-domain.com`
- 管理后台：`http://your-domain.com/admin`
- API文档：`http://your-domain.com/api/`

## 🎯 功能特点

### 已验证功能
- ✅ Django服务稳定运行
- ✅ 抽奖概率计算准确
- ✅ 微信授权接口正常
- ✅ 计数器功能正常
- ✅ 静态文件处理正常
- ✅ Docker容器化部署

### API端点
- `POST /api/count` - 计数器接口
- `POST /api/wechat/auth_url` - 微信授权URL
- `POST /api/wechat/user_info` - 微信用户信息

## 🚨 注意事项

### 安全建议
1. 修改默认的 `SECRET_KEY`
2. 配置 `ALLOWED_HOSTS`
3. 设置 `DEBUG=False`（生产环境）
4. 配置HTTPS/SSL证书
5. 定期更新依赖包

### 性能优化
1. 使用外部数据库（PostgreSQL/MySQL）
2. 配置CDN加速静态文件
3. 启用Gzip压缩
4. 设置合理的缓存策略

## 📞 故障排除

### 常见问题
1. **端口冲突**：检查80和8000端口
2. **权限问题**：修复文件权限
3. **依赖问题**：重新安装Python包
4. **数据库问题**：重新运行迁移

### 查看日志
```bash
# Gunicorn日志
tail -f /var/log/gunicorn/error.log

# Nginx日志
tail -f /var/log/nginx/error.log

# 系统日志
journalctl -u gunicorn -f
```

## 🎉 部署完成

恭喜！你的Django抽奖系统已成功部署！

### 下一步
1. 配置微信开放平台
2. 设置监控和告警
3. 配置自动备份
4. 优化性能
5. 添加更多功能

## 📚 相关文档

- [详细部署指南](DEPLOYMENT_GUIDE.md)
- [GitHub部署指南](GITHUB_DEPLOY_GUIDE.md)
- [项目README](README.md)

祝部署顺利，抽奖系统运行稳定！🚀