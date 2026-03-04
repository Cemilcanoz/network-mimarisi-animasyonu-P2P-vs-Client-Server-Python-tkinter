# ─────────────────────────────────────────────
#  node.py  —  Ağ düğümü (bilgisayar/sunucu)
#
#  Ağdaki her bilgisayarı temsil eder.
#  Canvas üzerinde renkli daire + ikon + etiket.
# ─────────────────────────────────────────────

import math
from config import TEXT_COLOR, ACCENT_YELLOW


class NetworkNode:
    """
    Ağ topolojisindeki tek bir bilgisayar/sunucu.

    node_type değerine göre farklı ikon gösterir:
      "server"  →  ⚙  (dişli, merkezi sunucu)
      "client"  →  💻 (bilgisayar, istemci)
      "peer"    →  ◈  (eşit eş, P2P düğümü)
    """

    # Her tip için ikon sözlüğü — sınıf seviyesinde tanımlandı
    # Yani her instance için ayrı ayrı tutulmaz, tek kopya var
    ICONS = {
        "server": "⚙",
        "client": "💻",
        "peer"  : "◈"
    }

    def __init__(self, canvas, x, y, label, color,
                 node_type="client", size=22):
        """
        canvas    : Çizim alanı (tkinter Canvas)
        x, y      : Düğümün merkez koordinatı
        label     : Gösterilecek isim ("SERVER", "C1", "P3" gibi)
        color     : Dolgu rengi (config.py'den gelir)
        node_type : "server" | "client" | "peer"
        size      : Dairenin yarıçapı (piksel)
        """
        self.canvas    = canvas
        self.x         = x
        self.y         = y
        self.label     = label
        self.color     = color
        self.node_type = node_type
        self.size      = size

        # Titreşim (pulse) animasyonu için faz sayacı
        # Her update() çağrısında artarak sin() dalgası oluşturur
        self.pulse = 0.0

        # Aktiflik durumu: paket alıp verirken True
        self.active       = False
        self.active_timer = 0   # Kaç kare daha aktif kalacak

        # Düğümü canvas'a çiz
        self._draw()

    def _draw(self):
        """
        Düğümü 3 katmanlı olarak çizer:
        1) Dış parlama halkası (glow)
        2) Ana daire (gövde)
        3) İkon + etiket metni
        """
        s = self.size

        # ── 1) Glow halkası ───────────────────────────────────
        # fill="" → dolu değil, sadece çerçeve
        # stipple  → noktalı desen = yarı saydam efekti
        self.glow = self.canvas.create_oval(
            self.x - s - 8, self.y - s - 8,
            self.x + s + 8, self.y + s + 8,
            fill="",
            outline=self.color,
            width=1,
            stipple="gray25"
        )

        # ── 2) Ana daire ──────────────────────────────────────
        self.circle = self.canvas.create_oval(
            self.x - s, self.y - s,
            self.x + s, self.y + s,
            fill=self.color,
            outline="white",
            width=2
        )

        # ── 3) İkon ───────────────────────────────────────────
        # dict.get(key, default) → key yoksa default döner
        icon = self.ICONS.get(self.node_type, "●")

        self.icon_text = self.canvas.create_text(
            self.x, self.y - 3,
            text=icon,
            font=("Segoe UI Emoji", 13),
            fill="white"
        )

        # ── 4) Etiket (altında) ───────────────────────────────
        self.label_text = self.canvas.create_text(
            self.x, self.y + s + 12,
            text=self.label,
            font=("Courier", 9, "bold"),
            fill=TEXT_COLOR
        )

    def set_active(self, duration=15):
        """
        Düğümü aktif yap (veri alışverişi yapıyor görünsün).
        duration: kaç animasyon karesi boyunca aktif kalacak
        """
        self.active       = True
        self.active_timer = duration

    def update(self):
        """
        Her karede çağrılır. Glow efektini günceller.

        Aktifken: Sarı, titreşen halkası
        Pasifken: Normal renk, sabit halka
        """
        self.pulse += 0.1   # Faz ilerlet

        if self.active:
            self.active_timer -= 1
            if self.active_timer <= 0:
                self.active = False

            # math.sin() → -1 ile +1 arasında salınan değer
            # Bunu halkaya eklersek büyüyüp küçülen efekt olur
            scale = 1 + 0.3 * math.sin(self.pulse * 3)
            s = self.size * scale + 8

            self.canvas.coords(
                self.glow,
                self.x - s, self.y - s,
                self.x + s, self.y + s
            )
            # itemconfig → mevcut şeklin özelliğini değiştir
            self.canvas.itemconfig(
                self.glow,
                outline=ACCENT_YELLOW,
                width=2
            )

        else:
            # Pasif halde sabit glow
            s = self.size + 8
            self.canvas.coords(
                self.glow,
                self.x - s, self.y - s,
                self.x + s, self.y + s
            )
            self.canvas.itemconfig(
                self.glow,
                outline=self.color,
                width=1
            )