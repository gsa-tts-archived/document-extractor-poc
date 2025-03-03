[![MegaLinter](https://github.com/flexion/document-extractor-poc/actions/workflows/megalinter.yml/badge.svg)](https://github.com/flexion/document-extractor-poc/actions/workflows/megalinter.yml)
<!--
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/flexion/document-extractor-poc/badge)](https://scorecard.dev/viewer/?uri=github.com/flexion/document-extractor-poc)
-->

# Document Extractor Proof of Concept

![document_uploader_poc drawio](docs/document_uploader_poc.drawio.png)

[source](https://drive.google.com/file/d/1Ev9UzL8j8pEjpyM0r93MwGahs8yXCajJ/view?usp=drive_link) in [Draw.io](https://draw.io/)


## Testing `uploadFileForTextExtractor` in AWS Console

1. **Open AWS Lambda** → Select **`uploadFileForTextExtractor`**.
2. **Go to Test Tab** → Click **Create new test event**.
3. **Enter Event Name** → Use `"TestUploadFile"`.
4. **Paste JSON Payload**:

   ```
   {
     "body": "{\"file_content\": \"<base64-encoded-content>\", \"file_name\": \"test-file.txt\"}"
   }
   ```
5. Save & Run Test → Click Test