# ─────────────────────────────────────────────
#  client_server_panel.py
#
#  CLIENT-SERVER mimarisini gösteren sol panel.
#
#  Mimari nasıl çalışır:
#    • 1 merkezi SUNUCU vardır
#    • N tane İSTEMCİ (client) sunucuya bağlanır
#    • İstemciler birbirleriyle KONUŞAMAZ
#    • İletişim: Client → Server → Client
#    • Sunucu çökerse HİÇBİR ŞEY çalışmaz
#
#  Gerçek örnekler: YouTube, Instagram, Gmail
# ─────────────────────────────────────────────

import random
import math
import tkinter as tk

from config import (
    PANEL_COLOR, BORDER_COLOR, DIM_COLOR,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE,
    ACCENT_RED, LINE_COLOR, TEXT_COLOR
)
from utils  import circle_point
from node   import NetworkNode
from packet import AnimatedPacket


class ClientServerPanel:
    """
    Sol panel: merkezi Client-Server mimarisini animasyonlu gösterir.

    Düğüm yerleşimi:
        Sunucu → Ortada, büyük, mavi
        İstemciler → Etrafında çember üzerinde, turuncu
    """

    def __init__(self, parent_frame, width, height):
        """
        parent_frame : Bu panelin konacağı tkinter Frame
        width        : Panel genişliği (piksel)
        height       : Panel yüksekliği (piksel)
        """
        self.w = width
        self.h = height

        self.packets     = []   # Aktif paket animasyonları
        self.nodes       = []   # Tüm düğümler
        self.frame_count = 0    # Kare sayacı (zamanlama için)

        # ── Canvas oluştur ────────────────────────────────────
        # Canvas = tkinter'ın çizim tahtası
        # highlightthickness + highlightbackground = kenarlık efekti
        self.canvas = tk.Canvas(
            parent_frame,
            width=width,
            height=height,
            bg=PANEL_COLOR,
            highlightthickness=2,
            highlightbackground=BORDER_COLOR
        )
        # pack() → frame içinde otomatik yerleşim
        self.canvas.pack()

        self._setup_nodes()
        self._draw_static()

    # ──────────────────────────────────────────────────────────
    # KURULUM
    # ──────────────────────────────────────────────────────────

    def _setup_nodes(self):
        """
        1 sunucu (ortada) + 6 istemci (etrafında) oluşturur.
        """
        cx = self.w // 2        # Yatay merkez
        cy = self.h // 2 + 15   # Dikey merkez (biraz aşağı kaydır)

        # ── Sunucu ────────────────────────────────────────────
        server = NetworkNode(
            self.canvas, cx, cy,
            label="SERVER",
            color=ACCENT_BLUE,
            node_type="server",
            size=28             # Sunucu diğerlerinden büyük olsun
        )
        self.nodes.append(server)
        self.server_node = server  # Sunucuya hızlı erişim için

        # ── İstemciler ────────────────────────────────────────
        count  = 6
        radius = 130   # Sunucudan kaç piksel uzakta

        for i in range(count):
            # 360° / 6 = 60° — her istemci 60 derece arayla
            # -90 ile başlayınca ilk istemci tam üstte olur
            angle = (360 / count) * i - 90

            nx, ny = circle_point(cx, cy, radius, angle)

            client = NetworkNode(
                self.canvas, nx, ny,
                label=f"C{i + 1}",
                color=ACCENT_ORANGE,
                node_type="client",
                size=18
            )
            self.nodes.append(client)

    def _draw_static(self):
        """
        Sabit (animasyonsuz) arka plan öğeleri:
        - Başlık
        - Bağlantı çizgileri
        - Bilgi kutusu
        """
        # ── Başlık ────────────────────────────────────────────
        self.canvas.create_text(
            self.w // 2, 18,
            text="CLIENT  →  SERVER",
            font=("Courier", 13, "bold"),
            fill=ACCENT_BLUE
        )
        self.canvas.create_text(
            self.w // 2, 35,
            text="Merkezi Mimari",
            font=("Courier", 8),
            fill=DIM_COLOR
        )

        # ── Bağlantı çizgileri ────────────────────────────────
        # nodes[0] = sunucu, nodes[1:] = tüm istemciler
        sx, sy = self.nodes[0].x, self.nodes[0].y

        for client in self.nodes[1:]:
            # create_line(x1,y1, x2,y2, ...)
            # dash=(dolu, boşluk) → kesik çizgi stili
            self.canvas.create_line(
                sx, sy,
                client.x, client.y,
                fill=LINE_COLOR,
                width=1,
                dash=(4, 4)
            )

        # ── Alt bilgi kutusu ──────────────────────────────────
        iy = self.h - 88
        self.canvas.create_rectangle(
            8, iy,
            self.w - 8, self.h - 8,
            fill="#0d1b2a",
            outline=BORDER_COLOR
        )

        items = [
            ("✓  Merkezi kontrol kolaylığı",  ACCENT_GREEN),
            ("✓  Kolay güvenlik yönetimi",    ACCENT_GREEN),
            ("✗  Tek nokta arızası riski",    ACCENT_RED),
            ("✗  Sunucu = Darboğaz noktası",  ACCENT_RED),
        ]

        for idx, (metin, renk) in enumerate(items):
            self.canvas.create_text(
                18, iy + 11 + idx * 17,
                text=metin,
                font=("Courier", 8),
                fill=renk,
                anchor="w"
            )

        # ── Dinamik durum metni ───────────────────────────────
        # Bu text_id'yi sonradan itemconfig() ile güncelleyeceğiz
        self.status_id = self.canvas.create_text(
            self.w // 2, iy - 12,
            text="● Hazır",
            font=("Courier", 9, "bold"),
            fill=DIM_COLOR
        )

    # ──────────────────────────────────────────────────────────
    # SİMÜLASYON
    # ──────────────────────────────────────────────────────────

    def send_packet(self, from_node, to_node, color, label):
        """
        İki düğüm arasında paket animasyonu başlatır.
        Paketi self.packets listesine ekler.
        """
        pkt = AnimatedPacket(
            self.canvas,
            from_node.x, from_node.y,
            to_node.x,   to_node.y,
            color=color,
            label=label
        )
        self.packets.append(pkt)

        # İki düğümü de aktif yap (sarı titreşim)
        from_node.set_active(20)
        to_node.set_active(20)

    def simulate_request(self):
        """
        Rastgele bir istemciden sunucuya istek, sunucudan cevap simüle eder.

        Adımlar:
          1) Rastgele bir istemci seç
          2) İstemci → Sunucu  (REQUEST)
          3) 500ms sonra Sunucu → İstemci  (RESPONSE)

        Bu tam olarak HTTP, oyun sunucusu, vb.'nin çalışma şeklidir.
        """
        # Rastgele istemci (nodes[0] sunucu, atla)
        client = random.choice(self.nodes[1:])
        server = self.server_node

        # Adım 1: İstek gönder
        self.send_packet(client, server, color=ACCENT_ORANGE, label="REQ")

        # Adım 2: 500ms sonra cevap gönder
        # lambda: anonim fonksiyon — after() bir fonksiyon bekler
        self.canvas.after(
            500,
            lambda: self.send_packet(server, client, color=ACCENT_BLUE, label="RES")
        )

        # Durum metnini güncelle
        self.canvas.itemconfig(
            self.status_id,
            text=f"● {client.label} → SERVER → {client.label}",
            fill=ACCENT_ORANGE
        )

    # ──────────────────────────────────────────────────────────
    # ANİMASYON DÖNGÜSÜ
    # ──────────────────────────────────────────────────────────

    def update(self):
        """
        Her animasyon karesinde (≈16ms) çağrılır.

        1. Paketleri ilerlet, bitenleri temizle
        2. Düğümleri güncelle (glow efekti)
        3. Belirli aralıklarla otomatik simülasyon yap
        """
        self.frame_count += 1

        # ── Paket güncelleme ──────────────────────────────────
        # Yeni liste: sadece henüz bitmemiş paketler
        alive = []
        for pkt in self.packets:
            pkt.update()
            if pkt.done:
                pkt.destroy()      # Canvas'tan sil
            else:
                alive.append(pkt)  # Devam ediyorsa sakla
        self.packets = alive

        # ── Düğüm güncelleme ──────────────────────────────────
        for node in self.nodes:
            node.update()

        # ── Otomatik simülasyon ───────────────────────────────
        # Her 90 karede bir (≈1.5 saniyede bir) istek at
        if self.frame_count % 90 == 0:
            self.simulate_request()