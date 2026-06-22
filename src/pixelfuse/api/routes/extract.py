import base64
import io
import zipfile

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

router = APIRouter()


@router.post("/extract-images/")
async def extract_images_from_text(file: UploadFile = File(...)) -> StreamingResponse:
    content = await file.read()
    blocks = content.decode("utf-8").split("\n\n")

    zip_buffer = io.BytesIO()
    count = 0

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, block in enumerate(blocks):
            if not block.startswith("Image"):
                continue
            try:
                header, encoded = block.split(":", 1)
                img_data = base64.b64decode(encoded.strip())

                if "heic" in header.lower():
                    zf.writestr(f"image_{idx + 1}.heic", img_data)
                else:
                    img = Image.open(io.BytesIO(img_data))
                    fmt = (img.format or "PNG").lower()
                    zf.writestr(f"image_{idx + 1}.{fmt}", img_data)

                count += 1
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error processing block {idx + 1}: {exc}",
                ) from exc

    if count == 0:
        raise HTTPException(status_code=400, detail="No images found in file.")

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="extracted_images.zip"'
        },
    )
