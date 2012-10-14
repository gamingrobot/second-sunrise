#! /bin/bash
# -*- coding: utf-8 -*-

openssl pkcs12 -in cert.p12 -out cert.pem -nodes -clcerts
multify -r -f naith.p3d -P "#! /usr/bin/env panda3d" -S cert.pem
rm cert.pem
chmod 755 naith.p3d
