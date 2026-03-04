# ─────────────────────────────────────────────
#  packet.py  —  Hareketli veri paketi
#
#  Ağ üzerinde uçan bir veri paketini temsil eder.
#  Canvas üzerinde hareket eden küçük bir daire.
# ─────────────────────────────────────────────

import random
from utils  import lerp
from config import ACCENT_YELLOW


class AnimatedPacket:
    """
    A noktasından B noktasına hareket eden animasyonlu paket.

    Nasıl çalışır?
    - t değişkeni 0.0'dan 1.0'a yükselir
    - Her update() çağrısında t biraz artar
    - lerp(x1, x2, t) ile anlık konum hesaplanır
    - t >= 1.0 olunca done=True → paket silinir
    """

    def __init__(self, canvas, x1, y1, x2, y2,
                 color=ACCENT_YELLOW, size=6, label=""):
        """
        canvas     : tkinter Canvas — üzerine çizeceğimiz alan
        x1,y1      : Başlangıç noktası (gönderen düğümün koordinatı)
        x2,y2      : Hedef nokta (alıcı düğümün koordinatı)
        color      : Paketin rengi
        size       : Dairenin yarıçapı (piksel)
        label      : Üzerinde görünecek kısa metin ("REQ", "P2P" gibi)
        """
        self.canvas = canvas
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.color  = color
        self.size   = size
        self.label  = label

        # t: ilerleme oranı. 0.0 = başlangıç, 1.0 = hedefe ulaştı
        self.t     = 0.0

        # Hız: her karede t kadar artar. Küçük = yavaş, büyük = hızlı
        # random.uniform(a, b) → a ile b arasında rastgele ondalıklı sayı
        self.speed = random.uniform(0.018, 0.032)

        # Animasyon bitti mi?
        self.done  = False

        # ── Canvas'a daire çiz ──────────────────────────────
        # create_oval(sol, üst, sağ, alt) → daire/elips çizer
        # Merkez x1,y1 olsun diye: sol=x1-size, sağ=x1+size
        self.shape = canvas.create_oval(
            x1 - size, y1 - size,
            x1 + size, y1 + size,
            fill=color,
            outline="white",
            width=1
        )

        # Paketin üstünde küçük etiket
        self.text_id = canvas.create_text(
            x1, y1 - size - 5,
            text=label,
            fill=color,
            font=("Courier", 7, "bold")
        )

    def update(self):
        """
        Her animasyon karesinde çağrılır.
        Paketi biraz ilerletir, yeni konuma taşır.
        """
        if self.done:
            return   # Zaten bittiyse hiçbir şey yapma

        # t'yi artır
        self.t += self.speed

        # t 1.0'ı geçmesin, geçince bitir
        if self.t >= 1.0:
            self.t   = 1.0
            self.done = True

        # Anlık konum = lerp ile başlangıç ve hedef arası
        cx = lerp(self.x1, self.x2, self.t)
        cy = lerp(self.y1, self.y2, self.t)

        # canvas.coords() → mevcut şeklin koordinatlarını günceller
        # (şekli silip yeniden çizmekten çok daha verimli)
        self.canvas.coords(
            self.shape,
            cx - self.size, cy - self.size,
            cx + self.size, cy + self.size
        )

        # Etiketi de aynı şekilde taşı
        self.canvas.coords(self.text_id, cx, cy - self.size - 5)

    def destroy(self):
        """
        Paketi canvas'tan tamamen kaldırır.
        Animasyon bitince çağrılır — bellek temizliği.
        """
        try:
            self.canvas.delete(self.shape)
            self.canvas.delete(self.text_id)
        except Exception:
            pass   # Zaten silinmişse sessizce geç