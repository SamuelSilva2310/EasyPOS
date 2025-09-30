
from easypos.database import init_db
from easypos.app import EasyPOSApp

def main():
    init_db()
    app = EasyPOSApp()
    app.run()

if __name__ == "__main__":
    main()