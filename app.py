from fastapi import FastAPI, UploadFile, File, Request
from docling.document_converter import DocumentConverter
import os

app = FastAPI()
converter = DocumentConverter()

@app.api_route("/{full_path:path}", methods=["POST"])
async def docling_handler(request: Request):
    try:
        form = await request.form()

        file = None
        for key in ["file", "files", "document", "data"]:
            if key in form:
                file = form[key]
                break

        if not file:
            return {
                "document": {
                    "md_content": "ERROR: No file received"
                }
            }

        content = await file.read()

        if not content:
            return {
                "document": {
                    "md_content": "ERROR: Empty file"
                }
            }

        path = "temp.pdf"
        with open(path, "wb") as f:
            f.write(content)

        result = converter.convert(path)

        text = result.document.export_to_markdown()

        return {
            "document": {
                "md_content": text
            }
        }

    except Exception as e:
        return {
            "document": {
                "md_content": f"ERROR: {str(e)}"
            }
        }

    finally:
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")