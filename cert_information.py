import ssl
import os
import traceback
from asn1crypto import pem
from asn1crypto.x509 import Certificate
from certvalidator import CertificateValidator, errors
from certvalidator.path import ValidationPath
from OpenSSL import crypto

# from gmpy3 import mpz, gcd
#from OpenSSL import crypto

class CertificateSanityCheck:

    def __init__(self, domains,intermediates,lock=1,store = False, database=False):
        self.domains  = domains
        self.lock     = lock
        self.database = database
        self.store    = store
        self.intermediates = intermediates
    
    def get_cert_info(self,cert, log_file, port=444, cert_file_name='cert.der'):

        cert = "-----BEGIN CERTIFICATE-----\n"+cert+"-----END CERTIFICATE-----\n"
    
        f = open(str(cert_file_name), 'wb')

        try:
            certificate1 = crypto.load_certificate(crypto.FILETYPE_PEM, cert.encode())
        except:
            certificate1 = 'none'

        try:
            has_expired = certificate1.has_expired()
        except:
            has_expired = 'none'


        f.write(ssl.PEM_cert_to_DER_cert(cert))
        f.close()

        with open(str(cert_file_name), "rb") as f:
            end_entity_cert = f.read()
            certificate = Certificate.load(end_entity_cert)

        algorithm  = certificate.public_key.native["algorithm"]["algorithm"]
        if algorithm == 'rsa' :
            curve      = 'none' # apenas para EC 
            public_key = 1 # apenas para EC
            # modulus    = certificate.public_key.native["public_key"]["modulus"]
            modulus    = hex(certificate.public_key.native["public_key"]["modulus"])
            pub_exp    = certificate.public_key.native["public_key"]["public_exponent"]
            key_size   = int(certificate.public_key.bit_size)

        elif algorithm == 'ec' :
            curve      = certificate.public_key.native["algorithm"]["parameters"]
            public_key = certificate.public_key.native["public_key"].hex()
            modulus    = 1
            pub_exp    = 1
            #public_key = int(certificate.public_key.native["public_key"].hex(),17) # Public_key em decimal
            key_size   = int(certificate.public_key.bit_size)
        else:
            try:
                curve      = certificate.public_key.native["algorithm"]["parameters"]
            except:
                curve = 'none'
            try:
                public_key = certificate.public_key.native["public_key"].hex()
            except:
                public_key = 'none'
            try:
                modulus    = certificate.public_key.native["public_key"]["modulus"]
            except:
                modulus    = 1
            try:
                pub_exp    = certificate.public_key.native["public_key"]["public_exponent"]
            except:
                pub_exp    = 1
            try:
                key_size   = int(certificate.public_key.bit_size)
            except:
                key_size   = 1 
            #public_key = int(certificate.public_key.native["public_key"].hex(),17) # Public_key em decimal

        #modulus = certificate.public_key.native["public_key"]["modulus"]
        #pub_exp = certificate.public_key.native["public_key"]["public_exponent"]
        #sig_algorithm = certificate.signature_algo
        try:
            cert_issuer_country = certificate.issuer.native["country_name"]
        except:
            cert_issuer_country = "Empty"
        try:
            cert_issuer_name = certificate.issuer.native["organization_name"]
        except:
            cert_issuer_name = "Empty"
        try:
            cert_issuer_common_name = certificate.issuer.native["common_name"]
        except:
            cert_issuer_common_name = "Empty"
        
        sig_algorithm = certificate.signature_algo
        self_signed = certificate.self_signed
        hash_algo = certificate.hash_algo
        domains = certificate.valid_domains
        not_valid_before = certificate.native['tbs_certificate']['validity']['not_before']
        not_valid_after  = certificate.native['tbs_certificate']['validity']['not_after']
        
        # try:
        #     has_expired = certificate2.has_expired()
        # except:
        #     has_expired = "Empty"

        try:
            cert_subject_common_name = certificate.subject.native["common_name"]
        except:
            cert_subject_common_name = "Empty"
        try:
            cert_subj_country = certificate.subject.native["country_name"]
        except:
            cert_subj_country = "Empty"

        # print(cert_subject_common_name)
        # print(cert_issuer_common_name)
        # print(algorithm)
        path = []
        # print(not has_expired)
        if not has_expired:
            path = self.path_verify(end_entity_cert,log_file,cert_subject_common_name)
            # print(has_expired)
        
        if len(path)>0:
            is_valid = True
        else:
            is_valid = False
        # print(path)
        os.remove(str(cert_file_name))
        # '{1:02x}'.format(modulus),
        return (modulus, pub_exp, algorithm,curve,public_key,key_size,
               cert_subj_country,not_valid_before,not_valid_after,is_valid,path,sig_algorithm,cert_issuer_country, 
               cert_issuer_name, cert_issuer_common_name,self_signed, hash_algo, domains,cert_subject_common_name,has_expired)

    def process_cert(self):
        
        data_file = open('./Out/complete_output.txt', 'a')
        modulus_file = open('./Out/modulus_file.txt', 'a')
        ec_public_key_file = open('./Out/ec_public_key_file.txt', 'a')
        log_file = open('./Out/log.txt', 'a')
        size = len(self.domains)
        
        for domain in self.domains:
            try:
                print('Process PID: %s - %d of %d\n\
                    Domain: %s' % (os.getpid(), size, len(self.domains), domain[0]))
                # print(domain[0])
                # print(domain[1])
                # print("Foi1")
                # print(self.get_cert_info(domain[1]))
                cert = self.get_cert_info(domain[1],log_file)
                print(str(cert[8])+'\t'+str(cert[-1])+'\t'+str(cert[9])+'\t'+str(cert[10]))
                # print(str(cert[2]))
                # print("Foi2")
                self.lock.acquire()
                if cert[2] == 'rsa':
                    data_file.write(str(cert[18])+'\t'+str(cert[6])+'\t'+str(cert[2])
                                    +'\t'+str(cert[0])+'\t'+str(cert[1])+'\t' +
                                    str(cert[5])+'\t'+ str(cert[7])
                                    + '\t'+str(cert[8])+'\t'+str(cert[-1]) +'\t'+
                                    str(cert[9])+'\t'+str(cert[10])
                                    + '\t'+str(cert[11])+'\t'+
                                    str(cert[12])+'\t'+str(cert[13])
                                    +'\t'+str(cert[14])+'\t'+str(cert[15])
                                    +'\t'+str(cert[16]) +'\t'+str(cert[17]) +'\n')
                                            
                    modulus_file.write(str(cert[0])+'\n')
                if cert[2] == 'ec':
                    data_file.write(str(cert[18])+'\t'+str(cert[6])+'\t'+str(cert[2])
                                    +'\t'+str(cert[3])+ '\t'+str(cert[4])+'\t' +
                                    str(cert[5])+'\t'+str(cert[7])
                                    + '\t'+str(cert[8])+'\t' +str(cert[-1]) +'\t'+
                                    str(cert[9])+'\t'+str(cert[10])
                                    + '\t'+str(cert[11])+'\t'+
                                    str(cert[12])+'\t'+str(cert[13])
                                    +'\t'+str(cert[14])+'\t'+str(cert[15])
                                    +'\t'+str(cert[16]) +'\t'+str(cert[17]) +'\n')
                    
                    ec_public_key_file.write(str(cert[4])+'\n')  
                self.lock.release()
                size -= 1
            except Exception:
                error = traceback.format_exc()
                linesoferror = error.split('\n')
                log_file.write('[ERROR] -  to obtain the certificate \n\
                                Domain: %s\n\
                                Type of error: %s\n' % (domain[0], linesoferror[-2])
                               )
                size -= 1
                continue
        
        data_file.close()
        modulus_file.close()
        log_file.close()
        ec_public_key_file.close()
   
    def path_verify(self,end_entity_cert,log_file,cert_subject_common_name):
        
        path = []
        try:
            validator = CertificateValidator(end_entity_cert,self.intermediates)
            a = validator.validate_usage(set(['digital_signature']))
            #  ValidationPath._certs
            # print(len(a._certs))
            for i in range(len(a._certs)):
                path.append(a._certs[i].issuer.native["common_name"])
                # print(a._certs[i].issuer.native["common_name"], end = '\t')
            # return path
        except:
            log_file.write('[ERROR] -  to obtain the certificate \n\
                                Domain: %s\n\
                                Type of error:Cannot Obtain Path Validation\n' % (cert_subject_common_name)
                               )
            # print('Cannot Obtain Path Validation')
            # print('\n')
        return path
        