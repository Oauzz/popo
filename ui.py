import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from templates.main_ui import Ui_MainWindow
from tasks import create_db, export_schema, import_schema, extract_scripts, extract_foreign_keys, determine_order
import logging

class DummyDbCreatorApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialize_ui()
        self.setup_logging()

    def initialize_ui(self):
        self.startButton.clicked.connect(self.start_process)
        self.progressBar.setValue(0)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.log_handler = QtHandler(self.logTextBox)
        logging.getLogger().addHandler(self.log_handler)

    def start_process(self):
        source_db_info = {
            "name": self.sourceDbNameInput.text(),
            "user": self.sourceDbUserInput.text(),
            "password": self.sourceDbPassInput.text(),
            "host": self.sourceDbHostInput.text(),
            "port": self.sourceDbPortInput.text(),
        }
        
        new_db_info = {
            "name": self.newDbNameInput.text(),
            "user": self.newDbUserInput.text(),
            "password": self.newDbPassInput.text(),
            "host": self.newDbHostInput.text(),
            "port": self.newDbPortInput.text(),
        }

        schema_file = f"{source_db_info['name']}_schema.sql"
        
        steps = [
            lambda: create_db.run(new_db_info),
            lambda: export_schema.run(source_db_info),
            lambda: self.extract_and_merge_scripts(schema_file),
            lambda: self.extract_foreign_keys(f"{source_db_info['name']}_schema_merged_schema.sql"),
            lambda: self.determine_table_order(f"{source_db_info['name']}_schema_merged_schema_foreign_keys.json"),
            lambda: import_schema.run(new_db_info, source_db_info['name']),
            # Add other steps here
        ]
        
        total_steps = len(steps)
        for i, step in enumerate(steps):
            step()
            self.progressBar.setValue(int((i + 1) / total_steps * 100))
            QApplication.processEvents()

    def extract_and_merge_scripts(self, schema_file):
        base_name = extract_scripts.run(schema_file)
        if base_name is None:
            logging.error("Failed to extract and merge scripts.")
        else:
            merged_schema_file = f"{base_name}_merged_schema.sql"
            logging.info(f"Merged CREATE TABLE statements written to {merged_schema_file}")

    def extract_foreign_keys(self, merged_schema_file):
        extract_foreign_keys.run(merged_schema_file)

    def determine_table_order(self, foreign_keys_file):
        determine_order.run(foreign_keys_file)

class QtHandler(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)

def run_ui():
    app = QApplication(sys.argv)
    main_window = DummyDbCreatorApp()
    main_window.show()
    sys.exit(app.exec_())
