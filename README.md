

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



# Windows related
https://nyorikakar.medium.com/printing-with-python-and-epson-pos-printer-fbd17e127b6c
