from src.login.user.role import Role


class Iam(Role):
    def get_role(self, principal_id, effect, resource) -> str:
        return self._generate_role_policy(principal_id, effect, resource)

    @staticmethod
    def _generate_role_policy(principal_id, effect, resource) -> dict[str:dict]:
        rest_api_arn = resource.split("/")[0]
        statement_one = {"Action": "execute-api:Invoke", "Effect": effect, "Resource": f"{rest_api_arn}/*"}
        policy_document = {"Version": "2012-10-17", "Statement": [statement_one]}
        auth_response = {"principalId": principal_id, "policyDocument": policy_document}

        return auth_response
