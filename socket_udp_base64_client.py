import socket
import sys
import base64

#Base64でエンコードする画像のパス
target_file=r"taku.png"
#エンコードした画像の保存先パス
encode_file=r"encode.txt"

with open(target_file, 'rb') as f:
    data = f.read()

#Base64で画像をエンコード
encode=base64.b64encode(data)
with open(encode_file,"wb") as f:
    f.write(encode)

M_SIZE = 4194304

# Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
serv_address = ('127.0.0.1', 8890)

# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(len(encode))
print(sys.getsizeof(encode))
try:
    # ②messageを送信する
    print('Input any messages, Type [end] to exit')
    message = encode
    if message != 'end':
        send_len = sock.sendto(message, serv_address)
        # ※sendtoメソッドはkeyword arguments(address=serv_addressのような形式)を受け付けないので注意

        # ③Serverからのmessageを受付開始
        print('Waiting response from Server')
        rx_meesage, addr = sock.recvfrom(M_SIZE)
        print(f"[Server]: {rx_meesage.decode(encoding='utf-8')}")

    else:
        print('closing socket')
        sock.close()
        print('done')


except KeyboardInterrupt:
    print('closing socket')
    sock.close()
    print('done')
