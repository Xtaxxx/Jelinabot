# main.py
from support_assistant import SupportAssistant
from config import Config

if __name__ == "__main__":
    assistant = SupportAssistant()

    # 查询获得答案
    response = assistant.query("Jelina是什么，给我讲解他能干什么")
    print(response)