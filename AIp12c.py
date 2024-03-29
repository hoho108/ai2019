# AIp12c.py: AI practices - 12 > program c: a Chatbot example
# Jia-Sheng Heh, 10/26/2019, revised from bot1.py

#################### AIp12c.py ####################

#####===== (1) Git/GitHub 遠端同步操作 =====#####
#####===== (2) Heroku =====#####

#####===== (3) LINE Developer建立bot =====#####

###=== (3.1) 申請 LINE Developer帳號 ===###  
# LINE Developer 網站
# --> 選擇 Developer Trial方案 (好友數80,無LINE@,發訊無上限,有Reply/Push API) 
# --> Start Using Message API --> Name + Email address

###=== (3.2) 創建 bot 機器人 ===###  
# LINE Developer 登入
# —> Provider List —> Create New Provider —> Create
# —> Messaging API —-> Create new channel —-> Selected Provider:
#    + App icon + App name + App description + Category/Subcategory —-> Create

###=== (3.3) 機器人訊息 ===###  
# LINE Developer —> Provider List —-> 選擇機器人 —-> Channel settings 
#   + Channel Secret 密碼* + Channel Access Token 密碼* ===> 用於webhook程式 (5.3)
#   ＋ QR code                                         ===> 用於加入群組

#####===== (4) 結合VScode/Flask/Git/Heroku建立網頁 =====#####
###=== (4.1) 建立新應用 ===###  
# 進入官網 —-> New App —-> 取專案名稱(AIp12x) —-> Deploy
###=== (4.2) VScode建立Flask專案描述檔案 ===###  
# 建立 (1) runtime.txt: 描述使用的python環境
# 建立 (2) requirements.txt: 描述程式運作所需要的套件
#       加上 line-bot-sdk
# 建立 (3) Profile: 告訴Heroku如何執行程式
#       web gunicorn AIp12c:app
# 建立本程式碼 (4) AIp12c.py
###=== (4.3) 先在本機上測試本程式 ==> 此步無法進行，可加入 heroku 偵錯 (參見4.5)
###=== (4.4) 將程式部署到Heroku App,並測試 ===###  
# $ heroku login              // 登入 Heroku
# $ git init                  // 初始化專案
# $ heroku git:remote -a 專案名稱  // 專案名稱 = aip12x
# $ git add .                // 更新專案 
# $ git commit -m “更新的訊息”
# $ git push heroku master
# --> 部署的網址： https://aip12x.herokuapp.com/   
###=== (4.5) 在部署Heroku時，同時偵錯 ===###  
# 建議 開設兩個 Terminals, 一個部署(如 4.4), 一個偵錯(如下行指令)
# $ heroku logs --tail --app aip12x   (偵錯指令)
# 偵錯時，在程式碼中 加入 print()

#####===== (5) AIp12c.py =====##### ===> 網路簡易範例

###=== (5.1) 載入軟件包 ===###  
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *
import time

###=== (5.2) 程式宣告 ===###  
app = Flask(__name__)  # __name__ 代表目前執行的模組

###=== (5.3) LINE介面密碼 ===### (參考3.3)
##== (1) Channel Access Token
line_bot_api = LineBotApi("Su7C/KeHlykwq0AwBinAZQ/lqkBn/gmufc7+J+NuzvU3euHnYvp/9Wdvwd+Xq9e9ePqzBdzTYe6oxeOsy8gMaK43wNbJ8iIDUnpwMY1FDKkQKrRfK/jAp95kGWyAoxfC1hJulBL6Ts9lWrXXfkcs/wdB04t89/1O/w1cDnyilFU=")
##== (2) Channel Secret
handler = WebhookHandler("73e5b02eec568c95b0602453d7699e3f")
###=== (5.4) 監聽來自 /callback 的 Post Request  ===###
@app.route("/callback", methods=['POST']) 
def callback():
    print(">>>>>>>>> 1.testing")  # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(">>>>>>>>> 2.testing")  # get request body as text
    body = request.get_data(as_text=True)
    print(">>>>>>>>> 3.testing"+body)
    app.logger.info("Request body: " + body)
    print(">>>>>>>>> 4.testing-body:"+body)
    # handle webhook body
    try:
        print(">>>>>>>>> 5.testing-try:...")
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

###=== (5.5) 處理訊息  ===###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    user_id = event.source.user_id
    if event.message.id == "100001":
        return
    text = event.message.text
    happy = ["可愛","喜歡","愛","乖"]
    sad = ["討厭","拋棄","丟掉"]
    h = 0
    for i in happy:
        if text.find(i) != -1:
            if text[text.find(i)-1] != "不":
               h = 1
               break
            else:
                h = -1
                break     
    for i in sad:
        if h == 1:
            break
        if text.find(i) != -1:
            if text[text.find(i)-1] != "不":
                h = -1
                break
            else:
                h = 0
                break
    if h == 1:
        reply_text = "^__^"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
        h = 0
    elif h == -1:
        line_bot_api.push_message(user_id, StickerSendMessage(package_id=11537, sticker_id=52002746))
        for i in range(10):
            if (10-i) == 4:
                line_bot_api.push_message(user_id, TextSendMessage("..."))
            time.sleep(1)
        line_bot_api.push_message(user_id, TextSendMessage("冷卻完畢"))
        h = 0
    elif (text.find("壞") != -1):
        line_bot_api.push_message(user_id, StickerSendMessage(package_id=11537, sticker_id=52002746))
        for i in range(10):
            if (10-i) == 4:
                line_bot_api.push_message(user_id, TextSendMessage("..."))
            time.sleep(1)
        line_bot_api.push_message(user_id, TextSendMessage("冷卻完畢"))
    elif (text.find("狗狗") != -1):
        reply_text = "凹嗚～"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    elif(text.find("吃飯") != -1): 
        reply_text = "（踏踏踏踏...）"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    elif(text.find("散步") != -1):
        reply_text = "汪！"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    elif(text.find("握手") != -1):
        reply_text = "（伸出右手）"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    elif(text.find("左") != -1):
        reply_text = "（伸出左手）"

        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    elif(text.find("右") != -1):
        reply_text = "（伸出右手）"
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    else: # 如果非以上的選項，就會學你說話
        reply_text = text
        line_bot_api.push_message(user_id, TextSendMessage(reply_text))
    # message = TextSendMessage(reply_text)
    # line_bot_api.reply_message(event.reply_token, message)

###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
