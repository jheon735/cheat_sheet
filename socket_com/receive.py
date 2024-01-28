import socket
import time

def recvSocket(host, port, IQ_queue):
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(timeout) #timeout 시간 설정
            server_socket.connect((host, port)) #ip와 port

            binary_data_count = 0

            while True:
                data_recv = 0

                if binary_data_count == 0:
                    print("binary_data receive")

                try:
                    binary_data = server_socket.recv(length)  #읽을 데이터 길이
                    data_recv += len(binary_data)

                    if len(binary_data) == 0:    #헤더가 없을 때
                        time.sleep(1)
                        binary_data_count += 1
                        continue

                    else:
                        print("binary_data receive")
                        st = time.time()
                        print("Check Preamble")

                        if hex(int.from_bytes(binary_data[0:4],'little')) != preamble: #헤더에서 오류가 있는지 체크할 프림블
                            print("[recv] Wrong Preamble!")

                            # 자료를 사용하지 않을 범위까지 크게 잡아서 exception 발생시킴
                            read_data = 2**33
                            print(f"!!!!data revised as {read_data}!!!!")

                        else:
                            IQ_queue.put(binary_data)

                        print('binary_data End')
                        print('Data Start')
                        binary_data_count = 0

                        total_size = 30 #전체 자료 사이즈

                        while data_recv < total_size:
                            try:
                                recv = server_socket.recv(buffer)  #버퍼 사이즈
                                data_recv += len(recv)

                            except socket.timeout as msg:
                                print(f'Socket Timeout Exception While Receiving Data ! ! ! : {msg}')
                                print(f'recv {data_recv} bytes')
                                data_recv += len(recv)
                                break

                        print(f'Total {data_recv} bytes received')

                        et = time.time()

                except socket.timeout as msg:
                    if binary_data_count == 0:
                        print(f'Socket Timeout Exception... waiting next beam binary_data : {msg}')
                        binary_data_count += 1
                    else:
                        binary_data_count += 1

        except (socket.timeout, ConnectionRefusedError) as msg:
            print("----- Ethernet Connection : Fail   -----")
            print(f'{msg}')
            if server_socket:
                server_socket.close()
            continue

        except (KeyboardInterrupt) as msg:
            print("----- Keyboard Interrupted         -----")
            print(msg)
            if server_socket:
                server_socket.close()
            break