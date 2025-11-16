# 微信API集成指南

## 🎯 概述

本项目已将微信API功能集成到云托管Django框架中，支持微信网页授权登录功能。

## 🔧 配置说明

### 1. 微信配置
在 `wxcloudrun/settings.py` 中配置微信参数：

```python
# 微信配置
WECHAT_APPID = '你的微信AppID'
WECHAT_APPSECRET = '你的微信AppSecret'
```

### 2. 跨域配置
已添加跨域支持，允许所有来源访问：

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://你的云托管域名"
]
```

## 📡 API接口

### 1. 获取微信授权URL

**接口地址**: `/api/wechat/auth_url`

**请求方式**: POST/GET

**请求格式**: 

标准格式：
```json
{
    "redirect_uri": "回调地址",
    "state": "状态参数",
    "scope": "授权作用域"
}
```

云托管格式：
```json
{
    "config": {"env": "test"},
    "data": {
        "redirect_uri": "回调地址",
        "state": "状态参数", 
        "scope": "授权作用域"
    }
}
```

**响应格式**:
```json
{
    "errcode": 0,
    "errmsg": "success",
    "auth_url": "微信授权URL"
}
```

### 2. 获取微信用户信息

**接口地址**: `/api/wechat/user_info`

**请求方式**: POST/GET

**请求格式**:

标准格式：
```json
{
    "code": "授权码",
    "state": "状态参数"
}
```

云托管格式：
```json
{
    "config": {"env": "test"},
    "data": {
        "code": "授权码",
        "state": "状态参数"
    }
}
```

**响应格式**:
```json
{
    "errcode": 0,
    "errmsg": "success",
    "user_info": {
        "openid": "用户OpenID",
        "nickname": "用户昵称",
        "sex": "性别",
        "province": "省份",
        "city": "城市",
        "country": "国家",
        "headimgurl": "头像URL",
        "privilege": [],
        "unionid": "UnionID"
    }
}
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置微信参数

编辑 `wxcloudrun/settings.py`，设置你的微信AppID和AppSecret：

```python
WECHAT_APPID = '你的微信AppID'
WECHAT_APPSECRET = '你的微信AppSecret'
```

### 3. 运行服务

```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. 测试API

运行测试脚本：

```bash
python test_wechat_api.py
```

## 📋 测试示例

### 获取授权URL测试

```bash
curl -X POST http://127.0.0.1:8000/api/wechat/auth_url \
  -H "Content-Type: application/json" \
  -d '{
    "redirect_uri": "http://127.0.0.1:8082/wechat/callback",
    "state": "test_state",
    "scope": "snsapi_userinfo"
  }'
```

### 获取用户信息测试

```bash
curl -X POST http://127.0.0.1:8000/api/wechat/user_info \
  -H "Content-Type: application/json" \
  -d '{
    "code": "test_code",
    "state": "test_state"
  }'
```

## 🔍 调试与日志

所有微信API相关操作都会记录日志，日志文件位于：
- Windows: `C:\Users\你的用户名\wxcloudrun\logs\`
- Linux/Mac: `/root/wxcloudrun/logs/`

## ⚠️ 注意事项

1. **微信配置**: 确保正确配置微信AppID和AppSecret
2. **跨域设置**: 根据实际需求配置CORS_ALLOWED_ORIGINS
3. **网络访问**: 确保服务器能够访问微信服务器
4. **测试环境**: 建议在本地测试通过后再部署到云托管

## 🔧 故障排查

### 常见问题

1. **获取用户信息失败**
   - 检查授权码(code)是否有效
   - 确认微信配置是否正确
   - 查看日志获取详细错误信息

2. **跨域问题**
   - 检查CORS配置
   - 确认请求来源是否在允许列表中

3. **JSON解析错误**
   - 确保请求格式正确
   - 检查Content-Type头部

### 日志查看

```bash
# 查看实时日志
tail -f /root/wxcloudrun/logs/wxcloudrun.log
```

## 📚 相关文档

- [微信网页授权开发文档](https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html)
- [Django官方文档](https://docs.djangoproject.com/)
- [云托管文档](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/)

## 🤝 支持与反馈

如有问题，请检查日志文件或联系技术支持。