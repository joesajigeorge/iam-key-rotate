import os
import boto3

iam = boto3.client("iam")

def lambda_handler(event, context):

    '''
    In AWS, you can have a maximum of two access keys per user. 
    '''

    username = os.environ['USERNAME']
    print("Username: " + username)

    try:
        if (event['state'] == "delete"):

            oldest_access_key_id = None
            oldest_access_key_create_date = None

            listResponse = iam.list_access_keys(UserName=username)

            # Iterate over the access keys
            for access_key in listResponse['AccessKeyMetadata']:
                create_date = access_key['CreateDate']

                # Check if this access key is older than the current oldest
                if oldest_access_key_create_date is None or create_date < oldest_access_key_create_date:
                    oldest_access_key_id = access_key['AccessKeyId']
                    oldest_access_key_create_date = create_date

            # Print the oldest access key
            print("Oldest access key: " + oldest_access_key_id)

            # Deactivate the old access key
            updateResponse = iam.update_access_key(
                UserName = username,
                AccessKeyId = oldest_access_key_id,
                Status= 'Inactive'
            )
            print("Deactivated access key %s for %s.", oldest_access_key_id, username)

            # Delete the old access key
            deleteResponse = iam.delete_access_key(
                UserName = username,
                AccessKeyId = oldest_access_key_id
            )
            print("Deleted access key %s for %s.", oldest_access_key_id, username)
        
        elif(event['state'] == "create"):

            # Create a new access key
            createResponse = iam.create_access_key(
                UserName = username
            )

            new_access_key_id = createResponse["AccessKey"]["AccessKeyId"]
            print("New Access Key: " + new_access_key_id)
            print("New Secret Access Key: " + createResponse["AccessKey"]["SecretAccessKey"])

            # We can email the keys to the persons or upload the keys as a file to cloud

    except Exception as e:
        print(e)
        print("Something failed")
