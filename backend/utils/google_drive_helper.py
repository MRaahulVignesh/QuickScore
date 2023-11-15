from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleDrive:
    def __init__(self):
        client_id = (
            "890355336997-e69t8ter89posnkgmbpnn7hmcr1gh6vo.apps.googleusercontent.com"
        )
        project_id = "quickscore-405104"
        client_secret = "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"
        private_key = (
            "-----BEGIN PRIVATE KEY-----\n{}\n-----END PRIVATE KEY-----\n".format(
                client_secret
            )
        )
        credentials = {
            "type": "service_account",
            "project_id": "quickscore-405104",
            "private_key_id": "d27b27f164008e1784728bda2bb56316dc46cc9d",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDF7vnncdyV+5+k\n+a8FnAE+bLdvxUPiPY1QIL/rAyIbnrMNOqe76Ooh6K2yCGm5q/yMi8SP5id0qxIc\nRUP2F3UmR1ifyCAAKJCALtyb1IdoKrUF8xKJZR01muJ0wFXKoieJ2crNTjf4SIm3\nCQsxxKHQBisybzUDF3AAMQQF3EbaLCga2M5p9mAs2re4GTSH7BRlg6+mJIh4sGjP\nSURN9S0XjCD230U1jaipxybf3Y0FLycqeqq4x02BtBVLdi4V2ddXEp34oqLryu7L\n+zIxF59YGbIx/yk106Ov/aDMNQOaToqfpQKzx7Q85msJmGMjxexmcG8tS0tseueu\nnYGlutDZAgMBAAECggEACD5bPyXxW3fG3t6dSP0F2j056JhNKvuISqmKhLW1MnRK\nHcdvG/bn5XCk51DNYnPEyW+6yIl75DKJxw6ldXblpKn9CW6S0p7d4dDR1FWmLBL3\nRh+pCnrhHA3u15D5Ib7eKbId7a4Py7HttmdUhYacfKb9HpUeHppXylJASiQx+T0h\nyx9mcneKY3vq+ywX0/Uzv+hmF+zqKhPy90cEnKE9iPAE5juYfduzyGUAalFASLA9\n7VO5llAOEKFT0aMqLh/LGXxBYz5SKICQQtevGPb0jgN226l+sexoBQduo/O0b3aV\nDmp0i4Z8D0NSSmy1NXvB3qc8oWJ6yeiyjNdYLDnLlwKBgQDr2SMdHnZWXgjGGwJf\nO2Nb7OZWuNHUrXcDbPD6sGpgKjfwLZpJ3Li3nVA+nrULwPBz6iDo1T/tiN6E7UgD\nIBT6H9YCiYxIKipGRy/CxZMVLC5BOU3dhjOYpmezzYlnt9lTEKFUSYUbogaT/6zA\n/3HvahAqdKZ/gyknSIMmoXEZuwKBgQDW2IGJ6mG19Q7FGg64aCcEzlMoyEZ0THTO\n1HEm/jTrlGkq/pbu7JRynE/QiuiT17o1/P69/jLhqpOWX665ZmnR407oe4q119XE\nAg50MHjQbFoIJjHNK78vzyiw+uLootHVOE3reWeKm2bAgYzAjxB5IBmeL4MoEhKK\nd0bDigkcewKBgFL8cFKKqXDyXXv3fPotV2S9Er9pAMwozTuzVYegE44KzOwB38wl\nkglpnRarmWCtXu4qb7H9dyUJh+KV60TOQRNRqGf0JhwuWfmoirGp+3rztMLWewN7\neSQ5STwHElYgZqPHsjyKMf/rHw1sZUjzmQ947n9B1GQBrrVX2m35WGaJAoGAVadb\nfbCD5BcfHFWXKM3dQH1BijDOZe9VYmAv/Gu8jW9NvmZhpj+Lr2XCLFI1BzwqcPu8\nU+LURkPLM1hSQHgkGBmXi/g1BOpXvx1Sxd/NSsrn2ffgQvv97QGaJ3TeogDHx0n7\nRrXQIeJyxKzhgKOI3cF+dSJcF82ctrd27t5JY6ECgYAyMvKPw5J1n/mX2uNfCWmF\nrXXO5ePEHoKnaKPmgDWe2MTPWvuwpttZMnaDoCxBvUiwg3TT0oOErS/PESuVAACJ\nMdyiC1Rn0zJ34e2kyFZ07q+a1i0ZYlZ1bT8rSW+hHMqNM5YLBx3Rs1lIpQ+/ynCx\nX9oA4QrVLtzWmWdQpkWNCw==\n-----END PRIVATE KEY-----\n",
            "client_email": "python-client@quickscore-405104.iam.gserviceaccount.com",
            "client_id": "117361356848551908027",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-client%40quickscore-405104.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com",
        }

        self.creds = service_account.Credentials.from_service_account_info(
            credentials, scopes=["https://www.googleapis.com/auth/drive"]
        )

    def get_files(self):
        service = build("drive", "v3", credentials=self.creds)
        results = service.files().list().execute()
        files = results.get("files", [])

        if not files:
            print("No files found.")
        else:
            print("Files:")
            for file in files:
                print(f"{file['name']} ({file['id']})")


gd = GoogleDrive()
gd.get_files()
