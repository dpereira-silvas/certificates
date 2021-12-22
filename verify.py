import ssl
import os
import traceback
from asn1crypto import pem
from asn1crypto.x509 import Certificate
from certvalidator import CertificateValidator, errors
from certvalidator.path import ValidationPath
import pandas as pd

def path_verify(cert,intermediates):
    cert = "-----BEGIN CERTIFICATE-----\n"+cert+"-----END CERTIFICATE-----\n"

    f = open('cert.der', 'wb')
    f.write(ssl.PEM_cert_to_DER_cert(cert))
    f.close()

    with open('cert.der', "rb") as f:
        end_entity_cert = f.read()
        certificate = Certificate.load(end_entity_cert)

    not_valid_after  = certificate.native['tbs_certificate']['validity']['not_after']
    self_signed = certificate.self_signed
    try:
        cert_issuer_common_name = certificate.issuer.native["common_name"]
    except:
        cert_issuer_common_name = "Empty"
    try:
        cert_subject_common_name = certificate.subject.native["common_name"]
    except:
        cert_subject_common_name = "Empty"

    # print("Not Valid After {} ".format(not_valid_after))
    # print("Self Signed {} ".format(self_signed))
    # print("Issuer Common Name {} ".format(cert_issuer_common_name))
    # print("Subject Common Name {} ".format(cert_subject_common_name))
    print(str(not_valid_after)+'\t'+str(self_signed)+'\t'+str(cert_issuer_common_name)+'\t'+str(cert_subject_common_name))
    try:
        validator = CertificateValidator(end_entity_cert,intermediates)
        a = validator.validate_usage(set(['digital_signature']))
        # ValidationPath._certs
        print(len(a._certs))
        for i in range(len(a._certs)):
            print(a._certs[i].issuer.native["common_name"], end = '\t')
        # print(a._certs[1].issuer.native["common_name"])
        # print(a._certs[2].issuer.native["common_name"])
        # validator.validate_tls('google.com')
        print('\n\n')
    # except (errors.PathValidationError):
    except:
        print('Cannot Obtain Path Validation')
        print('\n')

# df = pd.read_csv('MozillaIntermediateCerts.csv')

df = pd.read_csv('PublicAllIntermediateCertsWithPEMReport.csv')
# print(str(df['PEM'][0]))

# f = open('cert.der', 'wb')
# f.write(ssl.PEM_cert_to_DER_cert(str(df['PEM'][3])))
# f.close()

end_entity_cert = None
intermediates = []
# for c in df['PEM']:
for c in df['PEM Info']:
    intermediates.append(ssl.PEM_cert_to_DER_cert(str(c)))

# cert = "MIIEhjCCA26gAwIBAgIQJFd1/sRTtLAKAAAAAP9mCzANBgkqhkiG9w0BAQsFADBGMQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExMQzETMBEGA1UEAxMKR1RTIENBIDFDMzAeFw0yMTA5MTMwNDA3MTNaFw0yMTExMjAwNDA3MTJaMBkxFzAVBgNVBAMTDnd3dy5nb29nbGUuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAET7cCwapWtaJhYMcEn2wpNjXZS8mbM2Ww5HFVWaYKmFjL63HezQbV37uNY1jKLlrK0ovXDpyy48tkS0CykCdeM6OCAmYwggJiMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBRiegvAjZ8TnJ6XiA2Twd5OEKmR/DAfBgNVHSMEGDAWgBSKdH+vhc3ulc09nNDiRhTzcTUdJzBqBggrBgEFBQcBAQReMFwwJwYIKwYBBQUHMAGGG2h0dHA6Ly9vY3NwLnBraS5nb29nL2d0czFjMzAxBggrBgEFBQcwAoYlaHR0cDovL3BraS5nb29nL3JlcG8vY2VydHMvZ3RzMWMzLmRlcjAZBgNVHREEEjAQgg53d3cuZ29vZ2xlLmNvbTAhBgNVHSAEGjAYMAgGBmeBDAECATAMBgorBgEEAdZ5AgUDMDwGA1UdHwQ1MDMwMaAvoC2GK2h0dHA6Ly9jcmxzLnBraS5nb29nL2d0czFjMy9mVkp4YlYtS3Rtay5jcmwwggEDBgorBgEEAdZ5AgQCBIH0BIHxAO8AdQBc3EOS/uarRUSxXprUVuYQN/vV+kfcoXOUsl7m9scOygAAAXvdjVtAAAAEAwBGMEQCIH6mELn2WioLNsabuvIImi3YBMoCMHdRfWnELlG7V9wqAiBqspdAaqP6dz6/d3VIdSA56yLQxFAxPVW0c0bnfBslWAB2AH0+8viP/4hVaCTCwMqeUol5K8UOeAl/LmqXaJl+IvDXAAABe92NW1IAAAQDAEcwRQIhAMNRN+CGpNhpPZjfEwJALqBvQ6K+uuH8XEEK64WaO6GEAiAPNrUXDzM+wquGF6KHGd4IEp7RlqzCw7RUKHJlo+o+cTANBgkqhkiG9w0BAQsFAAOCAQEAn8laXKAkRbaxSE9uvcasJ1CfIu8zYoJCRW8OHJJkd5LUS04mKV8+glfHiJNrlsPbAFbG+CCptL32HTmC69VxqjkrgMRG89aC6iUZkGLWHxajxIEXjA8lwKvm8dhqJsBbhfdSqPIXcrb+i2zLxynVQzzjPj68K0OmtN5XQaUDQD+3xFLFn5B668t8g9ZNPXlR80ZKdBwN/A1R2y+j2vFou5NJ1pDKKinQzLYZij1CbHYPrWM7sDqpSIAB7ZJxhRQphRQFEnp5OgcVHSLSxyo1etcdh4hqQ1GWdWL3958XyqAWYHwKn79G/VlBKiqpGehqbcqdVlNMONjACRYLJhN/SQ=="
# cert = "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"
# cert = "MIIFYjCCBEqgAwIBAgIQd70NbNs2+RrqIQ/E8FjTDTANBgkqhkiG9w0BAQsFADBXMQswCQYDVQQGEwJCRTEZMBcGA1UEChMQR2xvYmFsU2lnbiBudi1zYTEQMA4GA1UECxMHUm9vdCBDQTEbMBkGA1UEAxMSR2xvYmFsU2lnbiBSb290IENBMB4XDTIwMDYxOTAwMDA0MloXDTI4MDEyODAwMDA0MlowRzELMAkGA1UEBhMCVVMxIjAgBgNVBAoTGUdvb2dsZSBUcnVzdCBTZXJ2aWNlcyBMTEMxFDASBgNVBAMTC0dUUyBSb290IFIxMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAthECix7joXebO9y/lD63ladAPKH9gvl9MgaCcfb2jH/76Nu8ai6Xl6OMS/kr9rH5zoQdsfnFl97vufKj6bwSiV6nqlKr+CMny6SxnGPb15l+8Ape62im9MZaRw1NEDPjTrETo8gYbEvs/AmQ351kKSUjB6G00j0uYODP0gmHu81I8E3CwnqIiru6z1kZ1q+PsAewnjHxgsHA3y6mbWwZDrXYfiYaRQM9sHmklCitD38m5agI/pboPGiUU+6DOogrFZYJsuB6jC511pzrp1Zkj5ZPaK49l8KEj8C8QMALXL32h7M1bKwYUH+E4EzNktMg6TO8UpmvMrUpsyUqtEj5cuHKZPfmghCN6J3Cioj6OGaK/GP5Afl4/Xtcd/p2h/rs37EOeZVXtL0m79YB0esWCruOC7XFxYpVq9Os6pFLKcwZpDIlTirxZUTQAs6qzkm06p98g7BAe+dDq6dso499iYH6TKX/1Y7DzkvgtdizjkXPdsDtQCv9Uw+wp9U7DbGKogPeMa3Md+pvez7W35EiEua++tgy/BBjFFFy3l3WFpO9KWgz7zpm7AeKJt8T11dleCfeXkkUAKIAf5qoIbapsZWwpbkNFhHax2xIPEDgfg1azVY80ZcFuctL7TlLnMQ/0lUTbiSw1nH69MG6zO0b9f6BQdgAmD06yK56mDcYBZUCAwEAAaOCATgwggE0MA4GA1UdDwEB/wQEAwIBhjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBTkrysmcRorSCeFL1JmLO/wiRNxPjAfBgNVHSMEGDAWgBRge2YaRQ2XyolQL30EzTSo//z9SzBgBggrBgEFBQcBAQRUMFIwJQYIKwYBBQUHMAGGGWh0dHA6Ly9vY3NwLnBraS5nb29nL2dzcjEwKQYIKwYBBQUHMAKGHWh0dHA6Ly9wa2kuZ29vZy9nc3IxL2dzcjEuY3J0MDIGA1UdHwQrMCkwJ6AloCOGIWh0dHA6Ly9jcmwucGtpLmdvb2cvZ3NyMS9nc3IxLmNybDA7BgNVHSAENDAyMAgGBmeBDAECATAIBgZngQwBAgIwDQYLKwYBBAHWeQIFAwIwDQYLKwYBBAHWeQIFAwMwDQYJKoZIhvcNAQELBQADggEBADSkHrEoo9C0dhemMXoh6dFSPsjbdBZBiLg9NR3t5P+T4Vxfq7vqfM/b5A3Ri1fyJm9bvhdGaJQ3b2t6yMAYN/olUazsaL+yyEn9WprKASOshIArAoyZl+tJaox118fessmXn1hIVw41oeQa1v1vg4Fv74zPl6/AhSrw9U5pCZEt4Wi4wStz6dTZ/CLANx8LZh1J7QJVj2fhMtfTJr9w4z30Z209fOU0iOMy+qduBmpvvYuR7hZL6Dupszfnw0Skfths18dG9ZKb59UhvmaSGZRVbNQpsg3BZlvid0lIKO2d1xozclOzgjXPYovJJIultzkMu34qQb9Sz/yilrbCgj8="
# cert = "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"
# cert = "MIIDlDCCAnygAwIBAgIJAOVM8jCHpwmpMA0GCSqGSIb3DQEBCwUAMBgxFjAUBgNVBAMTDTE4NS42NS4yMDkuNDgwHhcNMTgxMjI0MTkxMjA5WhcNMzgwMTE1MTkxMjA5WjAYMRYwFAYDVQQDEw0xODUuNjUuMjA5LjQ4MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzaHmkZ4RV9rPxqINaWA47QHuq3Uu82oLV4SL3/cVHVhYo1FMzeUMy//3XD2KYqy87LbfpYYShJ6/bmywaMCSMo4ws4yqtRBj3omVNpMZ6R9HpiytDNEQDrlvmPAI1VPfSFa5HQX80h33nmF8GsOf/3ZuY8LEhWal1PT5bcTrqVwbCUHqzDR8DWn0HQrUa3xaNXrsVb7dsg8Pns3NOcbV1iq+TDrZ+2vF6SeXmwuUKvmWCTo2WssdzH0+zj1+B7qq28Iu+GktmEyeV05yDjyBKX6pp0eAElradaXDX9PWaz7NQn/9o76+8qFLaCwDvBTCWtJTNsLPZbzhdzn2bNjNIwIDAQABo4HgMIHdMB0GA1UdDgQWBBQJRvt1tU9Fg0kYr8HrgnqkIej8NzBIBgNVHSMEQTA/gBQJRvt1tU9Fg0kYr8HrgnqkIej8N6EcpBowGDEWMBQGA1UEAxMNMTg1LjY1LjIwOS40OIIJAOVM8jCHpwmpMAwGA1UdEwQFMAMBAf8wZAYDVR0RAQH/BFowWIcEuUHRMIIJZnJpdHouYm94gg13d3cuZnJpdHouYm94ggtteWZyaXR6LmJveIIPd3d3Lm15ZnJpdHouYm94gglmcml0ei5uYXOCDXd3dy5mcml0ei5uYXMwDQYJKoZIhvcNAQELBQADggEBAIZiKnO6gk85U/Gj11fbvpsoFRppbrmWEoC8u3kVzYaJ9VI2Zl2akUlshpwrtVrMfzkVaslkQiNnyYXUni+sNpDv4Se04AKSpdDVeovJ8EFmOHMYwZ2IN5PHZthgaY3JfkwPpl0R16a2kgHh4/xg3bRUVzFxHrOEojmzFyiAXd2HHDjIecr4GWB364ujiOA5dCtS+QsHHJm3wxaLJutn6wXxy1Y7YLqjQmTQlirDLLdX8WhqgsDQDXQBO68Nk3KpvxlQkc+7t8zqPwxwIgba7Rltf12rlIO+gHxNUIYwCxsZ4fvCnlg/+SAJoOMjBxvsbdDO5GiGD+hqZa6DbjhI8OQ="
# cert = "MIIEpzCCA4+gAwIBAgISBGcQcjJe1dozFbG+dEwLXE9FMA0GCSqGSIb3DQEBCwUAMDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQDEwJSMzAeFw0yMTEwMTAwMzAwNDRaFw0yMjAxMDgwMzAwNDNaMBQxEjAQBgNVBAMTCWxlbmNyLm9yZzBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABG9MdN+6Q+ZsgDZ5p7CiEluW1qJYdnlfaD0RuKGNqcdp2EBTHyMC3xTqgsdcXm9X4TL1BtZiMElYOEf2d8onePSjggKeMIICmjAOBgNVHQ8BAf8EBAMCB4AwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFAjvaMQSzzsygZLkrDUsUnIr528RMB8GA1UdIwQYMBaAFBQusxe3WFbLrlAJQOYfr52LFMLGMFUGCCsGAQUFBwEBBEkwRzAhBggrBgEFBQcwAYYVaHR0cDovL3IzLm8ubGVuY3Iub3JnMCIGCCsGAQUFBzAChhZodHRwOi8vcjMuaS5sZW5jci5vcmcvMG8GA1UdEQRoMGaCCWxlbmNyLm9yZ4IPbGV0c2VuY3J5cHQuY29tgg9sZXRzZW5jcnlwdC5vcmeCDXd3dy5sZW5jci5vcmeCE3d3dy5sZXRzZW5jcnlwdC5jb22CE3d3dy5sZXRzZW5jcnlwdC5vcmcwTAYDVR0gBEUwQzAIBgZngQwBAgEwNwYLKwYBBAGC3xMBAQEwKDAmBggrBgEFBQcCARYaaHR0cDovL2Nwcy5sZXRzZW5jcnlwdC5vcmcwggEDBgorBgEEAdZ5AgQCBIH0BIHxAO8AdQDfpV6raIJPH2yt7rhfTj5a6s2iEqRqXo47EsAgRFwqcwAAAXxoXDLXAAAEAwBGMEQCIC5M9ZvPBU21QrhhXqhT369GrHPmWdHznJfo6nvIAJluAiA0aZifnoo6e90+V0+/8nyORISw5I+FOSIj80tpEAIZigB2AEalVet1+pEgMLWiiWn0830RLEF0vv1JuIWr8vxw/m1HAAABfGhcMv4AAAQDAEcwRQIgb8AS9W53S4C6R5Tt7iMJT7f7XiqrFwmMnK45UcngwJsCIQCAAn8LeEUilQhXdPb1MCQMkgCXKzy0yHMCnct6dyD+6TANBgkqhkiG9w0BAQsFAAOCAQEASWkQXzjagSQoyEorW3uapca9DVgHlcctW2D2DcY4VJc8fmIXLw5amd/N8XvrAPrlGjq/LUYObqPVqG7nfar22onZCQIHvJDsDgxqr6bOF0i/8Azaluako/C+pcJt6m0cK9sMseSb+41XXv2uNd5cZ3yCgx5M0PTpnc7GUgz3TvAHs7tc2+ZLrbeHw7eYYmLMWOos631C/xuCYUTqLjvmDAe0eUMC0Lit+BeEEGKAKKbq8swpZBSZenfCZTrAJbl4SzMCWJq5UriJaRNoeDqUqosmA/gK2v3FA9KURSaVYLPzAWAi+pmtouiSUApZQBN4kVmS0OkrWek5QU9vD2b8Og=="
# cert = "MIINxTCCDK2gAwIBAgIRAM+NLp+J8oHpCAfadTGHvS4wDQYJKoZIhvcNAQELBQAwgY8xCzAJBgNVBAYTAkdCMRswGQYDVQQIExJHcmVhdGVyIE1hbmNoZXN0ZXIxEDAOBgNVBAcTB1NhbGZvcmQxGDAWBgNVBAoTD1NlY3RpZ28gTGltaXRlZDE3MDUGA1UEAxMuU2VjdGlnbyBSU0EgRG9tYWluIFZhbGlkYXRpb24gU2VjdXJlIFNlcnZlciBDQTAeFw0yMDEyMDkwMDAwMDBaFw0yMTEyMTAyMzU5NTlaMBQxEjAQBgNVBAMTCWl6aXRvLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANXTR+/u2JbwSTzrxldv+QWL5RvErc1YMZNGLPJg4VZL9X+Xo+orPL/xdE/uT1vX00SHP9vuoZYx9ZFepY0u7M/ncOUU10d/ibeEAJSNuK5vo43hxptU1iPg3hZaHu24EUw5LQKGJl/a0vUljn4DfDbAgr4/19TPA43Qj0FBt+lAUQxHByWPHbF4Hhg2WaOlwlRJ9g+2UVkM2GwuLmMWC4dTwroSM4cjM2N1dr1rpU4tIViCXnpTkafEnUMgU1y2FJ9MGus24w2LjBgPs52LgPfRU6JQT4YITAuu0dkiI527GVnL2bscfY5mtEGz3rPGiF+vmBxpOWlDOQGuCRG01XUCAwEAAaOCCpQwggqQMB8GA1UdIwQYMBaAFI2MXsRUrYrhd+mb+ZsF4bgBjWHhMB0GA1UdDgQWBBRyLErcHU4VkGaCfwvF5s9KxJoIODAOBgNVHQ8BAf8EBAMCBaAwDAYDVR0TAQH/BAIwADAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwSQYDVR0gBEIwQDA0BgsrBgEEAbIxAQICBzAlMCMGCCsGAQUFBwIBFhdodHRwczovL3NlY3RpZ28uY29tL0NQUzAIBgZngQwBAgEwgYQGCCsGAQUFBwEBBHgwdjBPBggrBgEFBQcwAoZDaHR0cDovL2NydC5zZWN0aWdvLmNvbS9TZWN0aWdvUlNBRG9tYWluVmFsaWRhdGlvblNlY3VyZVNlcnZlckNBLmNydDAjBggrBgEFBQcwAYYXaHR0cDovL29jc3Auc2VjdGlnby5jb20wggECBgorBgEEAdZ5AgQCBIHzBIHwAO4AdQB9PvL4j/+IVWgkwsDKnlKJeSvFDngJfy5ql2iZfiLw1wAAAXZGYGXKAAAEAwBGMEQCID6/YtvpNmXAJNa7uUwVE2PupGclwT/cQwgG/USRLmnqAiB19k91CpoM2QTGtVZoRd74e44q+RKcPy7cZjNovj3TBgB1AJQgvB6O1Y1siHMfgosiLA3R2k1ebE+UPWHbTi9YTaLCAAABdkZgZfoAAAQDAEYwRAIgGWX06cjaqizCpWIQPI3wmglTsmy8pokjme/pFc0ebKcCIFI5EKYYax0OqAxE6iD6Sd2VYOqpFqvjfj1L2iyo8kK2MIIINwYDVR0RBIIILjCCCCqCCWl6aXRvLmNvbYILKi5peml0by5jb22CCiouaXppdG8ud3OCESouaXppdG9zZWFyY2guY29tgghpeml0by5hZYIMaXppdG8uYWZyaWNhgghpeml0by5hdIIIaXppdG8uYmGCCGl6aXRvLmJlgglpeml0by5iaXqCCGl6aXRvLmNhgghpeml0by5jaIIIaXppdG8uY2yCC2l6aXRvLmNvLmNyggtpeml0by5jby5pbIILaXppdG8uY28uaW6CC2l6aXRvLmNvLmtyggtpeml0by5jby5ueoILaXppdG8uY28udWuCC2l6aXRvLmNvLnphggxpeml0by5jb20uYXKCDGl6aXRvLmNvbS5hdYIMaXppdG8uY29tLmJvggxpeml0by5jb20uYnKCDGl6aXRvLmNvbS5jb4IMaXppdG8uY29tLmVjggxpeml0by5jb20uZXOCDGl6aXRvLmNvbS5teIIMaXppdG8uY29tLm15ggxpeml0by5jb20ubmeCDGl6aXRvLmNvbS5waIIMaXppdG8uY29tLnB5ggxpeml0by5jb20uc2eCDGl6aXRvLmNvbS5zdoIMaXppdG8uY29tLnRyggxpeml0by5jb20udHeCDGl6aXRvLmNvbS51YYIMaXppdG8uY29tLnZugghpeml0by5jeoIIaXppdG8uZGWCCGl6aXRvLmRrgghpeml0by5lZYIIaXppdG8uZXOCCGl6aXRvLmV1gghpeml0by5maYIIaXppdG8uZnKCCGl6aXRvLmdygghpeml0by5oa4IIaXppdG8uaG6CCGl6aXRvLmh1gghpeml0by5pZYIIaXppdG8uaW6CCml6aXRvLmluZm+CCGl6aXRvLmlzgghpeml0by5pdIIIaXppdG8uanCCCGl6aXRvLmx0gghpeml0by5sdoIIaXppdG8ubXiCCWl6aXRvLm5ldIIIaXppdG8ubmeCCGl6aXRvLm5sgghpeml0by5ub4IJaXppdG8ub3Jngghpeml0by5wZYIIaXppdG8ucGiCCGl6aXRvLnBrgghpeml0by5wbIIIaXppdG8ucHSCCGl6aXRvLnJvgghpeml0by5yc4IIaXppdG8ucnWCCGl6aXRvLnNlgghpeml0by5zaYIIaXppdG8uc2uCCGl6aXRvLnR3gghpeml0by51a4IIaXppdG8udXOCCml6aXRvLndpa2mCCGl6aXRvLndzgg9peml0b3NlYXJjaC5jb22CDHd3dy5peml0by5hZYIQd3d3Lml6aXRvLmFmcmljYYIMd3d3Lml6aXRvLmF0ggx3d3cuaXppdG8uYmGCDHd3dy5peml0by5iZYINd3d3Lml6aXRvLmJpeoIMd3d3Lml6aXRvLmNhggx3d3cuaXppdG8uY2iCDHd3dy5peml0by5jbIIPd3d3Lml6aXRvLmNvLmNygg93d3cuaXppdG8uY28uaWyCD3d3dy5peml0by5jby5pboIPd3d3Lml6aXRvLmNvLmtygg93d3cuaXppdG8uY28ubnqCD3d3dy5peml0by5jby51a4IPd3d3Lml6aXRvLmNvLnphghB3d3cuaXppdG8uY29tLmFyghB3d3cuaXppdG8uY29tLmF1ghB3d3cuaXppdG8uY29tLmJvghB3d3cuaXppdG8uY29tLmJyghB3d3cuaXppdG8uY29tLmNvghB3d3cuaXppdG8uY29tLmVjghB3d3cuaXppdG8uY29tLmVzghB3d3cuaXppdG8uY29tLm14ghB3d3cuaXppdG8uY29tLm15ghB3d3cuaXppdG8uY29tLm5nghB3d3cuaXppdG8uY29tLnBoghB3d3cuaXppdG8uY29tLnB5ghB3d3cuaXppdG8uY29tLnNnghB3d3cuaXppdG8uY29tLnN2ghB3d3cuaXppdG8uY29tLnRyghB3d3cuaXppdG8uY29tLnR3ghB3d3cuaXppdG8uY29tLnVhghB3d3cuaXppdG8uY29tLnZuggx3d3cuaXppdG8uY3qCDHd3dy5peml0by5kZYIMd3d3Lml6aXRvLmRrggx3d3cuaXppdG8uZWWCDHd3dy5peml0by5lc4IMd3d3Lml6aXRvLmV1ggx3d3cuaXppdG8uZmmCDHd3dy5peml0by5mcoIMd3d3Lml6aXRvLmdyggx3d3cuaXppdG8uaGuCDHd3dy5peml0by5oboIMd3d3Lml6aXRvLmh1ggx3d3cuaXppdG8uaWWCDHd3dy5peml0by5pboIOd3d3Lml6aXRvLmluZm+CDHd3dy5peml0by5pc4IMd3d3Lml6aXRvLml0ggx3d3cuaXppdG8uanCCDHd3dy5peml0by5sdIIMd3d3Lml6aXRvLmx2ggx3d3cuaXppdG8ubXiCDXd3dy5peml0by5uZXSCDHd3dy5peml0by5uZ4IMd3d3Lml6aXRvLm5sggx3d3cuaXppdG8ubm+CDXd3dy5peml0by5vcmeCDHd3dy5peml0by5wZYIMd3d3Lml6aXRvLnBoggx3d3cuaXppdG8ucGuCDHd3dy5peml0by5wbIIMd3d3Lml6aXRvLnB0ggx3d3cuaXppdG8ucm+CDHd3dy5peml0by5yc4IMd3d3Lml6aXRvLnJ1ggx3d3cuaXppdG8uc2WCDHd3dy5peml0by5zaYIMd3d3Lml6aXRvLnNrggx3d3cuaXppdG8udHeCDHd3dy5peml0by51a4IMd3d3Lml6aXRvLnVzgg53d3cuaXppdG8ud2lraTANBgkqhkiG9w0BAQsFAAOCAQEAMcA+XF4G7Xgpgv6F7HRNmYQAxrqw5CoBxFwoqONSRKEMW2HYTNG9NRyZtuGtsKtgF2arj5QWGrmjqacaNkb8iJRYsI4/iQ7VyDRx4akO2rx4AcL/oC3lTN7msctf89BEo8x2k2aDwxh81LkLE/IPxG9cbNgORfE4HIlw5MS8ZU3fSwrtLz4lELD1JR/xIX8Sx1ChZqHH5I5DLkZs5t7Zv/BCRmMpElKFENF1kxNkBjgkAJDsdoYS5ZSpAZXDV+ioDjq6FTdyeG9oi+BejVJArvD3bjfgxMCqF5OBOKvqSF3ZfsoveWj9FMNwHs/anwsplQt8j/Obupsxsb8kHxTwrA=="
# cert = "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"
# path_verify(cert,intermediates)

with open('./2019-01-01-1546308539-https_get_443_certs/xaa','r') as f:
    for l in f:
        cert = l.split(",")[1]
        path_verify(cert,intermediates)




# from oscrypto import tls


# session = tls.TLSSession(manual_validation=True)
# connection = tls.TLSSocket('www.google.com', 443, session=session)
# # ValidationPath.__dict__
# try:
#     validator = CertificateValidator(connection.certificate, connection.intermediates)
#     a = validator.validate_tls(connection.hostname)
#     print(a.__dict__)
# except (errors.PathValidationError):
#     print('Error')