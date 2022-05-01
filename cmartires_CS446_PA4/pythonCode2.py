#Set up a docker environment for this code, and don't try to include superfluous 
#packages!
from PIL import Image, ImageDraw
import csv
from scipy import constants
import numpy as np

from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

import os

color = 128 * np.ones(shape=[3], dtype=np.uint8)
tuplevals = tuple(color)
im = Image.new('RGB', (512, 512), tuplevals)
draw = ImageDraw.Draw(im)
draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
draw.text((100, 200), "You did it!", fill=(int(constants.speed_of_light), 0, 0))
im.save( "pythonCode2Image.png")

try:
    with open('temp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
except:
    pass

CN = gethostname()
CERT_FILE = "cmartires_selfSignedCertificate.crt"
KEY_FILE = "cmartires_privateKey.pem"

cert_dir="."
C_F = join(cert_dir, CERT_FILE)
K_F = join(cert_dir, KEY_FILE)

if not exists(C_F) or not exists(K_F):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "NV"
    cert.get_subject().L = "Reno"
    cert.get_subject().O = "University of Nevada, Reno"
    cert.get_subject().OU = "CSE"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(42)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(156780000)
    cert.set_pubkey(k)
    cert.set_issuer(cert.get_subject())
    cert.sign(k, 'sha512')
    open(C_F, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(K_F, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    os.system("openssl rsa -in cmartires_privateKey.pem -pubout -out cmartires_publicKey.pem")

#modify this code so that it also generates self signed certificate and keys