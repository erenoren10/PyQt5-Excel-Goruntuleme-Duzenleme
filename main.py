import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from slugify import slugify
from siparisler import *
import pandas as pd
import sqlite3

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()


def create_orders_table():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
        barkod TEXT,
        paket_no TEXT,
        kargo_firmasi TEXT,
        siparis_tarihi TEXT,
        termin_suresinin_bittigi_tarih TEXT,
        kargoya_teslim_tarihi TEXT,
        kargo_kodu TEXT,
        siparis_numarasi TEXT,
        alici TEXT,
        teslimat_adresi TEXT,
        il TEXT,
        ilce TEXT,
        urun_adi TEXT,
        fatura_adresi TEXT,
        alici_fatura_adresi TEXT,
        siparis_statusu TEXT,
        e_posta TEXT,
        komisyon_orani TEXT,
        marka TEXT,
        stok_kodu TEXT,
        adet TEXT,
        birim_fiyati TEXT,
        satis_tutari TEXT,
        indirim_tutari TEXT,
        trendyol_indirim_tutari TEXT,
        faturalanacak_tutar TEXT,
        butik_numarasi TEXT,
        teslim_tarihi TEXT,
        kargodan_alinan_desi TEXT,
        hesapladigim_desi TEXT,
        faturalanan_kargo_tutari TEXT,
        alternatif_teslimat_statusu TEXT,
        kurumsal_faturali_siparis TEXT,
        vergi_kimlik_numarasi TEXT,
        vergi_dairesi TEXT,
        sirket_ismi TEXT,
        arkadaslarinla_al_siparisi TEXT,
        fatura TEXT,
        musteri_siparis_adedi TEXT,
        mikro_ihracat TEXT,
        etgb_no TEXT,
        etgb_tarihi TEXT,
        yas TEXT,
        cinsiyet TEXT,
        kargo_desi TEXT,
        urun_maliyeti TEXT
        )'''
    )
    conn.commit()
    conn.close()



def select_excel_file():
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Excel Dosyası Seç", "", "Excel Dosyaları (*.xlsx *.xls)"
    )
    if file_path:
        import_excel_to_database(file_path)
    else:
        ui.gosterStatus.setText("Dosya seçilmedi veya iptal edildi.")


def translate_column_name(column_name):
    translations = {
        'ç': 'c',
        'ğ': 'g',
        'ı': 'i',
        'ö': 'o',
        'ş': 's',
        'ü': 'u',
        '-': '_',
    }
    translated_name = ''.join(translations.get(c, c) for c in column_name)
    return translated_name

def import_excel_to_database(file_path):
    if not file_path:
        ui.gosterStatus.setText("Dosya yolu geçerli değil.")
        return
    try:
        df = pd.read_excel(file_path)
        df['urun_maliyeti']= None
        df.columns = [slugify(col) for col in df.columns]
        df.columns = [translate_column_name(col) for col in df.columns]
        cols = df.columns.tolist()
        cols.insert(0, cols.pop(cols.index('urun_maliyeti')))
        df = df.reindex(columns=cols)
        con = sqlite3.connect("orders.db")
        df.to_sql("orders", con, if_exists="replace", index=False)
        con.close()
        ui.gosterStatus.setText("Excel verisi başarıyla veritabanına aktarıldı.")
        display_data_in_table()
    except Exception as e:
        print("Hata:", e)


def display_data_in_table():
    con = sqlite3.connect("orders.db")
    eg = pd.read_sql_query("SELECT * FROM orders", con)
    ui.tableWidget.setRowCount(eg.shape[0])
    ui.tableWidget.setColumnCount(eg.shape[1])
    ui.tableWidget.setHorizontalHeaderLabels(eg.columns)
    
    for i in range(eg.shape[0]):
        for j in range(eg.shape[1]):              
            if pd.isna(eg.iloc[i, j]):
                value = "NULL"
                item = QTableWidgetItem(value.upper())
                item.setBackground(QColor(200, 200, 200)) 
                ui.tableWidget.setItem(i, j, item)
            else:
                value = str(eg.iloc[i, j])
                item = QTableWidgetItem(value.upper()) 
                ui.tableWidget.setItem(i, j, item)
                
    urun_maliyeti_index = eg.columns.get_loc('urun_maliyeti')
   
    for i in range(eg.shape[0]):
        cost = eg.loc[i, 'urun_maliyeti'] 
        cost_item = QLineEdit(cost)  
        cost_item.returnPressed.connect(lambda: get_selected_row_data(ui))
        if not pd.isna(cost):
            cost_item.setStyleSheet("background-color: rgba(200, 200, 200, 100);")
        ui.tableWidget.setCellWidget(i, urun_maliyeti_index, cost_item) 
        

def get_selected_row_data(ui):
    selected_row = ui.tableWidget.currentRow()
    if selected_row != -1:
        row_data = []
        for column in range(ui.tableWidget.columnCount()):  
            item = ui.tableWidget.item(selected_row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")
        
        siparis_numarasi = row_data[8]
        

        con = sqlite3.connect("orders.db")
        eg = pd.read_sql_query("SELECT * FROM orders", con)  
        urun_maliyeti_index = eg.columns.get_loc('urun_maliyeti')
        maliyet_widget = ui.tableWidget.cellWidget(selected_row, urun_maliyeti_index)
        maliyet_degeri = maliyet_widget.text()
        
    
        cursor = con.cursor()
        cursor.execute("UPDATE orders SET urun_maliyeti = ? WHERE siparis_numarasi = ?", (maliyet_degeri, siparis_numarasi))
        con.commit()
        con.close()
        
        print("Seçili satır verileri: ")
        

        display_data_in_table()  
    else:
        print("Hiçbir satır seçili değil.")  


display_data_in_table()
create_orders_table()
ui.maliyetGir.clicked.connect(lambda: get_selected_row_data(ui))
ui.veriYukle.clicked.connect(select_excel_file)



sys.exit(app.exec_())
