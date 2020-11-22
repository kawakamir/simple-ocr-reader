## setup(for MAC user)

install tesseract
```
brew install tesseract
```

install popper for converting pdf to image
```
brew install popper
```

install python libraries
```
poetry install
```

how to use (example)
```
python ocr_processor/processor.py --input=./samples/test_scan.jpg --output=sample.text  --verbose
```

