
arq = open('links1.txt', "r")
arq1 = open('onlyCerts.txt', "w")

for f in arq:
    if f.find("get_443_certs.gz") >= 0:
        arq1.write(f.strip()+'\n')
        print(f.strip())

arq.close()