import struct
import numpy as np

def binary_Data_decoder(binary_data):
    data1 = int.from_bytes(binary_data[4:5], 'little')
    data2 = int.from_bytes(binary_data[5:6], 'little')
    data3 = int.from_bytes(binary_data[6:7], 'little')

    binary_data_info = [data1, data2, data3]

    binary_data_dict = dict(zip(["data1", "data2", "data3"], binary_data_info))
    return binary_data_dict


data = struct.unpack(f"<{length}h", data[length:length])  #바이너리 자료를 형태에 맞게 변환. h는 short, i는 int, f는 float. 프로토콜에 따라 설정가능

def openbi(fname, dt):
    with open(fname, 'rb') as f:
        data=f.read()
        col,raw  = data[:9].decode().split('X')
        arr = data[9:]
        arr=np.frombuffer(arr, dtype=dt).reshape(int(col), int(raw))
    return arr
