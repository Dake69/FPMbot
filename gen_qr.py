import qrcode

telegram_link = "781359"
qr = qrcode.make(telegram_link)
qr.save("telegram_qr.png")