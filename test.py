import pytest
import requests

class TestCRUDAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = 'http://127.0.0.1:8000/'  # Replace with your API base URL
        

    def test_create_user(self):
        try:
            ######## input new user info
            body = {
                "name": "presh3",
                "email": "presh3@gmail.com",
                "password": "xxxx",
                "is_admin": False
            }
            auth_endpoint = self.base_url + 'api/users/create-user/'
            
            # First user creation
            response = requests.post(auth_endpoint, json=body)
            assert response.status_code == 201

            # Duplicate user check (expecting 400 for duplicate)
            response = requests.post(auth_endpoint, json=body)
            if response.status_code == 400:
                # Handling the duplicate user scenario without failing the test
                print("Duplicate user creation attempted. Expected behavior.")
            else:
                # If status code is unexpected, consider it as a failure
                pytest.fail(f"Unexpected status code: {response.status_code}")

        except Exception as ex:
            pytest.fail(f"create user failed {ex}")

            
    def test_login(self):
        try:
            #input existing user info
            body = {
                "name": "precious2",
                "password": "12345"
            }
            auth_endpoint = self.base_url + 'api/users/login/'
            response = requests.post(auth_endpoint, json=body)
            assert response.status_code == 200
            body = response.json()
            assert "message" in body
            assert isinstance(body["message"], dict)
            assert isinstance(body["message"]["token"], str)

            # Set the token obtained during login as self.reset_Jwt
            

        except Exception as ex:
            print(response.json())
            pytest.fail(f"login failed {ex}")

    def test_get_reset_token(self):
        try:
            # Ensure self.reset_Jwt is set by calling the login method
            

            # Check if self.reset_Jwt is set properly
            token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNDQwMDA0LCJpYXQiOjE3MDA0MzY0MDQsImp0aSI6IjU3N2IzYmRlOTNiNDQ1M2M5YzgxOGJiMGQwNTNmNjk2IiwidXNlcl9pZCI6MywibmFtZSI6InByZWNpb3VzMiIsImlzX2FkbWluIjpmYWxzZX0.mxa0nmtjcSLUK_YNLMoFPeEEQ74pkv87hfNPFIHMVs0" #input existing token
            ############input esiting token

            body = {
                "name": "precious2"
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            auth_endpoint = self.base_url + 'api/users/generate-token/'
            response = requests.post(auth_endpoint, json=body, headers=headers)
            assert response.status_code == 200
            body = response.json()
            assert "message" in body
            assert isinstance(body["message"], str)
            self.reset_token = body["message"]

        except Exception as ex:
            pytest.fail(f"gen reset token failed {ex}")