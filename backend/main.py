import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.parser import parse_resume
from utils.optimizer import optimize_with_gemini, create_docx, create_pdf

# Create a directory for generated files if it doesn't exist
if not os.path.exists("generated"):
    os.makedirs("generated")

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # React default dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/optimize-resume/")
async def optimize_resume_endpoint(
        resume_file: UploadFile = File(...),
        job_description: str = Form(...)
):
    try:
        # 1. Parse the uploaded resume
        resume_contents = await resume_file.read()
        resume_text = parse_resume(resume_file.file, resume_file.filename)

        if not resume_text.strip():
            raise HTTPException(status_code=400,
                                detail="Could not extract text from the resume. Please ensure it's not an image-based file.")

        # 2. Call Gemini AI for optimization
        optimization_result = optimize_with_gemini(resume_text, job_description)

        if "Error" in optimization_result.get("optimized_resume_text", ""):
            raise HTTPException(status_code=500, detail="Failed to optimize resume due to an AI model error.")

        # 3. Generate DOCX and PDF files
        unique_id = uuid.uuid4()
        docx_filename = f"{unique_id}.docx"
        pdf_filename = f"{unique_id}.pdf"

        docx_filepath = os.path.join("generated", docx_filename)
        pdf_filepath = os.path.join("generated", pdf_filename)

        optimized_text = optimization_result["optimized_resume_text"]

        create_docx(optimized_text, docx_filepath)
        create_pdf(optimized_text, pdf_filepath)

        # 4. Return the result
        return JSONResponse(content={
            "optimized_resume_text": optimized_text,
            "changes_summary": optimization_result["changes_summary"],
            "download_links": {
                "docx": f"/api/download/docx/{docx_filename}",
                "pdf": f"/api/download/pdf/{pdf_filename}"
            }
        })
        # return JSONResponse(content={
        #     "optimized_resume_text": optimization_result["optimized_resume_text"],
        #     "changes_summary": optimization_result["changes_summary"],
        #     "analysis": optimization_result["analysis"],  # Add this line
        #     "download_links": {
        #         "docx": f"/api/download/docx/{docx_filename}",
        #         "pdf": f"/api/download/pdf/{pdf_filename}"
        #     }
        # })

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Generic error handler for unexpected issues
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred. Please try again later.")


@app.get("/api/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    filepath = os.path.join("generated", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")

    media_type = ""
    if file_type == "docx":
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif file_type == "pdf":
        media_type = "application/pdf"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    return FileResponse(path=filepath, media_type=media_type, filename=f"Optimized_Resume.{file_type}")