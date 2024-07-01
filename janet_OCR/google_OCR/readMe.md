# OCRPackage

OCRPackage 是一個使用 Google Cloud Vision API 進行文字檢測的 Python 包。

## 安裝

使用 pip 安裝 OCRPackage：

```bash
$ pip install ocrpackage-0.1.tar.gz
```

## 使用

### Step 1:

1. 把json檔放在root資料夾
2. 在main function寫

```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Janet_OCR_credential.json"
```


### Step 2:

```python
from my_ocr import OCRDetector

detector = OCRDetector()
text = detector.run_quickstart("/path/to/image.jpg")
print(text)
```

（將 "/path/to/image.jpg" 替換為圖片路徑）