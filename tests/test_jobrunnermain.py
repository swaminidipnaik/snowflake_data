import pytest
import sys
from unittest.mock import patch, MagicMock
sys.path.append('c://worspace//projects//bw-des-retail-analytics//utils')
from utils import *

@pytest.fixture
def mock_vault_client():
    with patch('utils.VaultClient') as MockVaultClient:
        mock_instance = MockVaultClient.return_value
        mock_instance.authenticate_with_approle.return_value = 'mock_token'
        mock_instance.get_secret.return_value = {'data': {'bw-aws-accesskey-dev': 'access_key', 'bw-aws-secretkey-dev': 'secret_key'}}
        yield mock_instance

@pytest.fixture
def mock_aws_connector():
    with patch('utils.AWSConnector') as MockAWSConnector:
        mock_instance = MockAWSConnector.return_value
        mock_instance.aws_client_conn = MagicMock()
        yield mock_instance

# def test_run_method(mock_vault_client, mock_aws_connector):
#     main_instance = MainClass(
#         vault_url="http://127.0.0.1:8200",
#         role_id="40eab551-1752-d210-876c-200497d3abbb",
#         secret_id="d5d175e6-d60b-a887-3cc1-f13358deb2de",
#         secret_path="secret/data/aws",
#         region='us-east-1'
#     )

    # main_instance.run()

    mock_vault_client.authenticate_with_approle.assert_called_once()
    mock_vault_client.get_secret.assert_called_once_with('mock_token')
    mock_aws_connector.aws_client_conn.list_groups.assert_called_once()

# def test_process_aws_method(mock_vault_client, mock_aws_connector):
#     secret_data = {'data': {'bw-aws-accesskey-dev': 'access_key', 'bw-aws-secretkey-dev': 'secret_key'}}

#     main_instance = MainClass(
#         vault_url="http://127.0.0.1:8200",
#         role_id="40eab551-1752-d210-876c-200497d3abbb",
#         secret_id="d5d175e6-d60b-a887-3cc1-f13358deb2de",
#         secret_path="secret/data/aws",
#         region='us-east-1'
#     )

#     main_instance.process_aws(secret_data)

#     mock_aws_connector.aws_client_conn.list_groups.assert_called_once()

