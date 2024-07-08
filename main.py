import logging
from ui import run_ui

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dummy DB Creator")
    
    run_ui()

if __name__ == "__main__":
    main()
