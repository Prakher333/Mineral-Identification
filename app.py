from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "static/runs/detect/train/weights/best.pt"
model = YOLO(MODEL_PATH)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the uploaded image directly into memory
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes))

        results = model(img)

        mineral = "Probably does not contain any of the 4 mentioned minerals"

        if results and results[0].boxes:
            index = int(results[0].boxes[0].cls.item())
            if index == 0:
                mineral = "Biotite"
            elif index == 2:
                mineral = "Chrysocolla"
            elif index == 4:
                mineral = "Pyrite"
            elif index == 5:
                mineral = "Quartz"

        return {"mineral": mineral}

    except Exception as e:
        return {"error": str(e)}

# Run FastAPI server:
# uvicorn app:app --host 127.0.0.1 --port 8000 --reload
