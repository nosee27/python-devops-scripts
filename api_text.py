#!/usr/bin/env python3
import requests
def main():
    url1= "https://httpbin.org/ip"
    try:
        response=requests.get(url1,timeout=5)
        response.raise_for_status()
        data=response.json()
        print(f"{data.get('origin','default')}")
    except Exception as e:
        print(f"错误原因为{e}")
    url2="https://api.github.com/repos/python/cpython"
    try:
        response=requests.get(url2,timeout=5)
        response.raise_for_status()
        data=response.json()
        stars=data.get('stargazers_count','default')
        print(f"stars are {stars}")
    except Exception as e:
        print(f"错误原因为{e}")
if __name__=="__main__":
    main()
