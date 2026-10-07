# VT720-WebRecon

> HTTP 资产指纹识别与 Web 信息收集引擎
> 🚧 项目处于早期阶段（v0.1），功能和代码结构仍在迭代中，欢迎 issue 与 PR。
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-green.svg)](../../releases)

`VT720-WebRecon` 是一个轻量级的 HTTP 资产指纹识别与 Web 信息收集工具。
支持单目标与批量扫描，自动规范化 URL，可选跟随或禁止重定向，
并将结果导出为结构化 JSON 报告。零配置文件，纯命令行驱动。

## ✨ 特性

- 🔍 **HTTP 资产指纹识别** —— Server / 中间件 / 框架 / CMS 等信息提取
- 📥 **单目标或批量输入** —— 支持 IP、域名、URL 混合列表
- ⚡ **多线程并发** —— 批量模式可自定义并发数，默认 20
- 🔗 **URL 自动规范化** —— 缺省协议时自动补全 `http://`
- ↪️ **重定向可控** —— 默认跟随并记录跳转链，或抓取原始 301/302 报文
- 🔒 **忽略证书校验** —— 支持自签名 / 过期 / 无效证书，并屏蔽 urllib3 告警
- 🎭 **高仿真 UA** —— 内置现代浏览器 User-Agent，避免暴露脚本特征
- 📄 **结构化 JSON 报告** —— 一键导出，便于后续处理与集成
- 🧩 **零配置** —— 全部通过命令行参数控制，开箱即用

## 📦 安装

```bash
git clone https://github.com/vt720/VT720-WebRecon.git
cd VT720-WebRecon
pip install -r requirements.txt
环境要求：Python 3.8+，依赖 requests。

🚀 使用方法
基本用法
bash
python vt720_webrecon.py -u http://example.com

批量扫描
bash
python vt720_webrecon.py -f targets.txt -c 30
targets.txt 示例（IP / 域名 / URL 可混合）：

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
--timeout SEC	HTTP 请求超时时间（默认 5.0 秒）
-a, --user-agent UA	自定义 User-Agent
--no-redirect	禁止跟随重定向，抓取 301/302 原始报文
-k, --insecure	忽略 SSL 证书校验，并屏蔽 urllib3 告警
-o, --output FILE	导出结构化 JSON 报告


示例
bash
# 忽略证书 + 不跟随重定向 + 导出报告
python vt720_webrecon.py -u https://example.com -k --no-redirect -o report.json

# 批量 + 高并发 + 自定义 UA
python vt720_webrecon.py -f targets.txt -c 50 -a "Mozilla/5.0 ..." -o report.json


📊 输出示例
使用 -o report.json 导出的结构化报告示例：

json
[
  {
    "url": "http://192.168.1.1",
    "final_url": "http://192.168.100.100",
    "status_code": 200,
    "response_time_ms": 0.06409573554992676,
    "title": "H61G",
    "server": "Mini web server.",
    "powered_by": "",
    "redirect_chain": [],
    "cookie_security": []
  }
]
字段说明
字段	类型	说明
url	string	规范化后的目标 URL
final_url	string	最终请求落地的 URL（跟随重定向后）
status_code	int	HTTP 响应状态码
response_time_ms	float	响应耗时（秒）
title	string	页面 <title> 内容
server	string	Server 响应头
powered_by	string	X-Powered-By 响应头
redirect_chain	array	重定向跳转链（--no-redirect 时为空）
cookie_security	array	安全性相关的 Cookie 标记信息
⚠️ 字段以后续版本为准，若脚本结构有更新，README 会同步维护。

🛡️ 免责声明
本项目仅供 安全研究、授权渗透测试、企业资产梳理、教学演示 等合法用途。

使用者需自行确保对目标拥有合法授权。任何未经授权的扫描、探测或信息收集行为均与本项目作者无关，由此产生的一切后果由使用者自行承担。

详见 DISCLAIMER.md。

📄 License
MIT
