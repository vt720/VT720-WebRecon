# VT720-WebRecon

> **HTTP 资产指纹识别与 Web 信息收集引擎**
> by **VT720**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-green.svg)](../../releases)

一个轻量级的 **HTTP 资产指纹识别与 Web 信息收集工具**。

支持单目标与批量扫描，自动规范化 URL，可选择跟随或禁止重定向，并将扫描结果导出为结构化 JSON 报告。

**零配置文件，纯命令行驱动，开箱即用。**

> 🚧 **项目状态：** 项目目前处于早期阶段（`v0.1`），功能与代码结构仍在持续迭代中，欢迎提交 Issue 与 Pull Request。
>
> ⚠️ **安全声明：** 本工具仅供网络安全学习、授权渗透测试和自有资产安全自查使用，请勿将其用于任何未经授权的扫描行为。

---

## ✨ 功能特性

* 🔍 **HTTP 资产指纹识别**
  提取 `Server`、中间件、Web 框架、CMS 等相关信息。

* 📥 **单目标 / 批量扫描**
  支持 IP、域名、URL 混合输入。

* ⚡ **多线程并发**
  批量扫描模式支持自定义最大并发数，提高扫描效率。

* 🔗 **URL 自动规范化**
  对缺少协议的目标自动补全 `http://` 前缀。

* ↪️ **重定向可控**
  默认跟随 HTTP 重定向并记录跳转链，也可以通过参数禁止跟随重定向，直接获取原始 `301/302` 响应。

* 🔒 **忽略 SSL 证书校验**
  支持自签名、过期或无效证书，并可屏蔽 `urllib3` 相关告警。

* 🎭 **高仿真 User-Agent**
  内置现代浏览器 User-Agent，可自定义 UA。

* 📄 **结构化 JSON 报告**
  支持将扫描结果导出为 JSON，方便后续分析、处理与集成。

* 🧩 **零配置**
  所有参数均通过命令行控制，无需额外配置文件。

---

## 📦 环境要求

* **Python 3.8+**
* 第三方依赖：

  * `requests`

---

## 🔧 安装

### 1. 克隆仓库

```bash
git clone https://github.com/vt720/VT720-WebRecon.git
cd VT720-WebRecon
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 使用方法

### 基本语法

```bash
python vt720_webrecon.py -u <目标URL> [选项]
```

或者使用批量目标：

```bash
python vt720_webrecon.py -f <目标文件> [选项]
```

---

## ⚙️ 参数说明

| 参数                  | 说明                           | 是否必填 | 默认值      |
| :------------------ | :--------------------------- | :--: | :------- |
| `-u, --url URL`     | 目标 URL，自动补全 `http://` 前缀     |  二选一 | -        |
| `-f, --file FILE`   | 批量目标文件，支持 IP / 域名 / URL 列表   |  二选一 | -        |
| `-c, --concurrency` | 批量模式最大并发数                    |   ❌  | `20`     |
| `--timeout`         | HTTP 请求超时时间，单位：秒             |   ❌  | `5.0`    |
| `-a, --user-agent`  | 自定义 User-Agent               |   ❌  | 内置浏览器 UA |
| `--no-redirect`     | 禁止跟随重定向，抓取原始 `301/302` 响应    |   ❌  | 跟随重定向    |
| `-k, --insecure`    | 忽略 SSL 证书校验，并屏蔽 `urllib3` 告警 |   ❌  | 校验证书     |
| `-o, --output`      | 导出结构化 JSON 报告                |   ❌  | 不导出      |

> `-u` 和 `-f` 至少提供一个。

---

## 💻 使用示例

### 1️⃣ 扫描单个目标

```bash
python vt720_webrecon.py -u http://example.com
```

---

### 2️⃣ 批量扫描

默认最大并发数为 `20`：

```bash
python vt720_webrecon.py -f targets.txt
```

`targets.txt` 示例：

```text
example.com
https://test.com
192.168.1.1
10.0.0.0/24
```

> 支持 IP、域名和 URL 混合输入。

---

### 3️⃣ 批量扫描 + 高并发 + 自定义 UA

```bash
python vt720_webrecon.py -f targets.txt -c 50 -a "Mozilla/5.0 ..."
```

---

### 4️⃣ 忽略 SSL 证书 + 禁止重定向 + 导出报告

```bash
python vt720_webrecon.py -u https://example.com -k --no-redirect -o report.json
```

---

## 📤 输出说明

### 终端输出

扫描过程中会实时显示每个目标的 HTTP 请求及指纹识别结果。

### JSON 文件输出

使用 `-o` 参数可以将扫描结果保存为结构化 JSON 文件：

```bash
python vt720_webrecon.py -u https://example.com -o report.json
```

生成的 JSON 数据结构示例如下：

```json
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
```

---

## 📊 JSON 字段说明

| 字段                 | 类型       | 说明                  |
| :----------------- | :------- | :------------------ |
| `url`              | `string` | 规范化后的目标 URL         |
| `final_url`        | `string` | 最终请求落地的 URL（跟随重定向后） |
| `status_code`      | `int`    | HTTP 响应状态码          |
| `response_time_ms` | `float`  | HTTP 请求响应耗时         |
| `title`            | `string` | 页面 `<title>` 内容     |
| `server`           | `string` | `Server` 响应头        |
| `powered_by`       | `string` | `X-Powered-By` 响应头  |
| `redirect_chain`   | `array`  | HTTP 重定向跳转链         |
| `cookie_security`  | `array`  | Cookie 安全相关标记信息     |

> **注意：** JSON 字段及数据结构可能会随着项目版本迭代发生变化，请以当前版本代码及 README 为准。

---

## 🗂️ 项目结构

```text
VT720-WebRecon/
├── vt720_webrecon.py      # 主程序
├── README.md              # 项目说明
├── DISCLAIMER.md          # 免责声明
├── CHANGELOG.md           # 版本记录
├── LICENSE                # MIT 开源协议
├── requirements.txt       # Python 依赖清单
└── .gitignore             # Git 忽略规则
```

---

## 🛡️ 免责声明

1. 本工具仅供**网络安全学习、授权渗透测试**和**自有资产安全自查**使用。
2. 使用者必须确保对扫描目标拥有合法、有效的授权。
3. 严禁将本工具用于任何未经授权的资产扫描、攻击或其他非法用途。
4. 因使用本工具产生的一切法律责任，由使用者自行承担，与作者及项目维护者无关。

详细内容请参阅：

[DISCLAIMER.md](DISCLAIMER.md)

---

## 📄 License

本项目基于 **MIT License** 开源。

详见：

[LICENSE](LICENSE)

---

## ⭐ 项目信息

**VT720-WebRecon** 是一个面向网络安全学习与授权资产安全检查场景的轻量级 Web 信息收集工具。

如果这个项目对你有帮助，欢迎提交 **Issue**、**Pull Request** 或给项目点一个 ⭐ **Star**。

> **VT720-WebRecon · Web Reconnaissance & Fingerprinting**
