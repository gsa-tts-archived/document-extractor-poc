$(document).ready(function() {
   
    const storedDocument = sessionStorage.getItem("verifiedData");

    if (!storedDocument) {
        console.error("No document found in storage.");
        return;
    }

    const updatedDocument = JSON.parse(storedDocument).updated_document;

    document.getElementById("preview-section-file-name").textContent = updatedDocument.original_filename.split("/").pop();

    populateCsvPreview(updatedDocument.extracted_data);
    
});

function populateCsvPreview(extractedData) {
    
    const tableContainer = document.createElement("table");
    tableContainer.classList.add("usa-table");
    
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    const th1 = document.createElement("th");
    th1.textContent = "Field";
    const th2 = document.createElement("th");
    th2.textContent = "Value";
    
    headerRow.appendChild(th1);
    headerRow.appendChild(th2);
    thead.appendChild(headerRow);
    tableContainer.appendChild(thead);

    const tbody = document.createElement("tbody");

    for (let key in extractedData) {
        if (extractedData.hasOwnProperty(key)) {
            console.log(extractedData[key])
            const row = document.createElement("tr");
            
            const fieldCell = document.createElement("td");
            fieldCell.textContent = key;

            const valueCell = document.createElement("td");
            valueCell.textContent = extractedData[key].value ? extractedData[key].value : "N/A";

            row.appendChild(fieldCell);
            row.appendChild(valueCell);
            tbody.appendChild(row);
        }
    }

    tableContainer.appendChild(tbody);
    document.getElementById("preview-section").appendChild(tableContainer);
}

function downloadCSV(documentData, originalFileName) {
    let csvContent = "data:text/csv;charset=utf-8,Field,Value\n";
    
    for (let key in documentData.extracted_data) {
        if (documentData.extracted_data.hasOwnProperty(key)) {
            const value = documentData.extracted_data[key].value ? documentData.extracted_data[key].value : "N/A";
            csvContent += `"${key}","${value}"\n`;
        }
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", originalFileName.replace(/\.[^/.]+$/, "") + ".csv");
    document.body.appendChild(link);
    link.click();
}

function downloadJSON(documentData, originalFileName) {
    const jsonContent = JSON.stringify(documentData, null, 2);
    const blob = new Blob([jsonContent], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = originalFileName.replace(/\.[^/.]+$/, "") + ".json";
    document.body.appendChild(link);
    link.click();
}



 