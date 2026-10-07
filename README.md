markdown
# VT720-WebRecon

> HTTP 资产指纹识别与 Web 信息收集引擎
> by VT720

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-green.svg)](../../releases)

一个采用多线程并发方式，对指定 URL / IP / 域名进行 HTTP 资产指纹识别与 Web 信息收集的脚本引擎。

> ⚠️ 本工具仅供网络安全学习、授权渗透测试和自有资产自查使用。请勿用于任何未经授权的扫描行为。

## ✨ 功能特性

- 🔍 **HTTP 资产指纹识别** —— Server / 中间件 / 框架 / CMS 等信息提取
- 📥 **单目标或批量输入** —— 支持 IP、域名、URL 混合列表
- ⚡ **多线程并发** —— 批量模式可自定义并发数（默认 20）
- 🔗 **URL 自动规范化** —— 缺省协议时自动补全 `http://`
- ↪️ **重定向可控** —— 默认跟随并记录跳转链，或抓取原始 301/302 报文
- 🔒 **忽略证书校验** —— 支持自签名 / 过期 / 无效证书，并屏蔽 urllib3 告警
- 🎭 **高仿真 UA** —— 内置现代浏览器 User-Agent，避免暴露脚本特征
- 📄 **结构化 JSON 报告** —— 一键导出，便于后续处理与集成
- 🧩 **零配置** —— 全部通过命令行参数控制，开箱即用

## 📦 环境要求

- Python 3.8+
- 依赖第三方库：`requests`

## 🔧 安装

```bash
# 1. 克隆仓库
git clone https://github.com/vt720/VT720-WebRecon.git
cd VT720-WebRecon

# 2. 安装依赖
pip install -r requirements.txt
🚀 使用方法
bash
python vt720_webrecon.py -u <目标URL> [选项]
完整参数
参数	说明	是否必填	默认值
-u, --url URL	目标 URL，自动补全 http:// 前缀	二选一	-
-f, --file FILE	批量目标文件（IP / 域名 / URL 列表）	二选一	-
-c, --concurrency	批量模式最大并发数	❌	20
--timeout	HTTP 请求超时时间（秒）	❌	5.0
-a, --user-agent	自定义 User-Agent	❌	内置浏览器 UA
--no-redirect	禁止跟随重定向，抓取 301/302 原始报文	❌	跟随
-k, --insecure	忽略 SSL 证书校验，屏蔽 urllib3 告警	❌	关闭
-o, --output	导出结构化 JSON 报告	❌	关闭
使用示例
1️⃣ 扫描单个 URL

bash
python vt720_webrecon.py -u http://example.com
2️⃣ 批量扫描

bash
python vt720_webrecon.py -f targets.txt -c 30
targets.txt 示例（IP / 域名 / URL 可混合）：

text
example.com
https://test.com
192.168.1.1
10.0.0.0/24
3️⃣ 忽略证书 + 不跟随重定向

bash
python vt720_webrecon.py -u https://example.com -k --no-redirect
4️⃣ 批量 + 高并发 + 自定义 UA + 导出报告

bash
python vt720_webrecon.py -f targets.txt -c 50 -a "Mozilla/5.0 ..." -o report.json
📤 输出说明
终端输出：实时显示每个目标的识别结果与关键字段。

文件输出：携带 -o report.json 时，结果保存为结构化 JSON，结构如下：

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

🗂️ 项目结构
text
VT720-WebRecon/
├── vt720_webrecon.py    # 主程序
├── README.md            # 项目说明
├── LICENSE              # MIT 开源协议
├── requirements.txt     # 依赖清单
├── CHANGELOG.md         # 版本记录
├── DISCLAIMER.md        # 免责声明
└── .gitignore           # Git 忽略规则
⚠️ 免责声明
本工具仅供网络安全学习、授权渗透测试和自有资产自查使用。

使用者必须确保对扫描目标拥有合法授权，否则一切后果自负。

严禁将本工具用于任何未经授权的扫描、探测或信息收集行为。

因使用本工具产生的一切法律责任，由使用者自行承担，与作者无关。

详见 DISCLAIMER.md。

📄 License
本项目基于 MIT License 开源。
