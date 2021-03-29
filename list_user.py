import boto3
import json
import datetime



def list_users_info(account_id, list_user_info):
    sts_client= boto3.Session().client("sts")
    # 切换role
    sts_response = sts_client.assume_role(
        RoleArn="arn:aws-cn:iam::" + account_id + ":role/tsp/Operations",
        RoleSessionName='TA_Role',
    )
    #获取iam client
    iam_client = boto3.client('iam',
                                aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                                aws_session_token=sts_response['Credentials']['SessionToken']
                                )


    users_response = iam_client.list_users(MaxItems=1000)
    user_response_all = users_response["Users"]
    
    for user_response in user_response_all:
        user = user_response["UserName"]
        try:
            users_login_profile_response = iam_client.get_login_profile(UserName=user)
            is_tec_user = 'no'
        except:
            is_tec_user = 'yes'
        if "PasswordLastUsed" in user_response.keys():
            never_password_login = 'no'
        else:
            never_password_login = 'yes'
        createdate = user_response["CreateDate"]
        #print(createdate)
        createDate = createdate.date().isoformat()
        user_policies_response = iam_client.list_attached_user_policies(UserName=user)
        lst_user_policy = iam_client.list_user_policies(UserName=user)
        user_policie_response_all = user_policies_response["AttachedPolicies"]
        policy = []
        if user_policie_response_all:
            for user_policie_response in user_policie_response_all:
                policy.append(user_policie_response["PolicyName"])
        if lst_user_policy["PolicyNames"]:
            policy.append(lst_user_policy["PolicyNames"])
        if policy:    
            policies = ','.join('%s' %id for id in policy)
        else:
            policices = ''    
        list_user_info.append([account_id, user, policies, is_tec_user, createDate])
    print(list_user_info)
    return list_user_info



if __name__ == '__main__':
    account_id = '123456789012'
    list_user_info = []
    list_user_info.append(['account_id', 'user', 'policy', 'is_tec_user', 'CreateDate'])
    list_users_info(account_id, list_user_info)
    #print(list_user_info)
