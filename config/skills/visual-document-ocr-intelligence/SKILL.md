---
name: visual-document-ocr-intelligence
description: Document AI, optical character recognition (OCR), table extraction, and visual document understanding. Covers multi-engine OCR orchestration (Tesseract, PaddleOCR, Surya), document preprocessing (deskewing, adaptive Sauvola binarization, shadow flattening), and structured table/form key-value extraction.
---

# Visual Document AI & OCR Intelligence (`visual-document-ocr-intelligence`)

The `visual-document-ocr-intelligence` skill provides specialized computer vision algorithms for document restoration, high-accuracy text extraction, multi-column layout parsing, and structured table digitization.

---

## 1. Document Intelligence Architecture

```
+------------------------------------------------------------------------+
|                 Raw Scanned Document / Form / Invoice                  |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                     Document Restoration Pipeline                      |
|  - Radon / Hough Skew Angle Detection & Rotational Correction         |
|  - Local Adaptive Sauvola / Niblack Binarization                      |
|  - Illumination Gradient & Shadow Removal                             |
|  - Perspective Keystoning Rectification                               |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                        Layout Analysis & OCR                           |
|  - Multi-Column Text Flow & Reading Order Reconstruction               |
|  - Multi-Engine OCR Dispatch (Surya, PaddleOCR, Tesseract)             |
|  - Confidence Score Filtering & Language Dictionary Correction         |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                     Structured Information Mining                      |
|  - Table Grid & Borderless Cell Reconstruction (Markdown / JSON)       |
|  - Form Key-Value Pair Extraction & Entity Normalization               |
+------------------------------------------------------------------------+
```

---

## 2. Core Capabilities

### A. Document Preprocessing & Restoration
* **Deskewing**: Automatically estimates orientation skew angle via Radon transform or Hough line orientation and rotates images back to $0^\circ$.
* **Sauvola Binarization**: Handles degraded, yellowed, or non-uniformly lit pages where global Otsu fails.
* **Shadow Flattening**: Filters low-frequency background illumination gradients while preserving sharp text edges.

### B. Multi-Engine OCR Orchestration
* **Tesseract**: Fast, headless CLI text extraction across 100+ languages.
* **PaddleOCR / Surya OCR**: State-of-the-art transformer text recognition with high robustness against complex fonts, vertical text, and mathematical formulas.

### C. Structured Table & Form Extraction
* Identifies horizontal and vertical line intersections to reconstruct tabular data into clean Markdown tables or structured JSON payloads.

---

## 3. CLI Helper Tool (`document_ocr_pipeline.py`)

Located at `config/skills/visual-document-ocr-intelligence/scripts/document_ocr_pipeline.py`.

### Commands
```bash
# 1. Preprocess and deskew scanned document
python3 config/skills/visual-document-ocr-intelligence/scripts/document_ocr_pipeline.py \
  preprocess --image scan_crooked.jpg --output preprocessed.png

# 2. Run OCR text extraction
python3 config/skills/visual-document-ocr-intelligence/scripts/document_ocr_pipeline.py \
  ocr --image preprocessed.png --engine tesseract --lang eng --output text.txt

# 3. Extract structured table as Markdown or JSON
python3 config/skills/visual-document-ocr-intelligence/scripts/document_ocr_pipeline.py \
  extract-table --image invoice.png --format markdown --output table.md
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`industrial-machine-vision-inspection`**: Classical computer vision, camera calibration, precision metrology, and industrial inspection. Covers OpenCV p...
- **`computer-vision-deep-learning`**: Modern deep-learning computer vision engineering and high-performance inference pipelines. Covers neural objec...
- **`argon-multimodal-vision-grounding`**: Directs Gemini 4 Argon's native multimodal vision capabilities toward game screen telemetry, UI layout audits,...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
