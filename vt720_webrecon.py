import requests
import re
import argparse
import ipaddress
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from http.cookies import SimpleCookie
from requests.compat import urljoin
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DomaincheckError(Exception):
    pass
class HttpScan():
    def __init__(self,url=None,file=None,concurrency=20,timeout=5.0,user_agent=None,no_redirect=True,insecure=False,output=None):
            self.url = url
            self.file = file
            self.concurrency = concurrency
            self.timeout = timeout
            self.user_agent = user_agent
            self.no_redirect = no_redirect
            self.insecure = insecure
            self.output = output


    def domain_check(self,url_0):
            is_have = False
            if "http://" in url_0 :
                url_1 = url_0[7:]
                is_have = True
                if "/" in url_1:
                    url = url_1.split("/")[0]
                else:
                    url = url_1
            elif "https://" in url_0:
                url_1 = url_0[8:]
                is_have = True
                if "/" in url_1:
                    url = url_1.split("/")[0] 
                else:
                    url = url_1
            else:
                url = url_0
            port_S = False
            domain_S = False
            is_ok = False

            if ":" in url:
                port = url.split(":")[1]
                domain = url.split(":")[0]
                try:
                    ipaddress.ip_address(domain)
                    domain_S = True
                except ValueError:
                    if "." in domain:
                        domain_list = domain.split(".")
                        domain_tlist = all([i.isascii() for i in domain_list])
                        if domain_tlist:
                            domain_S = True
                        else:
                            raise DomaincheckError(f"{url_0} 校验失败,不是一个合格的ip或域名，请检查后重新输入")
                            
                    elif domain.isalpha() and domain.isascii():
                        domain_S = True
                    else:
                        raise DomaincheckError(f"{url_0} 校验失败,不是一个合格的ip或域名，请检查后重新输入")
                        
                try:
                    if not(0 < int(port) <= 65535):
                        raise DomaincheckError(f"{url_0} 校验失败,端口范围有误，请检查后重新输入")
                        
                    else:
                        port_S = True
                except ValueError as V:
                    raise DomaincheckError(f"{url_0} 校验失败,端口必须为纯数字，请输入正确的端口")
                except DomaincheckError as D:
                    raise D
                if port_S and domain_S:
                    is_ok = True
            elif "." in url:
                try:
                    ipaddress.ip_address(url)
                    is_ok = True
                except ValueError:
                    domain_list2 = url.split(".")
                    domain_test2 = all([i.isascii() for i in domain_list2])
                    if domain_test2:
                        is_ok = True
                    else:
                        raise DomaincheckError(f"{url_0} 校验失败,不是一个合格的ip或域名，请检查后重新输入")
            else:
                if url.isalpha() and url.isascii():
                    is_ok = True
                else:
                    raise DomaincheckError(f"{url_0} 校验失败,不是一个合格的ip或域名，请检查后重新输入")
                    
            if is_have:
                if is_ok:
                    return url_0.lower()
            else:
                if is_ok:
                    return "http://" + url_0.lower()
            raise DomaincheckError(f"{url_0} 校验失败,不是一个合格的ip或域名，请检查后重新输入")



    def file_read(self,file_path):
        read_list = []
        with open(file_path,"r",encoding="utf-8") as f:
            for f1 in f:
                f2 = f1.strip()
                if f2 != "":
                    read_list.append(f2)
        return read_list


    def output_to_file(self,text):
        with open(self.output,"w",encoding="utf-8") as f1:
            json.dump(text,f1,ensure_ascii=False,indent=2)


    def request_do(self,ip):
        url = ip
        has_Httponly = False
        has_Secure = False
        is_safe = False
        cs = []
        redirect_chain = []
        start = time.time()
        headers = {"User-Agent": self.user_agent}
        try:
            req = requests.get(url=url,headers=headers,timeout=self.timeout,allow_redirects=self.no_redirect,verify=not(self.insecure),stream=True)
        except requests.exceptions.Timeout as e:
            print(f'连接超时,url :{ip}')
            return
        except requests.exceptions.TooManyRedirects:
            print(f'重定向次数超过 20,url :{ip}')
            return 
        except requests.exceptions.ConnectionError as e:
            print(f'连接失败,URL:, {ip}')
            return 
        except requests.exceptions.HTTPError as e:
            print(f'HTTP 错误,URL:, {ip}')
            return 
        except requests.exceptions.RequestException as e:
            print(f'其他请求错误,url :{ip}')
            return 
        end = time.time()
        final_url = url
        do_time = end - start
        req.encoding = req.apparent_encoding
        req_sc = req.status_code
        #req_len = req.headers.get("Content-Length")
        byt = bytearray()
        for chunk in req.iter_content(chunk_size=1024):
            if not chunk:
                continue
            byt.extend(chunk)
            if len(byt) >= 100*1024:
                break
        byte = bytes(byt)
        req_text = byte.decode(req.encoding,errors="replace")
        req_server=req.headers.get("server")
        req_xb = req.headers.get("X-Powered-By")
        req_re = re.search(r"<title>(.*?)</title>",req_text,re.S | re.I)
        if req_re: 
            req_re = req_re.group(1)                    
        for cookie in req.raw.headers.getlist("Set-Cookie"):
            c = SimpleCookie()
            c.load(cookie)
            for name,morsel in c.items():
                is_safe = False
                has_httponly = bool(morsel["httponly"])
                has_secure = bool(morsel["secure"])
                if has_httponly and has_secure:
                    is_safe = True
                cs.append({
                    "cookie_name":name,
                    "has_httponly":has_httponly,
                    "has_secure":has_secure,
                    "is_safe":is_safe
                })
        redirect_chain = [{"status": r.status_code, "url": r.url} for r in req.history]

        output = {
                "url": url,
                "final_url": final_url,
                "status_code": req_sc,
                "response_time_ms": do_time,
                "title": req_re,
                "server": req_server if req_server else '',
                "powered_by": req_xb if req_xb else '',
                "redirect_chain": redirect_chain,
                "cookie_security": cs
            }
        

        print(f'[{req_sc}] [{do_time*1000:.0f}ms] [{req_server}] {ip} - "{req_re}"')
        return output
                
    
    def prosessline(self,line):
        try:
            x = self.domain_check(line)
            y = self.request_do(x)
            return y
        except DomaincheckError as D:
            return str(D)


    def TPE(self):
        all_output = []
        if not self.file:
            raise ValueError("请实例化时指定一个文件")
        with ThreadPoolExecutor(max_workers=self.concurrency) as T:
            try:
                ips = self.file_read(self.file) 
            except FileNotFoundError as fr:
                print("未找到该文件，请检查路径后重试！")
                return 
            futures = [T.submit(self.prosessline,line) for line in ips]
            for f in as_completed(futures):
                r = f.result()
                if r is None:
                    continue
                if isinstance(r,str):
                    continue
                all_output.append(r)
        if self.output:
            self.output_to_file(all_output)


    def run(self):
        if self.url:
            res = self.prosessline(self.url)
            if self.output and res and not isinstance(res, str):
                self.output_to_file([res])  # 统一以列表格式保存
        elif self.file:
            self.TPE()
    

if __name__ == "__main__":
        parse = argparse.ArgumentParser(description="test")
        group = parse.add_mutually_exclusive_group(required=True)
        group.add_argument("-u","--url",help="目标url,自动规范化补全为 http:// 协议前缀")
        group.add_argument("-f","--file",help="接收一个文本文件路径，内容为ip或域名、url列表")
        parse.add_argument("-c","--concurrency",type=int,default=20,help="批量模式下的最大并发数（默认 20）")
        parse.add_argument("--timeout",type=float,default=5.0,help="HTTP 请求超时时间（默认 5.0 秒）")
        parse.add_argument("-a","--user-agent",default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",help="自定义 User-Agent（缺省时需内置一个高仿真的现代浏览器默认 UA，严禁使用暴露 Python 脚本特征的默认标头）。")
        parse.add_argument("--no-redirect",action="store_false",help="布尔开关。默认情况下程序应跟随重定向并记录跳转链；若携带此参数，则禁止跟随重定向（抓取 301/302 原始报文）。")
        parse.add_argument("-k","--insecure",action="store_true",help="布尔开关。遇到自签名、过期或无效的 SSL/HTTPS 证书时忽略告警强制连接，且终端不应被 urllib3 的红色告警刷屏。")
        parse.add_argument("-o","--output",help="导出报告文件名（结构化 JSON 格式）。")
        vt = parse.parse_args()
        ht = HttpScan(url=vt.url,file=vt.file,concurrency=vt.concurrency,timeout=vt.timeout,user_agent=vt.user_agent,no_redirect=vt.no_redirect,insecure=vt.insecure,output=vt.output)
        ht.run()