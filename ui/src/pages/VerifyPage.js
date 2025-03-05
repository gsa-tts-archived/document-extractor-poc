
import { useState, useEffect } from "react";
import Layout from "../components/Layout";

export default function VerifyPage() {
  const [documentId] = useState(() => sessionStorage.getItem("documentId"))
  const [responseData, setResponseData] = useState(null) // API response
  const [loading, setLoading] = useState(true) // tracks if page is loading

  async function pollApiRequest(attempts = 30, delay = 2000) {
    if (!documentId) {
      console.error("No document Id found")
      setLoading(false)
    }

    for (let i = 0; i < attempts; i++) {
      try {
        const response = await fetch(`/api/document/${documentId}`, {
          method: "GET",
          mode: "cors",
          headers: {
            Accept: "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();  // parse response

          setResponseData(result) // store API data in state
          setLoading(false) // stop loading when data is received
          return;
        } else {
          console.warn(`Attempt ${i + 1} failed: ${response.statusText}`);
        }
      } catch (error) {
        console.error(`Attempt ${i + 1} failed:`, error);
      }

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
    console.error('Attempt failed after max attempts')
    setLoading(false)
  }

  async function handleVerifySubmit(event) {
    event.preventDefault();

    if (!responseData || !responseData.extracted_data) {
      console.log("no extracted data available")
    }
    const formData = {
      extracted_data: responseData.extracted_data,
    };

    try {
      const apiUrl = `/api/document/${responseData.document_id}`;
      const response = await fetch(apiUrl, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        sessionStorage.setItem("verifiedData", JSON.stringify(result));
        window.location.href = `download-document`;
        //TODO remove alert
        alert("Data saved successfully!");
      } else {
        //TODO remove alert
        alert("Failed to save data: " + result.error);
      }
    } catch (error) {
      console.error("Error submitting data:", error);
      //TODO remove alert
      alert("An error occurred while saving.");
    }
  }

  useEffect(() => {
    if (!documentId) {
      console.error("No documentId found in sessionStorage")
      return
    }
    pollApiRequest()
  }, []) // runs only once when the component mounts

  function displayFileName() {
    const fileName = responseData?.document_key ? responseData?.document_key.replace("input/", "")
      : " ";
    return fileName
  }

  function handleInputChange(event, key, field) {
    setResponseData((prevData) => ({
      ...prevData,// keep previous data
      extracted_data: {
        ...prevData.extracted_data, // keep other fields the same
        [key]: { ...field, value: event.target.value },
      }
    }))
  }

  function displayExtractedData() {
    if (!responseData?.extracted_data) {
      console.warn("No extracted data found.");
      return;
    }
    return Object.entries(responseData.extracted_data)?.map(([key, field]) => {
      return (
        <div key={key}>
          <label className="usa-label" htmlFor="input-type-text">
            {key} <span className="text-accent-cool-darker display-inline-block width-full padding-top-2px">
              {field.confidence ? `(Confidence ${field?.confidence.toFixed(2)})` : "N/A"}
            </span>
          </label>
          <input className="usa-input" id="input-type-text" name="input-type-text" value={field.value || ""} onChange={((event) => handleInputChange(event, key, field))} /></div>
      )
    })
  }

  function displayFilePreview() {
    if (!responseData || !responseData.base64_encoded_file) return null;

    // get file extension
    const fileExtension = responseData.document_key.split(".").pop().toLowerCase();
    const mimeType = fileExtension === "pdf" ? "application/pdf" : `image/${fileExtension}`;
    // Base64 URL to display image
    const base64Src = `data:${mimeType};base64,${responseData.base64_encoded_file}`;

    return (
      <div id="file-display-container">
        {fileExtension === "pdf" ? (
          <iframe src={base64Src} width="100%" height="600px" title="Document Preview"></iframe>
        ) : (
          <img src={base64Src} alt="Uploaded Document" style={{ maxWidth: "100%", height: "auto" }} />
        )}
      </div>
    );
  }

  return (
    <Layout>
      {/* Start step indicator section  */}
      <div className="grid-container">
        <div className="usa-step-indicator usa-step-indicator--counters margin-y-2">
          <ol className="usa-step-indicator__segments">
            <li
              className="usa-step-indicator__segment usa-step-indicator__segment--complete"
            >
              <span className="usa-step-indicator__segment-label"
              >Upload documents <span className="usa-sr-only">completed</span></span
              >
            </li>
            <li
              className="usa-step-indicator__segment usa-step-indicator__segment--current"
            >
              <span className="usa-step-indicator__segment-label"
              >Verify documents and data
                <span className="usa-sr-only">not completed</span></span
              >
            </li>
            <li className="usa-step-indicator__segment">
              <span className="usa-step-indicator__segment-label"
              >Save and download CSV file
                <span className="usa-sr-only">not completed</span></span
              >
            </li>
          </ol>
        </div>
      </div>
      {/* End step indicator section  */}
      <div className="border-top-2px border-base-lighter">
        <div className="grid-container">
          <div className="grid-row">
            <div className="grid-col-12 tablet:grid-col-8">
              {/* Start card section  */}
              <ul className="usa-card-group">
                <li className="usa-card width-full">
                  <div className="usa-card__container file-preview-col">
                    <div className="usa-card__body">
                      <div id="file-display-container"></div>
                      {loading ? (<p>Processing...Please wait</p>) : ""}
                      <div>{displayFilePreview()}</div>
                      <p>{displayFileName()}</p>
                    </div>
                  </div>
                </li>
              </ul>
              {/* End card section  */}
            </div>
            <div
              className="grid-col-12 maxh-viewport border-bottom-2px border-base-lighter tablet:grid-col-4 tablet:border-left-2px tablet:border-base-lighter tablet:border-bottom-0"
            >{/* Start verify form section  */}
              <form id="verify-form" onSubmit={handleVerifySubmit}>
                <ul className="usa-card-group">
                  <li className="usa-card width-full">
                    <div className="usa-card__container verify-col">
                      <div
                        className="usa-card__body overflow-y-scroll minh-mobile-lg maxh-mobile-lg"
                      >
                        {displayExtractedData()}
                      </div>
                      <div
                        className="usa-card__footer border-top-1px border-base-lighter"
                      >
                        <button
                          id="verify-button"
                          className="usa-button"
                          type="submit"
                        >
                          Data verified
                        </button>

                      </div>
                    </div>
                  </li>
                </ul>
              </form>
              {/* End verify form section  */}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}