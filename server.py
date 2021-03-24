import socket
import json
import sys
import math
import datetime as dt

# -*- coding: utf-8 -*-

# Sokette, AF_INET iPV4 kullanıldığını temsil eder.
# Sokette, SOCK_STREAM TCP protokölü kullandığını temsil eder.

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except sock.error:
    print("Sokete bağlanılırken hata oluştu.")
    sys.exit()  # Olası bir hata durumunda serveri kapattırıyoruz.

server_address = ('127.0.0.1', 10002)
print('Sunucu baslatildi {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(5)  # Soketi bağlantılar arasında dinlemeye alır, 6 mesajı dinlemeye alabilir.


# Gelen veriyi ayrıştırarak ilgili method a yönlendirme yapar.
def _parser (client_data):
    client_data = json.loads(client_data)

    # Suncunun işlem yapabilmesi için json objesinden gerekli flag'ı seçer.
    proc_flag = client_data["flag"]

    # Json objesinden işlenecek veriyi ayırıyor.
    proc_data = client_data["data"]

    if proc_flag == 'T':
        result = (func_sum(proc_data))
        return result
    elif proc_flag == 'F':
        result = func_factorial(proc_data)
        return result
    else:
        print("Hatalı değer girişi yaptınız, tekrar deneyin.")

# Toplama fonksiyonunda ödev pdf'in de belirtildiği üzere tek rakam kalana kadar toplama devam ettirildi.
def func_sum(numbers):
    numbers_list = list(str(numbers))
    result = 0
    total = 0

    for num in numbers_list:
        result = result + int(num)

    print(result)
    result_list = list(str(result))
    for res in result_list:
        total = total + int(res)

    print(total)
    return total

#Faktoriyel standart olduğundan math, kütüphanesinden çektim.
def func_factorial(number):
    result = math.factorial(int(number))
    return result

#İstemci adresi ve bağlanma sürelerini client_list de grafik de kullanmak için depoluyoruz.
def print_to_client_info(client_adress,connect_time):
    try:
        save_client = open("client_list.txt", "a+")
    except save_client.error:
        print("İstemci girdisi kaydedilemedi.")

    save_string = ('İstemci bağlantı adresi: {0} --- Bağlantı saati: {1} \n'.format(client_adress,connect_time))
    save_client.write(save_string)


while True:

    print('Bağlantı kuruluyor...')

    # Soket bağlantısı kuruluyor.
    connection, client_address = sock.accept()

    # istemcinin bağlanma tarihi ve zamanını kaydeder.
    connect_time = dt.datetime.now()
    print_to_client_info(client_address,connect_time)

    try:
        print('Baglanti basarili. İstemci adresi:', client_address)
        while True:

            # Encode edilen verileri soket aracılığı ile çekiyoruz.
            data = connection.recv(1024)

            # Çekilen veri Decode edip tekrar json objesine dönüştürülüyor.
            data = json.loads(data.decode())
            json_object_to_data = json.dumps(data)

            # Client e elde edilen değer iletilir.
            result = "İşlem sonucunuz : " + str(_parser(json_object_to_data))

            connection.sendall(str(result).encode())

            if data:
                print('Veri aktarımı başarılı. ')
            else:
                print('Veri aktarımında hata alındı. İstemci adresi: ', client_address)
                break

    finally:
        print("Veri girişi yapılması bekleniyor.")
        connection.close()