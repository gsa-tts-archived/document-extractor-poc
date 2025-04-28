from src.external.aws.iam import Iam


def test_generate_role_policy_with_allow_works():
    principle = "user"
    effect = "allow"
    arn = "mytestarn/testing/*"

    role = Iam._generate_role_policy(principle, effect, arn)
    assert role is not None
    assert isinstance(role, dict)
    assert isinstance(role["policyDocument"]["Statement"], list)
    assert role["policyDocument"]["Statement"][0]["Action"] == "execute-api:Invoke"
    assert role["policyDocument"]["Statement"][0]["Effect"] == "allow"
    assert role["policyDocument"]["Statement"][0]["Resource"] == "mytestarn/*"
