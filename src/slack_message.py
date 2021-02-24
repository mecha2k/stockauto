import os

from slacker import Slacker
from dotenv import load_dotenv

load_dotenv(verbose=True)
bot_user_token = os.getenv("BOT_USER_TOKEN")

slack = Slacker(bot_user_token)

markdown_text = """
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
"""

attach_dict = {
    "color": "#ff0000",
    "author_name": "MECHA2K",
    "title": "오늘의 증목 현황",
    "text": """
    test
    2,326.13 △11.89 (+0.51%)
    2,326.13 △11.89 (+0.51%)
    """,
    "image_url": "ssl.pstatic.net/imgstock/chart3/day/KOSPI.png",
}

attach_list = [attach_dict]
slack.chat.post_message(channel="#stock", attachments=[attach_dict])
# slack.chat.post_message(channel="#stock", text=markdown_text)

# strbuf = (
#     "*내 계좌 현황*"
#     f"계좌명: {str(cpBalance.GetHeaderValue(0))}"
#     f"결제잔고수량: {str(cpBalance.GetHeaderValue(1))}"
#     f"평가금액: {str(cpBalance.GetHeaderValue(3))}"
#     f"평가손익: {str(cpBalance.GetHeaderValue(4))}"
#     f"종목수: {str(cpBalance.GetHeaderValue(7))}"
# )
# dbgout(strbuf)
