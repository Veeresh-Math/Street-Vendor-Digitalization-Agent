"""
QR Code + Business Card Generator
Uses: qrcode + Pillow (non-AI, no external API)
Generates:
  1. Plain QR PNG  (UPI payment link)
  2. Business card PNG  (vendor name + QR + location, Indian aesthetic)
"""

import os
import io
import uuid
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont

# Output directory (served as static files by FastAPI)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colours (Indian street-market palette)
INDIGO      = (27,  42,  107)   # #1B2A6B
TURMERIC    = (245, 166,  35)   # #F5A623
KRAFT       = (200, 169, 110)   # #C8A96E
KRAFT_LIGHT = (253, 246, 227)   # #FDF6E3
RICKSHAW    = (45,  106,  79)   # #2D6A4F
WHITE       = (255, 255, 255)
BLACK       = (20,  20,   20)


def _upi_url(upi_id: str, vendor_name: str, amount: str = "") -> str:
    """Build a standard UPI deep-link URL."""
    name = vendor_name.replace(" ", "%20")
    url  = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"
    if amount:
        url += f"&am={amount}"
    return url


def generate_qr(upi_id: str, vendor_name: str) -> str:
    """
    Generate a styled QR code PNG for the vendor's UPI ID.
    Returns the file path (relative to project root).
    """
    url = _upi_url(upi_id, vendor_name)

    qr = qrcode.QRCode(
        version         = 1,
        error_correction= qrcode.constants.ERROR_CORRECT_H,
        box_size        = 10,
        border          = 3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory  = StyledPilImage,
        module_drawer  = RoundedModuleDrawer(),
        back_color     = KRAFT_LIGHT,
        fill_color     = INDIGO,
    )

    filename = f"qr_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    return f"/static/generated/{filename}"


def generate_business_card(
    vendor_name  : str,
    business_type: str,
    location     : str,
    upi_id       : str,
) -> str:
    """
    Generate a business card PNG (Indian street-market style).
    Card size: 800 × 450 px.
    Returns file URL path.
    """
    W, H = 800, 460

    card = Image.new("RGB", (W, H), KRAFT_LIGHT)
    draw = ImageDraw.Draw(card)

    # ── Background stripes (Indian textile feel) ──────────────────────────────
    for y in range(0, H, 20):
        if (y // 20) % 5 == 0:
            draw.rectangle([(0, y), (W, y + 3)], fill=(*KRAFT, 180))

    # ── Top colour bar ────────────────────────────────────────────────────────
    draw.rectangle([(0, 0), (W, 60)], fill=INDIGO)

    # ── Turmeric accent stripe ────────────────────────────────────────────────
    draw.rectangle([(0, 60), (W, 68)], fill=TURMERIC)

    # ── Bottom colour bar ─────────────────────────────────────────────────────
    draw.rectangle([(0, H - 50), (W, H)], fill=RICKSHAW)
    draw.rectangle([(0, H - 58), (W, H - 50)], fill=TURMERIC)

    # ── Fonts (fallback to default if Noto not installed) ─────────────────────
    try:
        font_big   = ImageFont.truetype("NotoSans-Bold.ttf",   36)
        font_med   = ImageFont.truetype("NotoSans-Regular.ttf",22)
        font_small = ImageFont.truetype("NotoSans-Regular.ttf",16)
        font_upi   = ImageFont.truetype("NotoSans-Bold.ttf",   18)
    except IOError:
        font_big   = ImageFont.load_default()
        font_med   = font_big
        font_small = font_big
        font_upi   = font_big

    # ── Header text (vendor name on indigo bar) ───────────────────────────────
    draw.text((24, 14), vendor_name.upper(), font=font_big, fill=WHITE)

    # ── Business type + location ──────────────────────────────────────────────
    draw.text((24, 88),  business_type, font=font_med,   fill=INDIGO)
    draw.text((24, 118), f"📍 {location}",  font=font_med,   fill=INDIGO)

    # ── Divider ───────────────────────────────────────────────────────────────
    draw.line([(24, 155), (490, 155)], fill=(*KRAFT, 200), width=2)

    # ── UPI label ────────────────────────────────────────────────────────────
    draw.text((24, 168), "💳 Scan & Pay (UPI)",      font=font_small, fill=RICKSHAW)
    draw.text((24, 192), upi_id,                     font=font_upi,   fill=INDIGO)
    draw.text((24, 222), "Accepts: PhonePe · Paytm · GPay · BHIM",
              font=font_small, fill=(*BLACK, 180))

    # ── "SVDA — IBM watsonx.ai" badge ─────────────────────────────────────────
    badge_text = "Street Vendor Digitalization Agent · IBM watsonx.ai"
    draw.text((24, H - 40), badge_text, font=font_small, fill=WHITE)

    # ── QR code (right side) ─────────────────────────────────────────────────
    upi_url = _upi_url(upi_id, vendor_name)
    qr      = qrcode.QRCode(version=1,
                             error_correction=qrcode.constants.ERROR_CORRECT_H,
                             box_size=7, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        back_color=KRAFT_LIGHT,
        fill_color=INDIGO,
    ).get_image().convert("RGBA")

    # Scale QR to 240×240
    qr_img = qr_img.resize((240, 240), Image.LANCZOS)

    # Paste on card (right side, vertically centred)
    qr_x = W - 265
    qr_y = (H - 240) // 2
    card.paste(qr_img, (qr_x, qr_y))

    # QR border
    draw.rectangle([(qr_x - 4, qr_y - 4), (qr_x + 244, qr_y + 244)],
                   outline=TURMERIC, width=3)

    # ── Torn-receipt bottom perforations ─────────────────────────────────────
    for x in range(0, W, 18):
        draw.ellipse([(x, H - 52), (x + 8, H - 44)], fill=KRAFT_LIGHT)

    # ── Save ──────────────────────────────────────────────────────────────────
    filename = f"card_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    card.save(filepath)
    return f"/static/generated/{filename}"
