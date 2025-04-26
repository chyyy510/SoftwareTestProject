import os

from dotenv import load_dotenv
import qianfan
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 AK 和 SK
AK = os.getenv("QIANFAN_AK")
SK = os.getenv("QIANFAN_SK")

if not AK or not SK:
    raise ValueError("请设置环境变量 QIANFAN_AK 和 QIANFAN_SK")


def get_access_token(ak: str, sk: str) -> str:
    """获取百度千帆平台的 access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": ak,
        "client_secret": sk,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # 如果请求失败会抛异常
    data = response.json()
    if "access_token" not in data:
        raise ValueError(f"获取 access_token 失败: {data}")
    return data["access_token"]


def main():
    try:
        access_token = get_access_token(AK, SK)
        print("你的 access_token 是：", access_token)

        # 初始化 qianfan 客户端
        client = qianfan.ChatCompletion(access_token=access_token)

        # 发送对话请求
        response = client.do(
            model="ERNIE-4.0-8K", messages=[{"role": "user", "content": "你好！"}]
        )

        # 打印回复
        print("机器人回复：", response.body.get("result"))

    except Exception as e:
        print("发生错误：", e)


if __name__ == "__main__":
    main()
