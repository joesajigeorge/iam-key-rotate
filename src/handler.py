import os
import boto3

iam = boto3.client("iam")

def create_key(user_name):
    try:
        response = iam.create_access_key(
            UserName = user_name
        )
        return response

    except Exception:
        print("Couldn't create access key for %s.", user_name)
        raise

def list_key(user_name):
    try:
        response = iam.list_access_keys(
            UserName = user_name
        )
        return response

    except Exception:
        print("Couldn't list access keys for %s.", user_name)
        raise

def update_key(user_name, key_id):
    try:
        response = iam.update_access_key(
            UserName = user_name,
            AccessKeyId = key_id,
            Status= 'Inactive'
        )
        print("Updated access key %s for %s.", key_id, user_name)
    except Exception:
        print("Couldn't update key %s for %s", key_id, user_name)
        raise

def delete_key(user_name, key_id):
    try:
        response = iam.delete_access_key(
            UserName = user_name,
            AccessKeyId = key_id
        )
        print("Deleted access key %s for %s.", key_id, user_name)
    except Exception:
        print("Couldn't delete key %s for %s", key_id, user_name)
        raise

def lambda_handler(event, context):

    '''
    In AWS, you can have a maximum of two access keys per user. 
    Make sure that there is only one access key before executing this program.
    '''
    oldKey = ""

    username = os.environ['USERNAME']
    print("Username: " + username)

    # List the access keys and fetch the active one.
    listkeyResponse = list_key(username)
    for key in listkeyResponse["AccessKeyMetadata"]:
        if(key["Status"] == "Active"):
            oldKey = key["AccessKeyId"]
    print("Old Key: " + oldKey)

    # Create a new access key
    createKeyResponse = create_key(username)
    newKey = createKeyResponse["AccessKey"]["AccessKeyId"]
    print("New Access Key: " + newKey)
    print("New Secret Access Key: " + createKeyResponse["AccessKey"]["SecretAccessKey"])

    # Deactivate the old access key
    update_key(username, oldKey)

    # Delete the old access key
    delete_key(username, oldKey)
