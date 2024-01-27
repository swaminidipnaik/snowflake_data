import boto3
import sys
sys.path.append('c://worspace//projects//bw-des-retail-analytics//utils')
from utils.vaultUtil import VaultClient
from utils.awsUtil import AWSConnector

class MainClass:
    def __init__(self, vault_url, role_id, secret_id, secret_path, region):
        self.VAULT_URL = vault_url
        self.ROLE_ID = role_id
        self.SECRET_ID = secret_id
        self.SECRET_PATH = secret_path
        self.region = region

    def run(self):
        try:
            vault_client = VaultClient(self.VAULT_URL, self.ROLE_ID, self.SECRET_ID, self.SECRET_PATH)
            token = vault_client.authenticate_with_approle()

            if token:
                secret_data = vault_client.get_secret(token)
                if secret_data:
                    print("Secret data:", secret_data)
                    self.process_aws(secret_data)
                else:
                    print("Failed to retrieve secret.")
            else:
                print("Failed to authenticate with AppRole.")
        except Exception as e:
            print(f"An error occurred during execution: {str(e)}")

    def process_aws(self, secret_data):
        try:
            aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
            aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']

            client = 'iam'
            aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, self.region)

            # Acces the IAM client through the instance
            iam_client = aws_connector.aws_client_conn

            # Now you can use iam_client to perform IAM operations
            response = iam_client.list_groups()

            print("IAM groups:", response)
        except Exception as e:
            print(f"An error occurred during AWS processing: {str(e)}")

if __name__ == "__main__":
    # Pass your values to the MainClass constructor
    main_instance = MainClass(
        vault_url="http://127.0.0.1:8200",
        role_id="40eab551-1752-d210-876c-200497d3abbb",
        secret_id="d5d175e6-d60b-a887-3cc1-f13358deb2de",
        secret_path="secret/data/aws",
        region='us-east-1'
    )
    
    main_instance.run()
