import unittest
from unittest.mock import patch
from app import app, log

class Test(unittest.TestCase):

    def test_get_page(self):
        response = app.test_client().get('/')
        self.assertIn("<pre>Animals:", response.text)
        assert response.status_code == 200
    
    @patch('app.add_animal')
    def test_add_animal(self, mock_add_animal):
        mock_add_animal.post.side_effect = log.append(f"Mocking add_animal function")
        payload = {
            "name":  "luka",
            "animal": "dog",
            "add_animal": "Add Animals"}
        response = app.test_client().post('/', data=payload)
        self.assertIn("Mocking add_animal function", response.text)
        assert response.status_code == 200

    @patch('app.get_animals')
    def test_get_animals(self, mock_get_animals):
        mock_get_animals.post.side_effect = log.append(f"Mocking get_animals function")
        payload = {
            "get_animals": "Get Animals"}
        response = app.test_client().post('/', data=payload)
        self.assertIn("Mocking get_animals function", response.text)
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()