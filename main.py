import time, math
import os, sys
import numpy as np
from multiprocessing import Process, Lock
import cert_information as ci
import pandas as pd
import ssl

dir  = "./"+sys.argv[1].strip()
[subfolders] = os.walk(dir)

start = time.time()

df = pd.read_csv('PublicAllIntermediateCertsWithPEMReport.csv')
intermediates = []
# for c in df['PEM']:
for c in df['PEM Info']:
    intermediates.append(ssl.PEM_cert_to_DER_cert(str(c)))

for file in subfolders[2]:
    domains = []
    lock = Lock()
    p = 1   # Number of threads
    arq = open(dir+'/'+file, "r")
    for domain in arq:
        domains.append(domain.split(","))
    arq.close()
    if len(domains) > 0:
        n = int(math.ceil(len(domains)/p))
        Domains = [domains[i * n:(i + 1) * n] for i in range((len(domains) + n - 1) // n )]
        domains.clear()
        for i in range(len(Domains)):
            ts = ci.CertificateSanityCheck(Domains[i],intermediates, lock)
            Process(target=ts.process_cert(), args=(lock,Domains[i],)).start()
            
print('Sorting and removing duplicate items...\nThis process may take some time.')
os.system("sort ./Out/modulus_file.txt | uniq -u > ./Out/modulus.txt")
os.system("sort ./Out/ec_public_key_file.txt | uniq -u > ./Out/ec_public_key.txt")

end = time.time()
print("Time used: ",end - start)

# ts.ffmethod()
# ts.calc_gcd()
