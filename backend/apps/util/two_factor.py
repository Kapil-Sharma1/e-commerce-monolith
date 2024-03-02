import requests

from dj_rest_auth.utils import jwt_encode
from django.conf import settings

from apps.users.models import User


class TwoFactor():
    api_key = settings.TWO_FACTOR_API_KEY
    base_url = settings.TWO_FACTOR_BASE_URL
    
    def generate_otp(self, phone_number):
        try:

            url = f"{self.base_url}/{self.api_key}/SMS/{phone_number}/AUTOGEN"

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request(
                "GET", url, data=payload, headers=headers)
            return response

        except Exception as e:
            return e

    def verify_otp(self, otp, otp_session_id):
        try:
            url = f"http://2factor.in/API/V1/{self.api_key}/SMS/VERIFY/{otp_session_id}/{otp}"

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=payload, headers=headers)
            return response

        except Exception as e:
            return e

