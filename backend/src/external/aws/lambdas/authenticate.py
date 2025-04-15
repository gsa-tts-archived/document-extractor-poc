import boto3
import jwt

# SECRET_KEY = os.environ.get("JWT_SECRET", "super-duper-secrets-are-just-legend")

client = boto3.client("secretsmanager")
SECRET_KEY = client.get_secret_value(SecretId="JWT_SECRET")["SecretString"]


def lambda_handler(event, context):
    token = event["headers"].get("Authorization", "").replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"isAuthorized": True, "context": decoded}
    except Exception:
        return {"isAuthorized": False}


def verifyAccessToken(token: str):
    return "valid-token"
