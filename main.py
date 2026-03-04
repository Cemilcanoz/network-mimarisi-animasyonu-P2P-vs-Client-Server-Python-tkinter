# ─────────────────────────────────────────────
#  main.py  —  Uygulamanın giriş noktası
#
#  Sadece bu dosyayı çalıştırmak yeterli:
#      python main.py
#
#  Bu dosya:
#    - Ana pencereyi açar
#    - İki paneli yan yana koyar
#    - Butonları ekler
#    - Animasyon döngüsünü başlatır
# ─────────────────────────────────────────────

import tkinter as tk

from config              import (
    BG_COLOR, BORDER_COLOR, DIM_COLOR,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE,
    ACCENT_YELLOW, ACCENT_PURPLE, ACCENT_RED,
    TEXT_COLOR, FRAME_MS
)
from client_server_panel import ClientServerPanel
from p2p_panel           import P2PPanel


class App:
    """
    Ana uygulama sınıfı.

    Görevleri:
      1) Pencereyi oluştur ve boyutlandır
      2) Başlık, paneller, butonlar, legend ekle
      3) Animasyon döngüsünü çalıştır
    """

    def __init__(self):
        # ── Ana pencere ───────────────────────────────────────
        # tk.Tk() → uygulamanın tek ana penceresi
        self.root = tk.Tk()
        self.root.title("P2P  vs  Client-Server  —  Ağ Mimarisi")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Pencere boyutu
        W, H = 960, 620

        # Ekranın ortasına yerleştir
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

        # ── Arayüzü kur ───────────────────────────────────────
        self._build_header()
        self._build_panels()
        self._build_controls()
        self._build_legend()

        # Animasyon durumu
        self.running = True

        # Animasyon döngüsünü başlat
        self._animate()

    # ──────────────────────────────────────────────────────────
    # ARAYÜZ KURULUMU
    # ──────────────────────────────────────────────────────────

    def _build_header(self):
        """
        Üst başlık çubuğu.
        tk.Label → metin göstermek için temel widget
        pack() → widget'ı otomatik yerleştir
        """
        hdr = tk.Frame(self.root, bg=BG_COLOR)
        hdr.pack(fill="x", padx=10, pady=(8, 0))

        tk.Label(
            hdr,
            text="⬡  AĞ MİMARİSİ ANİMASYONU",
            font=("Courier", 15, "bold"),
            fg=TEXT_COLOR, bg=BG_COLOR
        ).pack(side="left")

        tk.Label(
            hdr,
            text="Python  +  tkinter",
            font=("Courier", 9),
            fg=DIM_COLOR, bg=BG_COLOR
        ).pack(side="right")

        # Yatay ayraç çizgisi (yüksekliği 1px Frame)
        tk.Frame(self.root, bg=BORDER_COLOR, height=1).pack(
            fill="x", padx=10, pady=(4, 0)
        )

    def _build_panels(self):
        """
        İki animasyon panelini yan yana yerleştirir.

        Layout:
          [  ClientServerPanel  ] | [  P2PPanel  ]
        """
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=6)

        PANEL_W = 455
        PANEL_H = 490

        # Sol frame → ClientServerPanel
        left = tk.Frame(container, bg=BG_COLOR)
        left.pack(side="left")

        # Orta ayraç
        tk.Frame(container, bg=BORDER_COLOR, width=2).pack(
            side="left", fill="y", padx=4
        )

        # Sağ frame → P2PPanel
        right = tk.Frame(container, bg=BG_COLOR)
        right.pack(side="left")

        # Panel nesnelerini oluştur
        # Artık her panel kendi canvas'ını kendi içinde yaratıyor
        self.cs_panel  = ClientServerPanel(left,  PANEL_W, PANEL_H)
        self.p2p_panel = P2PPanel(right, PANEL_W, PANEL_H)

    def _build_controls(self):
        """
        Alt kontrol butonları.

        tk.Button → tıklanabilir düğme
        command=   → tıklanınca çağrılacak fonksiyon
        """
        bar = tk.Frame(self.root, bg=BG_COLOR)
        bar.pack(fill="x", padx=10, pady=(2, 4))

        # Ortak buton stili sözlüğü
        # **stil → fonksiyon çağrısında aç (keyword argüman olarak geç)
        stil = dict(
            font=("Courier", 9, "bold"),
            relief="flat",
            padx=14, pady=5,
            cursor="hand2",
            bd=0
        )

        # Oynat / Durdur
        self.play_btn = tk.Button(
            bar,
            text="⏸  DURDUR",
            bg=ACCENT_BLUE, fg="white",
            activebackground="#1d4ed8",
            command=self._toggle_play,
            **stil
        )
        self.play_btn.pack(side="left", padx=(0, 6))

        # Client-Server manuel tetikleme
        tk.Button(
            bar,
            text="📤  C→S İstek Gönder",
            bg="#1e3a5f", fg=ACCENT_ORANGE,
            activebackground="#1e40af",
            command=self.cs_panel.simulate_request,
            **stil
        ).pack(side="left", padx=4)

        # P2P manuel tetikleme
        tk.Button(
            bar,
            text="🔄  P2P Transfer",
            bg="#14532d", fg=ACCENT_GREEN,
            activebackground="#166534",
            command=self.p2p_panel.simulate_p2p_transfer,
            **stil
        ).pack(side="left", padx=4)

        tk.Label(
            bar,
            text="← Butonlarla manuel test edebilirsin",
            font=("Courier", 8),
            fg=DIM_COLOR, bg=BG_COLOR
        ).pack(side="left", padx=12)

    def _build_legend(self):
        """
        Renk açıklama şeridi (ne renk ne anlama geliyor).
        """
        leg = tk.Frame(self.root, bg=BG_COLOR)
        leg.pack(fill="x", padx=10, pady=(0, 6))

        items = [
            (ACCENT_BLUE,   "● Server"),
            (ACCENT_ORANGE, "● Client"),
            (ACCENT_GREEN,  "● Peer"),
            (ACCENT_YELLOW, "● Veri Paketi"),
            (ACCENT_PURPLE, "● P2P Bağlantı"),
            (ACCENT_RED,    "● Zayıf Nokta"),
        ]

        for color, label in items:
            tk.Label(
                leg,
                text=label,
                font=("Courier", 8),
                fg=color, bg=BG_COLOR
            ).pack(side="left", padx=8)

    # ──────────────────────────────────────────────────────────
    # ANİMASYON DÖNGÜSÜ
    # ──────────────────────────────────────────────────────────

    def _toggle_play(self):
        """
        Animasyonu durdur / devam ettir.
        not operatörü: True→False, False→True
        """
        self.running = not self.running

        if self.running:
            self.play_btn.config(text="⏸  DURDUR", bg=ACCENT_BLUE)
            self._animate()   # Döngüyü yeniden başlat
        else:
            self.play_btn.config(text="▶  OYNAT", bg=ACCENT_GREEN)
            # Döngü self.running=False görünce kendisi durur

    def _animate(self):
        """
        Ana animasyon döngüsü.

        ┌─────────────────────────────────────────┐
        │  _animate() çağrılır                    │
        │  → her iki paneli update et             │
        │  → 16ms sonra _animate()'i tekrar çağır │
        │  → pencere kapanana kadar böyle devam   │
        └─────────────────────────────────────────┘

        Bu "game loop" / "render loop" pattern'idir.
        FRAME_MS = 16ms ≈ 60 FPS
        """
        if not self.running:
            return   # Duraklatıldıysa çık

        self.cs_panel.update()
        self.p2p_panel.update()

        # after(ms, fonksiyon) → ms sonra fonksiyonu çağır
        # Özyinelemeli çağrı: döngü böyle oluşur
        self.root.after(FRAME_MS, self._animate)

    def run(self):
        """
        Uygulamayı başlatır.
        mainloop() → pencere kapanana kadar olay dinler
        (tıklama, klavye, pencere boyutlandırma vs.)
        """
        self.root.mainloop()


# ─────────────────────────────────────────────
# PROGRAM GİRİŞ NOKTASI
#
# Bu dosya doğrudan çalıştırıldığında:
#   python main.py
# __name__ == "__main__" olur ve uygulama başlar.
#
# Eğer başka bir dosya bu dosyayı import ederse
# __name__ == "main" olur ve bu blok ÇALIŞMAZ.
# Bu sayede import edilince otomatik açılmaz.
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.run()