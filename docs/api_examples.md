# Example API Requests and Responses

## Upload API

### Request

```text
POST /upload
```

```JSON
{
  "body": {
    "file_content": "<base64-encoded-content>",
    "file_name": "test-file.txt"
  }
}
```

### Response

```JSON
{
  "resultCode": 200,
  "resultString": "File accepted for procesing.",
  "documentId": "1234567890abcdef1234567890abcdef"
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
