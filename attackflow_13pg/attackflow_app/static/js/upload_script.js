// Function to trigger the download of the content as a JSON file
function downloadAsJson() {
    // Prompt the user to enter a filename
    var filename = prompt("Enter the filename:", "myFile");
    if (filename === null) return;  // Exit if the user clicks cancel
    filename += ".json";  // Append the .json extension

    // Get the content from the <textarea>
    var content = document.getElementById("editable-area").value;

    // Create a Blob object from the content
    var blob = new Blob([content], { type: "application/json" });

    // Create a temporary URL for the Blob
    var url = URL.createObjectURL(blob);

    // Create a temporary <a> element to trigger the download
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Revoke the temporary URL
    URL.revokeObjectURL(url);
}
