# Legal Document Analysis Tool

## Description

The Legal Document Analysis Tool is a web application designed for analyzing and querying PDF documents. It allows users to upload PDFs, ask questions about the content, and receive answers extracted from the uploaded documents. The application features a user-friendly interface with modals for displaying responses and options to download or copy responses to the clipboard.

## Features

- **Upload PDFs**: Upload multiple PDF files for analysis.
- **Query Documents**: Submit text-based questions and receive answers extracted from the uploaded PDFs.
- **Response Modal**: Display responses in a modal with a dynamic layout.
- **Download as PDF**: Download responses as PDF files.
- **Copy to Clipboard**: Copy response text to the clipboard for easy sharing.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS
  - JavaScript
  - [jsPDF](https://cdnjs.com/libraries/jspdf) for PDF generation

- **Backend**:
  - FastAPI for handling file uploads and document queries
  - PyPDF2 for PDF processing
  - langchain for text splitting and vector storage
  - Google Generative AI for embeddings and question answering

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend development)
- FastAPI, PyPDF2, langchain, and Google Generative AI libraries

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Bilal7855/Legal-Document-Analysis-Tool.git
