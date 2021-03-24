import socket
import sys
import datetime as dt
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sokette, AF_INET iPV4 kullanıldığını temsil eder.
# Sokette, SOCK_STREAM TCP protokölü kullandığını temsil eder.

# Server adresini ile ilgili adrese bağlanır.
server_addr = ('127.0.0.1', 10002)
print('Sunucu adresi {} port {}'.format(*server_addr))

# Oluşturulan soket ile ilgili port ile bağlantı kurulur.
sock.connect(server_addr)

try:
    while True:
        print("""
        1. Çıkış için 'exit' yazınız.
        2. Veri girişi için 'giris' yazınız.
        """)
        secim =input("Seçiniz : ")
        if secim == 'exit':
            sys.exit()
        elif secim == 'giris':
            print("""
            Server'a hangi islemi yaptırmak istersiniz.
            1. Toplama yaptırmak için 'T'
            2. Faktoriyel hesaplatmak için 'F'
            """)
            flag = input("Seciminizi yapin : ")
            if flag == 'T' or flag == 'F':
                veri = input("Hesaplatmak istediginiz degeri giriniz : ")

                # Elde edilen girdileri tek sokette göndermek için,
                # Json object formatında oluşturulan liste girdisi sunucuya aktarırılır.
                client_data = json.dumps({"flag":flag, "data": veri})

                # Veri yollanılırken zamanı hesaplanılıyor.
                send_time = dt.datetime.now()

                # Json object aktarımını encode edip iletiyor sunucuda decode ediyoruz.
                sock.send(client_data.encode())
                try:
                    # Sucudan gelen cevap ve gönderilen veri arasındaki zaman farkının yazılacağı dosyayı açıyoruz.
                    save_time = open("response_time.txt", "a+")
                except save_time.error:
                    # Dosyanın açılması sırasında hata oluşursa programın çökmesini engellemek için oluşturuldu.
                     print("İstemci cevap süresinin kaydedileceği dosyada hata oluştu.")

                # TCP/IPV4 soketini dinleyip gelen datayı kabul ettiriyoruz.
                result = sock.recv(1024)

                # İleti geldiğinde, geliş zamanı ölçülür.
                get_time = dt.datetime.now()
                print(str(result.decode()))

                # İki süre aralığının farkı ile response değeri hesaplanılır.
                time_result = get_time - send_time
                save_time.write('Cevap verilme süresi : {0} \n'.format(str(time_result)))

            else:
                print("Hatalı giriş yaptığınız, lütfen tekrar deneyin.")
                break
        else:
            break

finally:
    print('İşlem tamamlandı, yine bekleriz.')

