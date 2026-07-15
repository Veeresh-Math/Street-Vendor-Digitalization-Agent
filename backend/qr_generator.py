"""
QR Code + Business Card Generator
Uses: qrcode + Pillow (non-AI, no external API)
Returns base64 data URIs so images work on any deployment (no filesystem dependency).
"""

import os
import io
import base64
import qrcode
from PIL import Image, ImageDraw, ImageFont

INDIGO      = (27,  42,  107)
TURMERIC    = (245, 166,  35)
KRAFT       = (200, 169, 110)
KRAFT_LIGHT = (253, 246, 227)
RICKSHAW    = (45,  106,  79)
WHITE       = (255, 255, 255)
BLACK       = (20,  20,   20)


def _upi_url(upi_id: str, vendor_name: str, amount: str = "") -> str:
    name = vendor_name.replace(" ", "%20")
    url  = f"upi://pay?pa={upi_id}&pn={name}&cu=INR"
    if amount:
        url += f"&am={amount}"
    return url


def _img_to_data_uri(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def generate_qr(upi_id: str, vendor_name: str) -> str:
    url = _upi_url(upi_id, vendor_name)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=INDIGO, back_color=KRAFT_LIGHT)
    return _img_to_data_uri(img)


def generate_business_card(
    vendor_name: str,
    business_type: str,
    location: str,
    upi_id: str,
) -> str:
    W, H = 800, 460
    card = Image.new("RGB", (W, H), KRAFT_LIGHT)
    draw = ImageDraw.Draw(card)

    for y in range(0, H, 20):
        if (y // 20) % 5 == 0:
            draw.rectangle([(0, y), (W, y + 3)], fill=KRAFT)

    draw.rectangle([(0, 0), (W, 60)], fill=INDIGO)
    draw.rectangle([(0, 60), (W, 68)], fill=TURMERIC)
    draw.rectangle([(0, H - 50), (W, H)], fill=RICKSHAW)
    draw.rectangle([(0, H - 58), (W, H - 50)], fill=TURMERIC)

    font = ImageFont.load_default()

    draw.text((24, 14), vendor_name.upper(), font=font, fill=WHITE)
    draw.text((24, 88), business_type, font=font, fill=INDIGO)
    draw.line([(24, 155), (490, 155)], fill=KRAFT, width=2)
    draw.text((24, 168), "Scan & Pay (UPI)", font=font, fill=RICKSHAW)
    draw.text((24, 192), upi_id, font=font, fill=INDIGO)
    draw.text((24, 222), "Accepts: PhonePe, Paytm, GPay, BHIM", font=font, fill=BLACK)
    draw.text((24, H - 40), "Street Vendor Digitalization Agent", font=font, fill=WHITE)

    upi_url = _upi_url(upi_id, vendor_name)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=7, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=INDIGO, back_color=KRAFT_LIGHT).convert("RGBA")
    qr_img = qr_img.resize((240, 240), Image.LANCZOS)

    qr_x = W - 265
    qr_y = (H - 240) // 2
    card.paste(qr_img, (qr_x, qr_y))
    draw.rectangle([(qr_x - 4, qr_y - 4), (qr_x + 244, qr_y + 244)], outline=TURMERIC, width=3)

    for x in range(0, W, 18):
        draw.ellipse([(x, H - 52), (x + 8, H - 44)], fill=KRAFT_LIGHT)

    return _img_to_data_uri(card)
