# Warspear trade bot

## Requirements
* [Python 3.8.16](https://www.python.org/downloads/release/python-3816/)
* [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
* Windows OS

## Configuration
Put your tesseract path to main.py

Template for config.json in config directory:
```json
{
  "windows": [
    "Warspear Online"
  ],
  "messages": [
    ["msg1", 8],
    ["msg2", 10],
    ["msg3", 5]
  ],
  "trade": {
    "current_amount": 200,
    "price": 20,
    "mask": "item_mask",
    "delay": 0.001
  },
  "click": {
    "delay": 0.1,
    "step": 100,
    "hold": {
      "0": 0,
      "100": 4.36,
      "200": 6.13,
      "300": 7.35,
      "400": 8.49
    }
  },
  "timeout": 60
}
```

## Configure game
![img.png](readme/img.png)
![img_1.png](readme/img_1.png)
![img_2.png](readme/img_2.png)
![img_3.png](readme/img_3.png)
![img_4.png](readme/img_4.png)
![img_5.png](readme/img_5.png)
![img_6.png](readme/img_6.png)
![img_7.png](readme/img_7.png)
![img_8.png](readme/img_8.png)
![img_9.png](readme/img_9.png)
![img_10.png](readme/img_10.png)
![img_11.png](readme/img_11.png)
![img_12.png](readme/img_12.png)
![img_13.png](readme/img_13.png)
![img_14.png](readme/img_14.png)
![img_15.png](readme/img_15.png)
![img_16.png](readme/img_16.png)
![img_17.png](readme/img_17.png)
![img_18.png](readme/img_18.png)
![img_19.png](readme/img_19.png)
![img_20.png](readme/img_20.png)

## GAME SCREEN SIZE MUST BE MINIMUM AS POSSIBLE
![img_21.png](readme/img_21.png)
## Install & Run
```bash
pip install -r requirements.txt
python main.py
```