import base64
import io
import urllib.parse
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image

from pixelfuse.config import get_settings

router = APIRouter()


@router.post("/convert-embed/")
async def convert_embed_images(
    files: Annotated[list[UploadFile], File()],
    output_file_name: Annotated[str, Form()],
) -> Response:
    settings = get_settings()
    if len(files) > settings.max_upload_files:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.max_upload_files} files allowed.",
        )

    blocks: list[str] = [f"Filename: {output_file_name}"]

    for idx, file in enumerate(files):
        content = await file.read()
        filename = file.filename or f"image_{idx + 1}"
        try:
            if filename.lower().endswith(".heic") or file.content_type == "image/heic":
                encoded = base64.b64encode(content).decode()
            else:
                Image.open(io.BytesIO(content)).verify()
                encoded = base64.b64encode(content).decode()
            blocks.append(f"Image {idx + 1} ({filename}):\n{encoded}")
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot process {filename}: {exc}",
            ) from exc

    return Response(
        content="\n\n".join(blocks),
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(output_file_name + '.txt', safe='')}"
        },
    )
