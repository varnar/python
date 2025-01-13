import qrcode

data = input("Enter the data you want to store in the QR code: ").strip()
filename = input("Enter the filename you want to save the QR code as: ").strip() + ".png"
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(data)
image =  qr.make_image(fill_color="black", back_color="white")
image.save(filename)
print(f"QR code saved as {filename}")
image.show()   
