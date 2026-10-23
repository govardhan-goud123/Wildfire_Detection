# Wildfire Detection AI (TensorFlow)

A clean TensorFlow/Keras version of the wildfire image-classification project. The old PyTorch scripts and `.pth` model have been removed.

## Project files

- `wildfire_detection_app.py` — Streamlit app for uploading and classifying an image.
- `train_model.py` — command-line training script.
- `model_utils.py` — model creation, dataset loading, training, and saving.
- `wildfire_dataset/` — provided training and testing images.
- `models/wildfire_detector.keras` — created after training.

## 1. Install Python packages

Open a terminal in this project folder and run:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Train the model

```bash
python train_model.py --epochs 5
```

The first run may need an internet connection to download the pretrained MobileNetV2 ImageNet weights. Training saves the model to `models/wildfire_detector.keras`.

You can change the number of epochs, for example `--epochs 10`.

## 3. Run the web app

```bash
streamlit run wildfire_detection_app.py
```

Use **Train / retrain model** in the sidebar if you have not trained a model yet. Then upload a JPG, JPEG, PNG, or WEBP image.

## Dataset structure

The app expects:

```text
wildfire_dataset/
├── Training and Validation/
│   ├── fire/
│   └── nofire/
└── Testing/
    ├── fire/
    └── nofire/
```

## Notes

- The class order is `fire`, then `nofire`.
- This is a binary image classifier, not a fire-location detector.
- Predictions can be wrong. Do not use the app as an emergency alert or as proof that an area is safe.
