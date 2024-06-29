# AWS OCR

AWS_OCR 是一個 Python 套件，用於從圖像中檢測文字，使用 Amazon Textract 服務。

## 安裝

使用 pip 安裝 AWS_OCR：

```bash
$ pip install AWS_OCR-0.1.tar.gz
```

## 使用

### Step 1:

1. Download "AWS CLI" (AWS SDKs不用下載)
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

2. Create "access key" & Download .csv file
https://docs.aws.amazon.com/textract/latest/dg/setup-awscli-sdk.html
(按照 ”第二點“ 操作)

3. Set "credentials" in the AWS credentials profile file on your local system
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
(在terminal 用指令 aws configure 去設定)


### Step 2:

```python
from my_aws_ocr import AWSTextDetector

aws_text_detector = AWSTextDetector()
response = aws_text_detector.detect_file_text(document_file_name="/path/to/image.jpg")
print(response)
```

（將 "/path/to/image.jpg" 替換為圖片路徑）
