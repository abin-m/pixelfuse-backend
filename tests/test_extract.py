import base64
import io
import zipfile

from httpx import AsyncClient
from PIL import Image


def _make_embed_text(filename: str = "test.png") -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode()
    return f"Filename: test\n\nImage 1 ({filename}):\n{encoded}".encode()


async def test_extract_images_returns_zip(client: AsyncClient) -> None:
    response = await client.post(
        "/extract-images/",
        files=[("file", ("embed.txt", _make_embed_text(), "text/plain"))],
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    zf = zipfile.ZipFile(io.BytesIO(response.content))
    assert len(zf.namelist()) == 1


async def test_extract_no_images_returns_400(client: AsyncClient) -> None:
    response = await client.post(
        "/extract-images/",
        files=[("file", ("empty.txt", b"no images here", "text/plain"))],
    )
    assert response.status_code == 400
    assert "No images found" in response.json()["detail"]
