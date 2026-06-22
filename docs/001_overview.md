# Overview

PixelFuse is a FastAPI service that converts images into a portable plain-text file and reverses the process.

**Embed flow:** Upload images → get a `.txt` file with base64-encoded image blocks.  
**Extract flow:** Upload that `.txt` file → get a `.zip` of the original images.

Supported formats: JPEG, PNG, HEIC.

## Text file format

```
Filename: my-export

Image 1 (photo.jpg):
<base64 data>

Image 2 (shot.png):
<base64 data>
```

Each block is separated by a blank line. The `Filename:` header line carries the export name.
