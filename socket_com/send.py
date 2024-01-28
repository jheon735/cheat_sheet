import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #소켓 설정. INET 방식, stream 형태
try:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port)) #port입력
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    time.sleep(3000)

    count = 0

    try:
        send_data = 0
        while send_data < total:    #total은 보내야하는 전체 데이터
            st = time.time()
            current_data = int.from_bytes(data, 'little')  #변환할 데이터
            client_socket.send(current_data)
            send_data += len(current_data)

    except Exception as msg:
        print(msg)

except (KeyboardInterrupt):
    server_socket.close()
