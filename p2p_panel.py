# ─────────────────────────────────────────────
#  p2p_panel.py
#
#  P2P (Peer-to-Peer) mimarisini gösteren sağ panel.
#
#  Mimari nasıl çalışır:
#    • Merkezi sunucu YOKTUR
#    • Her düğüm hem gönderici hem alıcıdır
#    • Düğümler birbirleriyle DOĞRUDAN iletişir
#    • Bir düğüm çökse ağ çalışmaya devam eder
#    • Dağıtık → dayanıklı ama yönetimi zor
#
#  Gerçek örnekler: BitTorrent, Bitcoin, WebRTC
# ─────────────────────────────────────────────

import random
import math
import tkinter as tk

from config import (
    PANEL_COLOR, BORDER_COLOR, DIM_COLOR,
    ACCENT_GREEN, ACCENT_RED, ACCENT_PURPLE,
    ACCENT_YELLOW, TEXT_COLOR
)
from utils  import circle_point, distance
from node   import NetworkNode
from packet import AnimatedPacket


class P2PPanel:
    """
    Sağ panel: dağıtık P2P mimarisini animasyonlu gösterir.

    Düğüm yerleşimi:
        7 peer → Çember üzerinde eşit aralıklı
        Hiyerarşi yok → Hepsi aynı boyut, aynı renk
    """

    def __init__(self, parent_frame, width, height):
        self.w = width
        self.h = height

        self.packets     = []
        self.nodes       = []
        self.frame_count = 0

        self.canvas = tk.Canvas(
            parent_frame,
            width=width,
            height=height,
            bg=PANEL_COLOR,
            highlightthickness=2,
            highlightbackground=BORDER_COLOR
        )
        self.canvas.pack()

        self._setup_nodes()
        self._draw_static()

    # ──────────────────────────────────────────────────────────
    # KURULUM
    # ──────────────────────────────────────────────────────────

    def _setup_nodes(self):
        """
        7 eş düğüm (peer) çember üzerine yerleştirir.

        Client-Server'dan farkı:
        - Ortada büyük bir sunucu YOK
        - Hepsi aynı boyut (hiyerarşi yok)
        - "peer" tipi (ne sunucu ne istemci, ikisi birden)
        """
        cx = self.w // 2
        cy = self.h // 2 + 15
        count  = 7
        radius = 130

        for i in range(count):
            angle = (360 / count) * i - 90

            nx, ny = circle_point(cx, cy, radius, angle)

            peer = NetworkNode(
                self.canvas, nx, ny,
                label=f"P{i + 1}",
                color=ACCENT_GREEN,
                node_type="peer",
                size=20
            )
            self.nodes.append(peer)

    def _draw_static(self):
        """
        Sabit arka plan öğelerini çizer.

        Client-Server'dan önemli fark:
        - Bağlantı çizgileri MESH şeklinde (herkes herkesle)
        - Çok yoğun olmaması için sadece yakın düğümler bağlanır
        """
        # ── Başlık ────────────────────────────────────────────
        self.canvas.create_text(
            self.w // 2, 18,
            text="PEER  ↔  PEER",
            font=("Courier", 13, "bold"),
            fill=ACCENT_GREEN
        )
        self.canvas.create_text(
            self.w // 2, 35,
            text="Dağıtık Mimari (P2P)",
            font=("Courier", 8),
            fill=DIM_COLOR
        )

        # ── Mesh bağlantı çizgileri ───────────────────────────
        # Kombinasyon: her düğüm çifti bir kez çizilsin
        # i=0..n, j=i+1..n → tekrar yok, aynı çift iki kez yok
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                n1 = self.nodes[i]
                n2 = self.nodes[j]

                # Çok uzak olanları bağlama (görsel karmaşa azalsın)
                # distance() utils.py'den gelir
                if distance(n1.x, n1.y, n2.x, n2.y) < 210:
                    self.canvas.create_line(
                        n1.x, n1.y,
                        n2.x, n2.y,
                        fill=ACCENT_PURPLE,
                        width=1,
                        dash=(3, 5),
                        stipple="gray50"   # Yarı saydam çizgi
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
            ("✓  Tek nokta arızası yok",      ACCENT_GREEN),
            ("✓  Ölçeklenebilir yapı",         ACCENT_GREEN),
            ("✗  Karmaşık yönetim",            ACCENT_RED),
            ("✗  Güvenlik sağlamak zor",       ACCENT_RED),
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
        pkt = AnimatedPacket(
            self.canvas,
            from_node.x, from_node.y,
            to_node.x,   to_node.y,
            color=color,
            size=5,
            label=label
        )
        self.packets.append(pkt)
        from_node.set_active(20)
        to_node.set_active(20)

    def simulate_p2p_transfer(self):
        """
        P2P'de veri transferi:
        - Rastgele iki peer seç
        - DOĞRUDAN gönder (araya sunucu girmiyor!)
        - Bazen birden fazla peer'a aynı anda gönder (broadcast)

        BitTorrent'ta bir parçayı indirirken aynı anda
        birden fazla kaynaktan alırsın — bu tam olarak o!
        """
        if len(self.nodes) < 2:
            return

        # İki farklı peer seç
        # list comprehension ile sender hariç listeyi filtrele
        sender   = random.choice(self.nodes)
        receiver = random.choice([n for n in self.nodes if n != sender])

        # Doğrudan gönder
        self.send_packet(sender, receiver, color=ACCENT_GREEN, label="P2P")

        # Durum güncelle
        self.canvas.itemconfig(
            self.status_id,
            text=f"● {sender.label}  ↔  {receiver.label}  (DOĞRUDAN)",
            fill=ACCENT_GREEN
        )

        # %35 ihtimalle aynı anda başka bir peer'a da gönder
        # Bu P2P'nin "broadcast" / "flood" özelliğini simüle eder
        if random.random() < 0.35:
            extras = [n for n in self.nodes if n not in (sender, receiver)]
            if extras:
                extra = random.choice(extras)
                # 250ms gecikmeyle, paketler üst üste binmesin
                self.canvas.after(
                    250,
                    lambda: self.send_packet(
                        sender, extra,
                        color=ACCENT_PURPLE,
                        label="bcast"
                    )
                )

    # ──────────────────────────────────────────────────────────
    # ANİMASYON DÖNGÜSÜ
    # ──────────────────────────────────────────────────────────

    def update(self):
        """
        Her karede çağrılır.
        P2P paneli biraz daha sık simülasyon yapar
        (her 65 kare) → daha dinamik görünsün.
        """
        self.frame_count += 1

        alive = []
        for pkt in self.packets:
            pkt.update()
            if pkt.done:
                pkt.destroy()
            else:
                alive.append(pkt)
        self.packets = alive

        for node in self.nodes:
            node.update()

        # Her 65 karede bir otomatik transfer
        if self.frame_count % 65 == 0:
            self.simulate_p2p_transfer()