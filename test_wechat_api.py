#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试微信API接口
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_auth_url():
    """测试获取微信授权URL接口"""
    print("=== 测试获取微信授权URL ===")
    
    # 测试标准格式
    url = f"{BASE_URL}/api/wechat/auth_url"
    data = {
        "redirect_uri": "http://127.0.0.1:8082/wechat/callback",
        "state": "test_state_123",
        "scope": "snsapi_userinfo"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析结果: {result}")
            if result.get('errcode') == 0:
                print("✅ 获取授权URL成功")
                print(f"授权URL: {result.get('auth_url')}")
            else:
                print(f"❌ 获取授权URL失败: {result.get('errmsg')}")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print()

def test_auth_url_cloud_format():
    """测试云托管格式获取微信授权URL"""
    print("=== 测试云托管格式获取微信授权URL ===")
    
    url = f"{BASE_URL}/api/wechat/auth_url"
    data = {
        "config": {
            "env": "test"
        },
        "data": {
            "redirect_uri": "http://127.0.0.1:8082/wechat/callback",
            "state": "test_state_123",
            "scope": "snsapi_userinfo"
        }
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析结果: {result}")
            if result.get('errcode') == 0:
                print("✅ 云托管格式获取授权URL成功")
                print(f"授权URL: {result.get('auth_url')}")
            else:
                print(f"❌ 云托管格式获取授权URL失败: {result.get('errmsg')}")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print()

def test_user_info():
    """测试获取微信用户信息接口（模拟）"""
    print("=== 测试获取微信用户信息 ===")
    
    url = f"{BASE_URL}/api/wechat/user_info"
    data = {
        "code": "test_code_123",
        "state": "test_state_123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析结果: {result}")
            if result.get('errcode') == 0:
                print("✅ 获取用户信息成功")
                print(f"用户信息: {result.get('user_info')}")
            else:
                print(f"❌ 获取用户信息失败: {result.get('errmsg')}")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print()

def test_user_info_cloud_format():
    """测试云托管格式获取微信用户信息"""
    print("=== 测试云托管格式获取微信用户信息 ===")
    
    url = f"{BASE_URL}/api/wechat/user_info"
    data = {
        "config": {
            "env": "test"
        },
        "data": {
            "code": "test_code_123",
            "state": "test_state_123"
        }
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析结果: {result}")
            if result.get('errcode') == 0:
                print("✅ 云托管格式获取用户信息成功")
                print(f"用户信息: {result.get('user_info')}")
            else:
                print(f"❌ 云托管格式获取用户信息失败: {result.get('errmsg')}")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print()

def test_existing_apis():
    """测试现有的API接口"""
    print("=== 测试现有API接口 ===")
    
    # 测试计数器接口
    counter_url = f"{BASE_URL}/api/count"
    
    try:
        # GET请求
        response = requests.get(counter_url)
        print(f"计数器GET状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"计数器GET响应: {response.json()}")
        
        # POST请求
        response = requests.post(counter_url)
        print(f"计数器POST状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"计数器POST响应: {response.json()}")
            
    except Exception as e:
        print(f"❌ 计数器测试异常: {e}")
    
    print()

def main():
    """主测试函数"""
    print("🚀 开始测试微信API接口")
    print(f"API基础URL: {BASE_URL}")
    print("=" * 50)
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 测试现有API
    test_existing_apis()
    
    # 测试微信API
    test_auth_url()
    test_auth_url_cloud_format()
    test_user_info()
    test_user_info_cloud_format()
    
    print("=" * 50)
    print("✅ 测试完成")

if __name__ == "__main__":
    main()