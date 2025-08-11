# AI Resume Optimiser & Generator

This is a full-stack web application that helps job seekers optimize their resumes for specific job descriptions using AI. It parses a user's resume, compares it against a target job description, and provides an ATS-optimized version along with a summary of the changes.

## Features

-   **Resume Upload**: Supports PDF and DOCX formats with a drag-and-drop interface.
-   **AI-Powered Optimization**: Uses the Gemini Pro API to analyze and rewrite resume content.
-   **Keyword Matching**: Identifies and incorporates relevant keywords from the job description.
-   **Instant Preview**: View the optimized resume directly in the browser.
-   **Download Options**: Download the final resume as a DOCX or PDF file.
-   **Change Summary**: Get a clear, bulleted list of what was changed and why.
-   **Responsive Design**: Clean, modern UI that works on both desktop and mobile devices.
-   **State Persistence**: Your job description text and results are saved in your local session.

## Tech Stack

-   **Frontend**: React, Vite, Tailwind CSS
-   **Backend**: Python, FastAPI
-   **AI Model**: Google Gemini Pro
-   **File Parsing**: `pdfplumber`, `python-docx`
-   **File Generation**: `python-docx`, `reportlab`

## Project Structure