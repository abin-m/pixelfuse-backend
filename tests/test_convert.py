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
        "attachment; filename*=UTF-8''output.txt"
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


async def test_convert_embed_filename_special_chars(client: AsyncClient) -> None:
    response = await client.post(
        "/convert-embed/",
        files=[("files", ("test.png", _make_png(), "image/png"))],
        data={"output_file_name": 'report "final"'},
    )
    assert response.status_code == 200
    disposition = response.headers["content-disposition"]
    assert '"' not in disposition.split("filename*=UTF-8''")[1]


async def test_convert_embed_rate_limit(rate_limited_client: AsyncClient) -> None:
    r1 = await rate_limited_client.post(
        "/convert-embed/",
        files=[("files", ("test.png", _make_png(), "image/png"))],
        data={"output_file_name": "output"},
    )
    assert r1.status_code == 200

    r2 = await rate_limited_client.post(
        "/convert-embed/",
        files=[("files", ("test.png", _make_png(), "image/png"))],
        data={"output_file_name": "output"},
    )
    assert r2.status_code == 429
