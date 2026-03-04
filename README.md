<img width="1201" height="816" alt="image" src="https://github.com/user-attachments/assets/2115d3c6-24a6-4e18-aed3-593269f5a205" />

Bu Proje Ne Öğretiyor?
1. Client-Server Mimarisi
Tek bir merkezi sunucu vardır. Tüm istemciler yalnızca sunucuyla konuşabilir — birbirleriyle konuşamazlar. Animasyonda turuncu istemcilerin paketleri önce mavi sunucuya gittiğini, cevabın da sunucudan geri döndüğünü gözlemleyebilirsin.
•Sunucu çöktüğünde tüm ağ durur → "tek nokta arızası"
•Yönetimi kolaydır, güvenlik merkezi olarak uygulanır
•Gerçek örnekler: YouTube, Instagram, Gmail, çevrimiçi oyun sunucuları
<img width="590" height="816" alt="image" src="https://github.com/user-attachments/assets/e4c18732-8454-41ab-948b-f8cbaff88080" />


3. P2P (Peer-to-Peer) Mimarisi
Merkezi sunucu yoktur. Her düğüm (peer) hem gönderici hem alıcıdır — ağdaki diğer herkesle doğrudan konuşabilir. Animasyonda yeşil peer'ların birbirlerine doğrudan paket gönderdiğini görebilirsin.
•Bir düğüm çökse ağ çalışmaya devam eder → "dayanıklı yapı"
•Ölçeklenmesi kolaydır, yeni peer eklemek yeterlidir
•Gerçek örnekler: BitTorrent, Bitcoin/Blockchain, WebRTC görüntülü arama
<img width="605" height="810" alt="image" src="https://github.com/user-attachments/assets/14acd916-5e23-4f9b-8b75-f9829d1df86d" />

Python Programlama Kavramları
Projenin her dosyası ayrı bir Python kavramını öğretmek üzere tasarlanmıştır:
Dosya	Öğrettiği Kavram
config.py	Sabit değişkenler, kod organizasyonu
utils.py	Fonksiyonlar, trigonometri (sin/cos), modülerlik
packet.py	Sınıflar (__init__, update, destroy), lerp animasyonu
node.py	Sınıf kalıtımı temelleri, canvas çizimi, math.sin ile efekt
client_server_panel.py	Sınıflar arası iletişim, liste yönetimi, after() zamanlayıcı
p2p_panel.py	Rastgelelik (random), lambda fonksiyonları, liste filtreleme
main.py	Ana giriş noktası, __name__ == '__main__', mainloop()

Dosya Yapısı
<img width="953" height="555" alt="image" src="https://github.com/user-attachments/assets/acf1ea33-d9a4-41c3-9ddc-b6340846123a" />

Proje 7 dosyadan oluşur. Her dosya tek bir sorumluluğa sahiptir (Separation of Concerns ilkesi):
p2p_app/
├── main.py                ← Çalıştırılacak tek dosya
├── config.py              ← Tüm renkler ve sabit değerler
├── utils.py               ← Matematik yardımcı fonksiyonları
├── packet.py              ← AnimatedPacket sınıfı
├── node.py                ← NetworkNode sınıfı
├── client_server_panel.py ← Sol panel (merkezi mimari)
└── p2p_panel.py           ← Sağ panel (dağıtık mimari)

Dosyalar birbirini şu şekilde kullanır:
main.py  →  client_server_panel + p2p_panel
her iki panel  →  node + packet
node + packet  →  config + utils
Nasıl Kullanılır?
Otomatik Animasyon
Uygulama açıldığında her iki panel de kendi kendine çalışmaya başlar. Sol panelde istemciler sunucuya istek gönderir ve cevap alır. Sağ panelde peer'lar birbirleriyle doğrudan veri paylaşır.
Manuel Kontroller
•⏸ DURDUR / ▶ OYNAT — Animasyonu durdurur veya devam ettirir
•📤 C→S İstek Gönder — Sol panelde anlık bir istek/cevap döngüsü tetikler
•🔄 P2P Transfer — Sağ panelde rastgele bir P2P transferi başlatır
Renk Kodları
•Mavi  ● — Sunucu (Server)
•Turuncu ● — İstemci (Client)
•Yeşil ● — P2P Peer
•Sarı ● — Uçan veri paketi
•Mor ● — P2P bağlantı çizgileri

 Animasyon Nasıl Çalışır?
Game Loop (Oyun Döngüsü)
Animasyonun kalbi main.py içindeki _animate() fonksiyonudur. Bu fonksiyon her ~16 milisaniyede bir kendini tekrar çağırır — bu yaklaşık 60 FPS (saniyede 60 kare) demektir.
def _animate(self):
    self.cs_panel.update()   # Sol paneli güncelle
    self.p2p_panel.update()  # Sağ paneli güncelle
    self.root.after(16, self._animate)  # 16ms sonra tekrar çağır

Lerp (Linear Interpolation)
Paketlerin A'dan B'ye yumuşakça hareket etmesi için "lerp" (doğrusal ara değer) tekniği kullanılır. t değeri 0'dan 1'e çıktıkça paket hedefine yaklaşır.
def lerp(a, b, t):
    return a + (b - a) * t   # t=0 → a,  t=1 → b

Trigonometri ile Yerleşim
Düğümleri çember üzerine eşit aralıklı yerleştirmek için trigonometri kullanılır. circle_point() fonksiyonu her düğümün (x, y) koordinatını hesaplar.
x = merkez_x + yarıçap * cos(açı)
y = merkez_y + yarıçap * sin(açı)
