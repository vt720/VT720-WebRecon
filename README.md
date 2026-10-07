# VT720-WebRecon

> HTTP 资产指纹识别与 Web 信息收集引擎

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-green.svg)](../../releases)

`VT720-WebRecon` 是一个轻量级的 HTTP 资产指纹识别与 Web 信息收集工具，
支持单目标与批量扫描，自动规范化 URL，跟随/禁止重定向可选，
并可将结果导出为结构化 JSON 报告。

## ✨ 特性

- 🔍 HTTP 资产指纹识别（CMS / 框架 / 中间件 / Server 等）
- 📥 单 URL 或批量文件输入（IP / 域名 / URL 混合）
- ⚡ 多线程并发扫描，批量模式可调并发数
- 🔗 自动规范化 URL（补全 `http://` 前缀）
- ↪️ 可选跟随重定向并记录跳转链，或抓取原始 301/302 报文
- 🔒 可选忽略 SSL 证书校验（自签名 / 过期 / 无效证书）
- 🎭 内置高仿真现代浏览器 User-Agent，避免暴露脚本特征
- 📄 结构化 JSON 报告导出
- 🧩 零配置文件，纯命令行参数驱动

## 📦 安装

```bash
git clone https://github.com/vt720/VT720-WebRecon.git
cd VT720-WebRecon
pip install -r requirements.txt
依赖：Python 3.8+、requests

🚀 使用方法
基本用法
python vt720_webrecon.py -u http://example.com

批量扫描
python vt720_webrecon.py -f targets.txt -c 30
targets.txt 

示例：
text
example.com
https://test.com
192.168.1.1
10.0.0.0/24

完整参数
参数	说明
-u, --url URL	目标 URL，自动补全 http:// 前缀
-f, --file FILE	批量目标文件（IP / 域名 / URL 列表）
-c, --concurrency N	批量模式最大并发数（默认 20）
--timeout SEC	HTTP 请求超时（默认 5.0 秒）
-a, --user-agent UA	自定义 User-Agent
--no-redirect	禁止跟随重定向，抓取 301/302 原始报文
-k, --insecure	忽略 SSL 证书校验，并屏蔽 urllib3 告警
-o, --output FILE	导出结构化 JSON 报告

示例
# 忽略证书 + 不跟随重定向 + 导出报告
python vt720_webrecon.py -u https://example.com -k --no-redirect -o report.json

# 批量 + 高并发 + 自定义 UA
python vt720_webrecon.py -f targets.txt -c 50 -a "Mozilla/5.0 ..." -o report.json

🛡️ 免责声明
本项目仅供 安全研究、授权渗透测试、资产梳理 等合法用途。
使用者需自行确保对目标拥有合法授权。任何未经授权的扫描行为均与本项目作者无关。