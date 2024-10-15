#!/bin/env python3

# check_ssl_cert.py - python get info for expired SSL cert
# Copyright 2022 Sharuzzaman Ahmat Raslan <sharuzzaman@gmail.com>

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License along with this program. If not, see https://www.gnu.org/licenses/.

from cryptography import x509
import socket
import ssl
import sys

hostname = sys.argv[1]

# create default context
context = ssl.create_default_context()

# override context so that it can get expired cert
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print("SSL/TLS version:", ssock.version())
        print()

        # get cert in DER format
        data = ssock.getpeercert(True)
        print("Data:", data)
        print()

        # convert cert to PEM format
        pem_data = ssl.DER_cert_to_PEM_cert(data)
        print("PEM cert:", pem_data)

        # pem_data in string. convert to bytes using str.encode()
        # extract cert info from PEM format
        cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))

        # show cert expiry date
        print("Expiry date:", cert_data.not_valid_after)
        print()