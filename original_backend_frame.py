import boto3
import json
import logging
import timestamp
from botocore.exceptions import ClientError
from pprint import pprint
from decimal import Decimal

def create_collection(collection_id, region):
    client = boto3.client('rekognition', region_name=region)

    # Check if collection already exists
    try:
        client.describe_collection(CollectionId=collection_id)
        print(f'Collection {collection_id} already exists')
    except client.exceptions.ResourceNotFoundException:
        # Create a collection if it doesn't exist
        print('Creating collection:' + collection_id)
        response = client.create_collection(CollectionId=collection_id,
        Tags={"SampleKey1":"SampleValue1"})
        print('Collection ARN: ' + response['CollectionArn'])
        print('Status code: ' + str(response['StatusCode']))
        print('Done...')


def detect_faces(target_file, region):
    client=boto3.client('rekognition', region_name=region)

    imageTarget = open(target_file, 'rb')

    response = client.detect_faces(Image={'Bytes': imageTarget.read()},
    Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))

        # Access predictions for individual face details and print them
        print("Gender: " + str(faceDetail['Gender']))
        print("Smile: " + str(faceDetail['Smile']))
        print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
        print("Emotions: " + str(faceDetail['Emotions'][0]))

    return len(response['FaceDetails'])


def compare_faces(bucket, sourceFile, targetFile, region):
    client = boto3.client('rekognition', region_name=region)

    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=99,
                                    SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile}},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) +
              ' matches with ' + similarity + '% confidence')

    imageTarget.close()
    return len(response['FaceMatches'])


def add_faces_to_collection(target_file, photo, collection_id, region):
    client = boto3.client('rekognition', region_name=region)

    imageTarget = open(target_file, 'rb')

    response = client.index_faces(CollectionId=collection_id,
                                  Image={'Bytes': imageTarget.read()},
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])
    print(response)

    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
        print('  Image ID: {}'.format(faceRecord['Face']['ImageId']))
        print('  External Image ID: {}'.format(faceRecord['Face']['ExternalImageId']))
        print('  Confidence: {}'.format(faceRecord['Face']['Confidence']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])


# Create DynamoDB database with image URL and face data, face ID
def create_dynamodb_table(table_name, region):
    dynamodb = boto3.client("dynamodb", region_name=region)

    try:
        table_description = dynamodb.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists. Returning its description.")
        return table_description
    except dynamodb.exceptions.ResourceNotFoundException:
        # if table doesn't exist, create a table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{
                'AttributeName': 'FaceID', 'KeyType': 'HASH'  # Partition key
            }, ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'FaceID', 'AttributeType': 'S'
                }, ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10
            }
        )
        print(table)
        return table




# 1. create collection
collection_id = 'facial_collection'
region = "ap-southeast-1"
create_collection(collection_id, region)

# 2. detect faces in target image
photo = 'target_image.jpg'
face_count=detect_faces(photo, region)
print("Faces detected: " + str(face_count))

if face_count == 1:
    print("Image suitable for use in collection.")
else:
    print("Please submit an image with only one face.")


# 3. compare faces in source image and target image
bucket = 'oneteambucket'
source_file = 'id_image.jpg'
target_file = 'target_image.jpg'

face_matches = compare_faces(bucket, source_file, target_file, region)
print("Face matches: " + str(face_matches))

if str(face_matches) == "1":
    print("Face match found.")
else:
    print("No face match found.")


# 4. Search for faces in collection
collectionId = 'facial_collection'
threshold = 99
maxFaces = 1
client = boto3.client('rekognition', region_name=region)
# input image should be local file here, not s3 file
with open(photo, 'rb') as image:
    response = client.search_faces_by_image(CollectionId=collectionId,
    Image={'Bytes': image.read()},
    FaceMatchThreshold=threshold, MaxFaces=maxFaces)

faceMatches = response['FaceMatches']
print(faceMatches)

for match in faceMatches:
    print('FaceId:' + match['Face']['FaceId'])
    print('ImageId:' + match['Face']['ImageId'])
    print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    print('Confidence: ' + str(match['Face']['Confidence']))

# Index faces
image = 'id_image.jpg'
photo_name = 'id_image'

indexed_faces_count = add_faces_to_collection(image, photo_name, collection_id, region)
print("Faces indexed count: " + str(indexed_faces_count))


# 5. add faces to collection
# store local file in S3 bucket
file_name = "id_image.jpg"
key_name = f"facial_images/{timestamp}_id_image.jpg"
s3 = boto3.client('s3', region_name=region)
# Upload the file
try:
    response = s3.upload_file(file_name, bucket, key_name)
    print("File upload successful!")
except ClientError as e:
    logging.error(e)


# 6. create DynamoDB table
database_name = 'facial_database'
dynamodb_table = create_dynamodb_table(database_name, region)
print("Table status:", dynamodb_table)




# The local file that was stored in S3 bucket
file_name = "id_image.jpg"

# Get URL of file
file_url = "https://s3.amazonaws.com/{}/{}".format(bucket, key_name)
print(file_url)

# upload face-id, face info, and image url
def AddDBEntry(file_name, file_url, face_id, image_id, confidence):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table('facial_database')
    response = table.put_item(
       Item={
            'ExternalImageID': file_name,
            'ImageURL': file_url,
            'FaceID': face_id,
            'ImageID': image_id,
            'Confidence': json.loads(json.dumps(confidence), parse_float=Decimal)
       }
    )
    return response

# Mock values for face ID, image ID, and confidence - replace them with actual values from your collection results
face_id = "response['FaceRecords'][0]['Face']['FaceId']"
image_id = "response['FaceRecords'][0]['Face']['ImageId']"
confidence = "response['FaceRecords'][0]['Face']['Confidence']"
dynamodb_resp = AddDBEntry(file_name, file_url, face_id, image_id, confidence)
print("Database entry successful.")
pprint(dynamodb_resp, sort_dicts=False)


# Existing User Login

# Call the DetectFaces Operation
photo = 'id_image.jpg'
face_count=detect_faces(photo, region)
print("Faces detected: " + str(face_count))

if face_count == 1:
    print("Image suitable for use in collection.")
else:
    print("Please submit an image with only one face.")


# Call the SearchFacesByImage Operation
fileName = 'id_image.jpg'
threshold = 70
maxFaces = 1
client = boto3.client('rekognition', region_name=region)

# input image should be local file here, not s3 file
with open(fileName, 'rb') as image:
    response = client.search_faces_by_image(CollectionId=collectionId,
    Image={'Bytes': image.read()},
    FaceMatchThreshold=threshold, MaxFaces=maxFaces)


# Check for the Returned FaceID and Confidence Level
faceMatches = response['FaceMatches']
print(faceMatches)

for match in faceMatches:
    print('FaceId:' + match['Face']['FaceId'])
    print('ImageId:' + match['Face']['ImageId'])
    print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    print('Confidence: ' + str(match['Face']['Confidence']))