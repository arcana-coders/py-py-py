import qrcode

def main ():
    url = input("url a qr: ")
    nameqr = input("nombre del codigo? ")
    createqr(url, nameqr)
    



def createqr (url, nameqr):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    if True:
        img.save(f'{nameqr}_qr.png')
        print("codigo realizado")

    
    ...




if __name__=="__main__":
    main()