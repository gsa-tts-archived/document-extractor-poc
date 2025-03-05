# Example API Requests and Responses

## Upload API

### Request

```http request
POST /api/document
```

```json
{
    "file_content": "<base64-encoded content of the uploaded file>",
    "file_name": "<name of the file>"
}
```

### Response

```json
{
    "message": "File uploaded successfully.",
    "documentId": "<random UUID>"
}
```

## Verify API

### Request

```text
POST /verify
```

```JSON
{
  "documentId": "1234567890abcdef1234567890abcdef"
}
```

### Response

```JSON
{
  "resultCode": 200,
  "resultString": "Extract finished.",
  "resultsData": {
    "foq": "bat"
  }
}
```

## Update API

### Request

```text
POST /update
```

```JSON
{
  "documentId": "1234567890abcdef1234567890abcdef",
  "updates": [
    {
      "oldField": "foq",
      "oldValue": "bat",
      "newField": "foo",
      "newValue": "bar"
    }
  ]
}
```

### Response

```JSON
{
  "documentId": "1234567890abcdef1234567890abcdef",
  "resultCode": 200,
  "resultString": "Update accepted.",
  "resultsData": {
    "foo": "bar"
  },
  "links": {
    "CSV": "https://url.of/data.csv",
    "JSON": "https://url.of/data.json"
  }
}
```
