import requests,shutil,uuid
import threading


def down_img():
    for i in range(100):
        url = "https://weibo.com/signup/v5/pincode/pincode.php?lang=zh&sinaId=3a7cc9f0714cf8bacea0b44e67b7ea99"
        resp = requests.get(url, verify=False, stream=True)
        if resp.status_code == 200:
            with open("imgs\weibo\{}.png".format(uuid.uuid4().hex), 'wb') as f:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, f)

def down_img_multi_thread():
    for i in range(20):
        t = threading.Thread(target=down_img)
        t.start()

