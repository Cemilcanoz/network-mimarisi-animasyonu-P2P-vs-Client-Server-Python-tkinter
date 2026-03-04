# ─────────────────────────────────────────────
#  config.py  —  Tüm renk ve sabit değerler
#
#  Neden ayrı dosya?
#  Bir rengi değiştirmek istersen sadece buraya
#  bakman yeterli. Dağınık olmaz.
# ─────────────────────────────────────────────

# Arka plan renkleri
BG_COLOR     = "#0a0e1a"   # Ana arka plan (koyu lacivert)
PANEL_COLOR  = "#111827"   # Panel arka planı
BORDER_COLOR = "#1e3a5f"   # Kenarlık rengi

# Metin renkleri
TEXT_COLOR   = "#e2e8f0"   # Ana metin (açık gri)
DIM_COLOR    = "#64748b"   # Soluk metin (orta gri)

# Vurgu renkleri
ACCENT_BLUE   = "#3b82f6"  # Sunucu (server) rengi
ACCENT_GREEN  = "#22c55e"  # P2P peer rengi
ACCENT_ORANGE = "#f97316"  # Client rengi
ACCENT_RED    = "#ef4444"  # Hata / olumsuz
ACCENT_YELLOW = "#eab308"  # Veri paketi rengi
ACCENT_PURPLE = "#a855f7"  # P2P bağlantı rengi
LINE_COLOR    = "#1e40af"  # Bağlantı çizgisi

# Animasyon ayarları
FPS        = 60            # Saniyedeki kare sayısı
FRAME_MS   = 1000 // FPS  # Her kare kaç milisaniye (≈16ms)