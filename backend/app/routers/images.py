from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4

router = APIRouter(prefix ="/images", tags=["images"])

STORAGE_DIR = Path(__file__).resolve().parents[2] / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    image_id = uuid4().hex + ext
    dest = STORAGE_DIR / image_id

    content = await file.read()
    with dest.open("wb") as f:
        f.write(content)

    return {"image_id": image_id,
            "url": f"/images/{image_id}"
            }

@router.get("/{image_id}")
def get_image(image_id: str):
    path = STORAGE_DIR / image_id
    if not path.exists():
        raise HTTPException(status_code=404, detail="Image not found.")
    return FileResponse(path)