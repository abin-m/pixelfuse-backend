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


async def test_extract_filename_with_colon(client: AsyncClient) -> None:
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color="green").save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode()
    embed = f"Filename: test\n\nImage 1 (my:file.png):\n{encoded}".encode()

    response = await client.post(
        "/extract-images/",
        files=[("file", ("embed.txt", embed, "text/plain"))],
    )
    assert response.status_code == 200
    zf = zipfile.ZipFile(io.BytesIO(response.content))
    assert len(zf.namelist()) == 1


async def test_extract_non_utf8_returns_400(client: AsyncClient) -> None:
    response = await client.post(
        "/extract-images/",
        files=[("file", ("bad.txt", b"\xff\xfe binary garbage", "text/plain"))],
    )
    assert response.status_code == 400
    assert "UTF-8" in response.json()["detail"]


async def test_extract_rate_limit(rate_limited_client: AsyncClient) -> None:
    r1 = await rate_limited_client.post(
        "/extract-images/",
        files=[("file", ("embed.txt", _make_embed_text(), "text/plain"))],
    )
    assert r1.status_code == 200

    r2 = await rate_limited_client.post(
        "/extract-images/",
        files=[("file", ("embed.txt", _make_embed_text(), "text/plain"))],
    )
    assert r2.status_code == 429
