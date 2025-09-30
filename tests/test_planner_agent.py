import unittest
from unittest.mock import patch, Mock
import os

# Import your function (update with actual module path!)
from your_module import generate_plan  


class TestGeneratePlan(unittest.TestCase):

    @patch('requests.post')
    def test_generate_plan_success(self, mock_post):
        # Arrange
        user_prompt = "Test user prompt"
        temperature = 0.3
        model = "llama3-70b-8192"

        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': "Plan content"}}]
        }
        mock_post.return_value = mock_response

        # Act
        plan = generate_plan(user_prompt, temperature, model)

        # Assert
        self.assertEqual(plan, "Plan content")

    @patch('requests.post')
    def test_generate_plan_failure(self, mock_post):
        # Arrange
        user_prompt = "Test user prompt"
        temperature = 0.3
        model = "llama3-70b-8192"

        mock_response = Mock()
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        # Act
        plan = generate_plan(user_prompt, temperature, model)

        # Assert
        self.assertIsNone(plan)

    @patch('requests.post')
    def test_generate_plan_with_error(self, mock_post):
        # Arrange
        user_prompt = "Test user prompt"
        temperature = 0.3
        model = "llama3-8b-8192"

        mock_response = Mock()
        mock_response.json.side_effect = Exception("Mocked Exception")
        mock_post.return_value = mock_response

        # Act
        plan = generate_plan(user_prompt, temperature, model)

        # Assert
        self.assertIsNone(plan)

    def test_generate_plan_without_groq_api_key(self):
        # Arrange
        user_prompt = "Test user prompt"
        temperature = 0.3
        model = "llama3-8b-8192"

        # Act + Assert
        with patch.dict(os.environ, {}, clear=True):  # clears env vars
            with self.assertRaises(KeyError):
                generate_plan(user_prompt, temperature, model)


if __name__ == '__main__':
    unittest.main()


