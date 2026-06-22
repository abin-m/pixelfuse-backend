import io

from httpx import AsyncClient
from PIL import Image


def _make_png() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), color="red").save(buf, format="PNG")
    return buf.getvalue()


async def test_convert_embed_returns_text(client: AsyncClient) -> None:
    response = await client.post(
        "/convert-embed/",
        files=[("files", ("test.png", _make_png(), "image/png"))],
        data={"output_file_name": "output"},
    )
    assert response.status_code == 200
    assert "Image 1 (test.png)" in response.text
    assert response.headers["content-disposition"] == (
        'attachment; filename="output.txt"'
    )


async def test_convert_embed_too_many_files(client: AsyncClient) -> None:
    files = [("files", (f"img{i}.png", _make_png(), "image/png")) for i in range(11)]
    response = await client.post(
        "/convert-embed/",
        files=files,
        data={"output_file_name": "output"},
    )
    assert response.status_code == 400
    assert "Maximum" in response.json()["detail"]
