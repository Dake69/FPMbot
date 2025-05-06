import qrcode

telegram_link = "https://t.me/italksdnubot?start=qr_code_123123"
qr = qrcode.make(telegram_link)
qr.save("telegram_qr.png")