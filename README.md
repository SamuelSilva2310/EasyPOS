

## Runnign DEV

1. Poetry install

```
poetry install
```

2. Activate poetry env
```
eval $(poetry env activate)
```

3. Run app

```
python src/easypos/main.py 
```



## Creating a build

To create a build, make sure to use venv (poetry does not work)

1. Create venv

```
python3 -m venv venv
```

2. Activate venv
```
source venv/bin/activate
```

3. Build

```
pyinstaller EasyPOS.spec --clean --noconfirm
```



# 🧾 EasyPOS - Windows Setup Guide

## 1. Install the Printer Driver (libusbK via Zadig)

1. Download **Zadig** from [https://zadig.akeo.ie](https://zadig.akeo.ie)
2. Plug in your USB thermal printer.
3. Open **Zadig**.
4. Go to **Options → List All Devices**.
5. Select your printer from the list (e.g., “USB Printing Support”).
6. On the right side, choose **libusbK (v3.x.x.x)**.
7. Click **Replace Driver**.
8. Wait for installation to finish.
9. Open **Device Manager** → confirm the printer appears under **libusbK USB Devices**.

---

## 2. Create and Activate a Virtual Environment

```bash
cd path\to\EasyPOS
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Run the Application
```bash
cd src
python -m easypos.main
```

## 4. Test printer
```bash
python src/easypos/test_printer.py
```

## Must Know


**During Development**
On WINDOWS the app files (db, logs, config) are located on a different directory

When using pyhton from Microsoft (installed via store, maybe some other cases)
```
C:\Users\<USERNAME>\AppData\Local\Packages\PythonSoftwareFoundation.....\LocalCache\Local\<YourAuthor>\EasyPOS
```