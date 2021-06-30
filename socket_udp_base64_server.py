import socket
import time
import cv2
import base64
import numpy as np
import io


M_SIZE = 4194304

# 
host = '127.0.0.1'
port = 8890

locaddr = (host, port)

#デコードされた画像の保存先パス
image_file=r"decode.jpg"

# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
print('create socket')

# ②自ホストで使用するIPアドレスとポート番号を指定
sock.bind(locaddr)

while True:
    try :
        # ③Clientからのmessageの受付開始
        print('Waiting message')
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f'Received message is [{message}]')

        # Clientが受信待ちになるまで待つため
        time.sleep(1)

        # ④Clientへ受信完了messageを送信
        print('Send response to Client')
        sock.sendto('Success to receive message'.encode(encoding='utf-8'), cli_addr)


        #バイナリデータ <- base64でエンコードされたデータ  
        img_binary = base64.b64decode(message)
        jpg=np.frombuffer(img_binary,dtype=np.uint8)

        #raw image <- jpg
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        #画像を保存する場合
        cv2.imwrite(image_file,img)

        #表示確認
        cv2.imshow('window title', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break