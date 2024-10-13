import base64
import zipfile
from fastapi import BackgroundTasks, FastAPI, File, Form, UploadFile, HTTPException
from typing import List
from PIL import Image
from fastapi.responses import FileResponse
import pyheif
import io
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pixelfuse-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to convert image to base64
def encode_image_to_base64(image: bytes):
    return base64.b64encode(image).decode('utf-8')

# Function to open HEIC image and convert it to a format supported by PIL
def open_heic_image(content: bytes):
    heif_file = pyheif.read_heif(content)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    return image

@app.post("/convert-embed/")
async def convert_embed_images(
    files: List[UploadFile] = File(...),
    output_file_name: str = Form(...)
):
    # Check if more than 10 files are uploaded
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="You can upload a maximum of 10 files.")
    
    # Prepare text content that will be written into the text file
    text_content = f"Filename: {output_file_name}\n\n"
    total_size = 0
    max_total_size = 5 * 1024 * 1024  # 5 MB limit

    for idx, file in enumerate(files):
        content = await file.read()  # Read the content of each uploaded file
        try:
            # Handle HEIC files separately
            if file.filename.lower().endswith(".heic") or file.content_type == "image/heic":
                image = open_heic_image(content)  # Open HEIC image
                img_format = "HEIC"
            else:
                image = Image.open(io.BytesIO(content))  # Open other image formats
                img_format = image.format

            # Encode the original image without quality reduction
            encoded_image = encode_image_to_base64(content)
            image_size = len(encoded_image.encode('utf-8'))

            # Check total size doesn't exceed 5MB
            if total_size + image_size > max_total_size:
                raise HTTPException(
                    status_code=400,
                    detail="Total size exceeds 5 MB limit. Try uploading fewer or smaller files."
                )

            total_size += image_size
            text_content += f"Image {idx + 1} ({file.filename}):\n{encoded_image}\n\n"

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cannot process image file: {file.filename}. Error: {str(e)}")

    # Write the base64-encoded content into a .txt file
    output_txt_file = f"./{output_file_name}.txt"
    with open(output_txt_file, "w") as text_file:
        text_file.write(text_content)

    return FileResponse(path=output_txt_file, media_type='text/plain', filename=f"{output_file_name}.txt")


@app.post("/extract-images/")
async def extract_images_from_text(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    decoded_images = content.decode('utf-8').split('\n\n')

    extracted_images = []
    output_dir = "extracted_images"
    
    # Create a directory to store the extracted images
    os.makedirs(output_dir, exist_ok=True)

    for idx, block in enumerate(decoded_images):
        if block.startswith("Image"):
            # Extract image info and base64 data
            try:
                header, encoded_img = block.split(":", 1)
                encoded_img = encoded_img.strip()
                img_data = base64.b64decode(encoded_img)
                
                # Open the image directly from the original format
                img = Image.open(io.BytesIO(img_data))
                img_format = img.format.lower() or "jpeg"  # Retain the original format
                
                output_image_path = os.path.join(output_dir, f"extracted_image_{idx + 1}.{img_format}")
                with open(output_image_path, 'wb') as f:
                    f.write(img_data)  # Save the image without modification
                
                extracted_images.append(output_image_path)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error processing image {idx + 1}: {str(e)}")

    # Create a ZIP file of the extracted images
    zip_filename = "extracted_images.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for img in extracted_images:
            zipf.write(img, os.path.basename(img))
    
    background_tasks.add_task(clean_up_files, output_dir)

    return FileResponse(zip_path, media_type='application/zip', filename=zip_filename)

# Clean up function to delete files after download
def clean_up_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(directory)  # Remove the directory after cleaning up
