from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox
)

from generic_utilities import GenericUtilities 
import shutil

class ExportPythonUtilities:

    @staticmethod
    def download_python(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)
        if fileName:
            try:
                                
                bin_file_path = GenericUtilities.get_recent_intensity_tracing_file()
                binFileName = f"{fileName}.bin"

                if bin_file_path:
                    shutil.copy(bin_file_path, binFileName)
                
                with open('plot_data_file.py', 'r') as file:
                    content = file.readlines()
                
                
                new_content = []
                skip_function = False
                for line in content:
                    if 'def get_recent_intensity_tracing_file()' in line:
                        skip_function = True
                    elif skip_function and line.startswith('times ='):
                        skip_function = False
                    if not skip_function:
                        if 'times =' in line:
                            line = line+ f"\nfile_path = '{binFileName}'\n"
                        new_content.append(line)
                
          
                with open(f"{fileName}.py", 'w') as file:
                    file.writelines(new_content)
                
                QMessageBox.information(self, "Save Successful", f"The file has been saved successfully: {fileName}")
            except Exception as e:
                QMessageBox.warning(self, "Save error", f"An error occurred while saving the file: {str(e)}")
    
              