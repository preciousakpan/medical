import pytest
import requests

class TestCRUDAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = 'http://127.0.0.1:8000/'  # Replace with your API base URL
        self.create_user()
    
    def create_user(self):
        try:
            body = {
                "name": "precious252",
                "email": "p1954660@gmail.com",
                "password": "12345",
                "is_admin": True
            }
            auth_endpoint = self.base_url + 'api/users/create-user/'
            response = requests.post(auth_endpoint, json=body)
            assert response.status_code == 201
            #duplicate user check
            
            response = requests.post(auth_endpoint  ,json= body)
            assert response.status_code == 400  
        except Exception as ex:
            pytest.fail(f"create user failed {ex}")
    
    def test_duplicate_user(self):
        
    
        assert True  # Dummy test to check if tests are running
            
    

    # def get_token(self):
    #     try:
    #         auth_endpoint = self.base_url + '/api/token/'
    #         response = requests.post(auth_endpoint, json={'username': 'testuser', 'password': 'testpassword'})
    #         response.raise_for_status()
    #         return response.json().get('access')
    #     except RequestException as e:
    #         pytest.fail(f"Failed to get token: {e}")

    # def test_create_record(self):
    #     endpoint = self.base_url + '/api/endpoint/'
    #     headers = {'Authorization': f'Bearer {self.token}'}
    #     data = {'field1': 'value1', 'field2': 'value2'}  # Your data for creation
    #     try:
    #         response = requests.post(endpoint, json=data, headers=headers)
    #         assert response.status_code == 201
    #         # Add assertions to check if the object is created properly
    #     except RequestException as e:
    #         pytest.fail(f"Failed to create record: {e}")

    # # Similarly, write other test methods (test_retrieve_record, test_update_record, test_delete_record)