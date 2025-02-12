import boto3
import json
import os

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
sqs_client = boto3.client('sqs')

SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']

# This lambda function is triggred by S3 event when files are uploaded to S3 and is responsible for writing the extracted json to SQS.
def lambda_handler(event, context):
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    document_key = record['s3']['object']['key']

    response = textract_client.analyze_document(
        Document={'S3Object': {'Bucket': bucket_name, 'Name': document_key}},
        FeatureTypes=['FORMS', 'TABLES']
    )
 
    extracted_data = parse_textract_response(response)

    # Send extracted data to SQS
    sqs_client.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({
            'document_key': document_key,
            'extracted_data': extracted_data
        })
    )

    return {'statusCode': 200, 'body': json.dumps('Message sent to SQS')}

def parse_textract_response(response):
    """ Extracts key-value pairs correctly from AWS Textract response. """
    key_map = {}  # Stores key text
    value_map = {}  # Stores value text
    block_map = {}  # Stores all blocks by ID

    # Iterate through each block
    for block in response.get('Blocks', []):
        block_id = block['Id']
        block_map[block_id] = block  # Store all blocks in a map

        # If it's a key, store in key_map
        if block['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in block and 'KEY' in block['EntityTypes']:
            key_map[block_id] = block

        # If it's a value, store in value_map
        if block['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in block and 'VALUE' in block['EntityTypes']:
            value_map[block_id] = block

    extracted_data = {}

    # Iterate over key_map and find the corresponding value
    for key_id, key_block in key_map.items():
        key_text = get_text_from_block(key_block, block_map)  # Extract key text
        value_text = None

        # Find the corresponding value by checking relationships
        for relationship in key_block.get('Relationships', []):
            if relationship['Type'] == 'VALUE':
                for value_id in relationship['Ids']:
                    value_block = value_map.get(value_id)
                    if value_block:
                        value_text = get_text_from_block(value_block, block_map)  # Extract value text

        if key_text and value_text:
            extracted_data[key_text] = value_text  # Store extracted key-value pair
    print(extracted_data)
    return extracted_data

def get_text_from_block(block, block_map):
    """ Extracts text from a block, handling word and line structures. """
    text = ''
    if 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word_block = block_map.get(child_id)
                    if word_block and 'Text' in word_block:
                        text += word_block['Text'] + ' '
    return text.strip() 
