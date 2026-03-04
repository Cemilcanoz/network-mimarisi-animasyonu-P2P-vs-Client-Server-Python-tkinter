# ─────────────────────────────────────────────
#  utils.py  —  Yardımcı (utility) fonksiyonlar
#
#  Birden fazla sınıfın kullandığı küçük
#  matematik fonksiyonları burada toplanır.
#  Böylece her sınıf dosyasında tekrar yazmak
#  gerekmez — sadece "from utils import ..." der.
# ─────────────────────────────────────────────

import math   # sin, cos, hypot için


def circle_point(cx, cy, radius, angle_deg):
    """
    Bir çemberin üzerindeki noktanın koordinatını döndürür.

    Trigonometri:
        x = merkez_x + r * cos(açı)
        y = merkez_y + r * sin(açı)

    Örnek kullanım:
        x, y = circle_point(250, 250, 130, 90)
        # 250,250 merkezli, yarıçapı 130 olan çemberin
        # 90 derece noktasını verir (tam aşağı)
    """
    rad = math.radians(angle_deg)         # Derece → Radyan
    x   = cx + radius * math.cos(rad)
    y   = cy + radius * math.sin(rad)
    return x, y


def lerp(a, b, t):
    """
    Linear interpolation — iki değer arasında düzgün geçiş.

    t=0.0  → a değerini döndürür  (başlangıç)
    t=0.5  → a ile b'nin ortasını döndürür
    t=1.0  → b değerini döndürür  (hedef)

    Animasyonda paketin A noktasından B noktasına
    YAVAŞÇA kayması için her karede t'yi artırırız.
    """
    return a + (b - a) * t


def distance(x1, y1, x2, y2):
    """
    İki nokta arasındaki düz çizgi mesafesi.
    math.hypot = sqrt(dx² + dy²) kısaltması.
    """
    return math.hypot(x2 - x1, y2 - y1)