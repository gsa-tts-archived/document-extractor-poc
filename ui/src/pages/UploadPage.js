import { useState, useRef } from 'react';
import Layout from '../components/Layout';
import { authorizedFetch } from '../utils/auth';

export default function UploadPage() {
  // state for alert messages
  const [alertMessage, setAlertMessage] = useState(null);
  const [alertType, setAlertType] = useState(null);
  const fileInputRef = useRef(null);

  function showAlert(message, type) {
    setAlertMessage(message);
    setAlertType(type);
  }

  // handle form submission
  async function handleSubmit(event) {
    event.preventDefault();

    const file = fileInputRef.current?.files[0];

    console.log('file upload successful', file.name);

    if (!file) {
      showAlert('Please select a file to upload!', 'error');
      return;
    }

    // read file as Base64
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onload = async function () {
      const base64File = reader.result.split(',')[1];
      const requestBody = {
        file_content: base64File,
        file_name: file.name,
      };

      try {
        const apiUrl = '/api/document';
        const response = await authorizedFetch(apiUrl, {
          method: 'POST',
          body: JSON.stringify(requestBody),
        });

        const data = await response.json();
        console.log('request response', data, response);

        if (response.ok) {
          sessionStorage.setItem('documentId', data.documentId);
          showAlert('File uploaded successfully!', 'success, fake id', data.id);
          window.location.href = `verify-document`;
        } else {
          showAlert('File failed to upload!', 'error');
        }
      } catch (error) {
        console.error('Upload failed:', error);
        showAlert('An error occurred while uploading!', 'error');
      }
    };
  }

  return (
    <Layout>
      <div className="site-wrapper grid-container padding-bottom-15">
        {/* Start alert section */}
        {alertMessage && (
          <div
            className={`usa-alert usa-alert--${alertType} usa-alert--no-icon`}
          >
            <div className="usa-alert__body">
              <p className="usa-alert__text">{alertMessage}</p>
            </div>
          </div>
        )}
        {/* End alert section */}
        {/* Start step indicator section */}
        <div className="usa-step-indicator usa-step-indicator--counters margin-bottom-6">
          <ol className="usa-step-indicator__segments">
            <li className="usa-step-indicator__segment usa-step-indicator__segment--current">
              <span className="usa-step-indicator__segment-label">
                Upload documents <span className="usa-sr-only">completed</span>
              </span>
            </li>
            <li className="usa-step-indicator__segment">
              <span className="usa-step-indicator__segment-label">
                Verify documents and data{' '}
                <span className="usa-sr-only">not completed</span>
              </span>
            </li>
            <li className="usa-step-indicator__segment">
              <span className="usa-step-indicator__segment-label">
                Save and download CSV file{' '}
                <span className="usa-sr-only">not completed</span>
              </span>
            </li>
          </ol>
        </div>

        {/* End step indicator section */}
        <h1 className="font-ui-xl margin-bottom-2">Upload documents</h1>
        <form id="upload-form" onSubmit={handleSubmit}>
          {/* Start card section */}
          <ul className="usa-card-group">
            <li className="usa-card tablet:grid-col-6 widescreen:grid-col-4">
              <div className="usa-card__container">
                <div className="usa-card__header">
                  <h4 className="usa-card__heading font-body-md">
                    File upload
                  </h4>
                </div>
                <div className="usa-card__body">
                  {/* Start file input section */}
                  <div className="usa-form-group">
                    <span className="usa-hint" id="file-input-specific-hint">
                      Files must be under 10MB
                    </span>
                    <label
                      className="usa-label margin-top-1"
                      htmlFor="file-input-single"
                    >
                      Attach a JPG, PDF, TIFF, HEIC, or PNG file
                    </label>
                    <input
                      id="file-input-single"
                      className="usa-file-input"
                      type="file"
                      name="file-input-single"
                      accept=".jpg,.pdf,.tiff,.heic,.png"
                      ref={fileInputRef}
                    />
                  </div>
                  {/* End file input section */}
                </div>
              </div>
            </li>
          </ul>
          {/* End card section */}
          {/* Start button section */}
          <div className="display-flex flex-column flex-align-end tablet:grid-col-6">
            <button id="upload-button" className="usa-button" type="submit">
              Process data
            </button>
          </div>
          {/* End button section */}
        </form>
      </div>
    </Layout>
  );
}
