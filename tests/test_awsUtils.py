import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.append("C:\\worspace\\projects\\bw-des-retail-analytics\\utils")

from utils.awsUtil import AWSConnector

@pytest.fixture
def mock_boto3_session():
    with patch('boto3.Session') as MockBoto3Session:
        mock_instance = MockBoto3Session.return_value
        yield mock_instance

def test_create_session(mock_boto3_session):
    aws_access_key = 'mock_access_key'
    aws_secret_key = 'mock_secret_key'
    region = 'us-east-1'

    aws_connector = AWSConnector(aws_access_key, aws_secret_key, region=region)

    mock_boto3_session.assert_called_once_with(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )

def test_create_aws_client(mock_boto3_session):
    aws_connector = AWSConnector('mock_access_key', 'mock_secret_key', client='s3', region='us-east-1')

    aws_connector.create_aws_client()

    mock_boto3_session.return_value.client.assert_called_once_with('s3')

def test_aws_connector_initialization(mock_boto3_session):
    aws_connector = AWSConnector('mock_access_key', 'mock_secret_key', client='s3', region='us-east-1')

    assert aws_connector.aws_access_key == 'mock_access_key'
    assert aws_connector.aws_secret_key == 'mock_secret_key'
    assert aws_connector.region == 'us-east-1'
    assert aws_connector.aws_client == 's3'
    assert isinstance(aws_connector.session, MagicMock)
    assert isinstance(aws_connector.aws_client_conn, MagicMock)
