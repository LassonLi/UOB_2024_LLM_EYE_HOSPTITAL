# Tesseract OCR

這是一個使用 Tesseract 進行光學字符識別（OCR）的 Python 套件。

## 安裝

### Step 1:
安裝tesseract：
https://github.com/tesseract-ocr/tesseract

(我用mac是用home brew裝的, "brew install tesseract")


### Step 2:
使用 pip 安裝 OCRPackage：

```bash
$ pip install tesseract_ocr-0.1.tar.gz
```

## 使用


```python
from my_tesseract import TesseractOCR

ocr = TesseractOCR('/path/to/tesseract')
result_string = ocr.perform_ocr('/path/to/image.jpg')
print(result_string)
```

（將 "/path/to/tesseract" 替換為tesseract executable in your PATH) --> 在我電腦裡的路徑是/opt/homebrew/Cellar/tesseract/5.4.1/bin/tesseract 給你參考
（將 "/path/to/image.jpg" 替換為圖片路徑）
