import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from siparisler import *
import pandas as pd
import sqlite3

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()


def select_excel_file():
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Excel Dosyası Seç", "", "Excel Dosyaları (*.xlsx *.xls)"
    )
    if file_path:
        import_excel_to_database(file_path)
    else:
        print("Dosya seçilmedi veya iptal edildi.")


def import_excel_to_database(file_path):
    print(file_path)
    if not file_path:
        print("Dosya yolu geçerli değil.")
        return
    try:
        df = pd.read_excel(file_path)
        con = sqlite3.connect("orders.db")
        df.to_sql("orders", con, if_exists="replace", index=False)
        con.close()
        print("Excel verisi başarıyla SQLite veritabanına aktarıldı.")
        display_data_in_table(df)
    except Exception as e:
        print("Hata:", e)


def display_data_in_table(df):
    ui.tableWidget.setRowCount(df.shape[0])
    ui.tableWidget.setColumnCount(df.shape[1])
    ui.tableWidget.setHorizontalHeaderLabels(df.columns)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
                if pd.isna(df.iloc[i, j]):
                    value = "NULL"
                    item = QTableWidgetItem(value.upper())
                    item.setBackground(QColor(200, 200, 200))  # Gri arka plan
                    ui.tableWidget.setItem(i, j, item)
                else:
                    value = str(df.iloc[i, j])
                    item = QTableWidgetItem(value.upper())  # Değeri büyük harflerle yaz
                    ui.tableWidget.setItem(i, j, item)

#ui.pushButton.clicked.connect(select_excel_file)


sys.exit(app.exec_())
