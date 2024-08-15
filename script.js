// Utility function to show the modal and change background
function showModal() {
    const modal = document.getElementById('responseModal');
    const body = document.body;
    const mainContent = document.querySelector('main'); // Adjust selector if needed

    modal.style.display = 'flex';
    body.classList.add('body-background-change'); // Change background color
    body.classList.add('body-compress-left'); // Compress left side of the body
    modal.classList.add('response-modal-left'); // Reposition modal
    body.style.marginRight = '400px'; // Adjust body margin to make room for the modal
}

// Utility function to hide the modal and reset styles
function hideModal() {
    const modal = document.getElementById('responseModal');
    const body = document.body;
    const mainContent = document.querySelector('main'); // Adjust selector if needed

    modal.style.display = 'none';
    body.classList.remove('body-background-change'); // Reset background color
    body.classList.remove('body-compress-left'); // Reset left margin
    modal.classList.remove('response-modal-left'); // Reset modal position
    body.style.marginRight = '0'; // Reset body margin
}

// Utility function to handle file uploads
async function uploadFiles(event) {
    event.preventDefault();

    const pdfFilesInput = document.getElementById('pdfFiles');
    const files = pdfFilesInput.files;
    
    if (files.length === 0) {
        alert('Please select files to upload.');
        return;
    }

    const formData = new FormData();
    Array.from(files).forEach(file => formData.append('pdf_files', file));

    try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();

        alert(result.message || result.error || 'Upload completed.');
    } catch (error) {
        console.error('Error uploading files:', error);
        alert('Failed to upload files. Please try again.');
    }
}

// Utility function to handle document queries
async function submitQuery(event) {
    event.preventDefault();

    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ question }),
        });
        const result = await response.json();

        const responseText = result.answer || result.error || 'No response received.';
        document.getElementById('responseText').textContent = responseText;
        showModal(); // Show the modal with the response
    } catch (error) {
        console.error('Error querying document:', error);
        alert('Failed to query document. Please try again.');
    }
}

// Utility function to download the response as a PDF
function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const responseText = document.getElementById('responseText').textContent;

    doc.text('Response:', 10, 10);
    doc.text(responseText, 10, 20);
    doc.save('response.pdf');
}

// Event listeners for form submissions
document.getElementById('uploadForm').addEventListener('submit', uploadFiles);
document.getElementById('queryForm').addEventListener('submit', submitQuery);

// Event listener to close the modal
document.getElementById('closeModal').addEventListener('click', hideModal);

// Close modal when clicking outside the modal content
window.addEventListener('click', (event) => {
    const modal = document.getElementById('responseModal');
    if (event.target === modal) {
        hideModal();
    }
});

// Add a button to download the response as a PDF
const downloadButton = document.createElement('button');
downloadButton.textContent = 'Download as PDF';
downloadButton.style.marginTop = '20px';
downloadButton.addEventListener('click', downloadPDF);
document.getElementById('responseContent').appendChild(downloadButton);
