from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO

app = FastAPI(
    title="LearnLoop AI Backend",
    description="PDF processing API for LearnLoop AI"
)

@app.get("/")
def home():
    return {
        "message": "LearnLoop AI Backend is running!",
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF must be smaller than 10 MB."
        )

    try:
        reader = PdfReader(BytesIO(content))

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            pages.append({
                "page": page_number,
                "text": text
            })

        return {
            "filename": file.filename,
            "total_pages": len(reader.pages),
            "pages": pages
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process this PDF."
        )
