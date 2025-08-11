import os
import json
import google.generativeai as genai
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Configure the Gemini API
# Make sure to set your GOOGLE_API_KEY as an environment variable
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    raise Exception("ERROR: GOOGLE_API_KEY environment variable not set.")


def optimize_with_gemini(resume_text: str, job_description: str) -> dict:
    """
    Uses the Gemini Pro API to optimize the resume and get a change summary.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert ATS (Applicant Tracking System) optimization specialist and a professional resume writer.
    Your task is to take a candidate's resume text and a target job description, then generate an optimized resume and a summary of the changes.

    **Candidate's Resume Text:**
    ---
    {resume_text}
    ---

    **Target Job Description:**
    ---
    {job_description}
    ---

    **Instructions:**
    1.  Thoroughly analyze the job description to identify the most critical keywords, skills, and qualifications (e.g., "Python," "React," "Data Analysis," "Team Leadership").
    2.  Compare the candidate's resume against these required qualifications and identify any gaps.
    3.  Rewrite and enhance the resume's content (especially the summary/objective and the work experience bullet points) to truthfully and naturally incorporate the identified keywords.
    4.  IMPORTANT: Do NOT invent skills or experience. Your goal is to rephrase and highlight the candidate's existing experience using the language of the job description.
    5.  Maintain a professional tone and a clean, readable format. The output should be a complete, well-structured resume text.
    6.  Provide a brief, bulleted list of the key changes you made and explain WHY you made them (e.g., "Added 'Agile Methodologies' to the skills section to match the job description's emphasis on Scrum.").

    **Output Format:**
    Return your response as a single, valid JSON object. Do not include any text, explanations, or markdown formatting outside of this JSON object.
    The JSON object must have exactly two keys: "optimized_resume_text" and "changes_summary".

    Example JSON structure:
    {{
      "optimized_resume_text": "John Doe\\nNew York, NY | (123) 456-7890 | john.doe@email.com\\n\\nSummary\\nA highly motivated software engineer... (full optimized resume text here)",
      "changes_summary": [
        "Rephrased the summary to include keywords like 'SaaS' and 'cloud computing' from the job description.",
        "Quantified achievements in the 'Software Engineer at TechCorp' role to demonstrate impact, e.g., 'improved API response time by 30%'.",
        "Added 'CI/CD' and 'Docker' to the skills section as they were explicitly mentioned as requirements."
      ]
    }}
    """
    # prompt = f"""
    #     You are an expert ATS (Applicant Tracking System) optimization specialist and a professional resume writer.
    #     Your task is to take a candidate's resume text and a target job description, then generate an optimized resume and a detailed analysis.
    #
    #     **Candidate's Resume Text:**
    #     ---
    #     {resume_text}
    #     ---
    #
    #     **Target Job Description:**
    #     ---
    #     {job_description}
    #     ---
    #
    #     **Instructions:**
    #     1.  Analyze the job description for critical keywords, skills, and qualifications.
    #     2.  Rewrite the resume to align with the job description, truthfully incorporating keywords.
    #     3.  Based on your analysis, calculate an "ATS Match Score" as a percentage (0-100) representing how well the *original* resume matched the job description.
    #     4.  Identify the most important keywords from the job description. List which ones were found in the original resume and which were missing.
    #     5.  Provide a single, highly actionable tip for the user.
    #     6.  Provide a bulleted list of the key changes you made.
    #
    #     **Output Format:**
    #     Return your response as a single, valid JSON object with the following exact structure. Do not include any text outside this JSON object.
    #
    #     {{
    #       "optimized_resume_text": "The full text of the newly optimized resume...",
    #       "changes_summary": [
    #         "A bullet point explaining the first significant change.",
    #         "And so on..."
    #       ],
    #       "analysis": {{
    #         "match_score": 85,
    #         "keywords_found": ["Python", "Data Analysis"],
    #         "keywords_missing": ["React", "Team Leadership", "Agile"],
    #         "actionable_tip": "Consider adding a brief project section to showcase your 'React' experience with a tangible example."
    #       }}
    #     }}
    #     """
    try:
        response = model.generate_content(prompt)
        # Clean up the response text to ensure it's valid JSON
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "")
        result = json.loads(cleaned_response_text)
        return result
    except Exception as e:
        print(f"Error during Gemini API call or JSON parsing: {e}")
        # Provide a fallback error response
        return {
            "optimized_resume_text": "Error: Could not generate the optimized resume. The AI model might be unavailable or an error occurred. Please try again later.",
            "changes_summary": [
                "An error occurred while communicating with the AI model. Please check the backend logs for more details."]
        }


def create_docx(text: str, filepath: str):
    """
    Creates a .docx file from the given text.
    """
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    doc.save(filepath)


def create_pdf(text: str, filepath: str):
    """
    Creates a .pdf file from the given text using reportlab.
    """
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Replace newlines with <br/> tags for paragraph breaks in reportlab
    paragraphs = [Paragraph(line, style) for line in text.split('\n')]

    doc.build(paragraphs)