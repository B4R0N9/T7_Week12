# ======================================================
# Nama  : M. Danuarta Wiraguna
# NIM   : F1D02310124
# Kelas : C
# ======================================================

import sys
import pandas as pd
import matplotlib
matplotlib.use('QtAgg')

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QFrame,
    QLineEdit,
    QHeaderView,
    QTabWidget
)

from PySide6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ======================================================
# CLASS GRAFIK
# ======================================================

class GrafikCanvas(FigureCanvas):

    def __init__(self):

        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)

        super().__init__(self.fig)

    # ==================================================

    def tampilkan_bar_chart(self, data):

        self.ax.clear()

        self.ax.bar(
            data.index,
            data.values
        )

        self.ax.set_title("Total Sales Product")
        self.ax.set_xlabel("Product Line")
        self.ax.set_ylabel("Sales")

        self.ax.tick_params(
            axis='x',
            rotation=20
        )

        self.draw()

    # ==================================================

    def tampilkan_pie_chart(self, data):

        self.ax.clear()

        self.ax.pie(
            data,
            labels=data.index,
            autopct='%1.1f%%',
            startangle=90
        )

        self.ax.set_title("Payment Distribution")

        self.draw()


# ======================================================
# CLASS DASHBOARD
# ======================================================

class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Dashboard Analisis Penjualan")
        self.resize(1400, 850)

        # LOAD DATA
        self.df = pd.read_csv("supermarket_sales.csv")

        self.setup_ui()

        self.load_dashboard()

    # ==================================================

    def setup_ui(self):

        main_layout = QHBoxLayout(self)

        # ==================================================
        # SIDEBAR
        # ==================================================

        sidebar = QFrame()

        sidebar.setFixedWidth(250)

        sidebar.setStyleSheet("""
            background-color: #1f2937;
            border-radius: 10px;
        """)

        sidebar_layout = QVBoxLayout(sidebar)

        title_sidebar = QLabel("DASHBOARD")

        title_sidebar.setAlignment(Qt.AlignCenter)

        title_sidebar.setStyleSheet("""
            color: white;
            font-size: 26px;
            font-weight: bold;
            padding: 20px;
        """)

        sidebar_layout.addWidget(title_sidebar)

        # COMBOBOX FILTER

        sidebar_layout.addWidget(QLabel("Filter Branch"))

        self.combo_branch = QComboBox()

        self.combo_branch.addItem("All Branch")

        for item in sorted(self.df["Branch"].unique()):
            self.combo_branch.addItem(item)

        self.combo_branch.currentTextChanged.connect(
            self.load_dashboard
        )

        sidebar_layout.addWidget(self.combo_branch)

        # SEARCH

        sidebar_layout.addWidget(QLabel("Cari Data"))

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Masukkan keyword..."
        )

        self.search_input.textChanged.connect(
            self.filter_table
        )

        sidebar_layout.addWidget(self.search_input)

        # BUTTON REFRESH

        btn_refresh = QPushButton("Refresh Data")

        btn_refresh.clicked.connect(
            self.load_dashboard
        )

        sidebar_layout.addWidget(btn_refresh)

        # BUTTON EXPORT

        btn_export = QPushButton("Export Grafik")

        btn_export.clicked.connect(
            self.export_chart
        )

        sidebar_layout.addWidget(btn_export)

        sidebar_layout.addStretch()

        # ==================================================
        # CONTENT
        # ==================================================

        content_layout = QVBoxLayout()

        # HEADER

        header = QLabel(
            "SISTEM ANALISIS DATA SUPERMARKET"
        )

        header.setAlignment(Qt.AlignCenter)

        header.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            padding: 15px;
        """)

        content_layout.addWidget(header)

        # ==================================================
        # CARD STATISTIK
        # ==================================================

        card_layout = QHBoxLayout()

        self.card_sales = self.buat_card(
            "TOTAL SALES"
        )

        self.card_transaksi = self.buat_card(
            "JUMLAH TRANSAKSI"
        )

        self.card_branch = self.buat_card(
            "TOTAL BRANCH"
        )

        card_layout.addWidget(self.card_sales)
        card_layout.addWidget(self.card_transaksi)
        card_layout.addWidget(self.card_branch)

        content_layout.addLayout(card_layout)

        # ==================================================
        # TAB
        # ==================================================

        self.tabs = QTabWidget()

        # TAB VISUALISASI

        tab_visual = QWidget()

        visual_layout = QHBoxLayout(tab_visual)

        self.chart_bar = GrafikCanvas()
        self.chart_pie = GrafikCanvas()

        visual_layout.addWidget(self.chart_bar)
        visual_layout.addWidget(self.chart_pie)

        # TAB TABEL

        tab_table = QWidget()

        table_layout = QVBoxLayout(tab_table)

        self.table = QTableWidget()

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table_layout.addWidget(self.table)

        # ADD TAB

        self.tabs.addTab(
            tab_visual,
            "Visualisasi"
        )

        self.tabs.addTab(
            tab_table,
            "Data Tabel"
        )

        content_layout.addWidget(self.tabs)

        # ==================================================

        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet("""

            QWidget{
                background-color: #f3f4f6;
                font-family: Arial;
            }

            QLabel{
                color: #111827;
                font-size: 14px;
            }

            QPushButton{
                background-color: #2563eb;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: #1d4ed8;
            }

            QComboBox, QLineEdit{
                background-color: white;
                padding: 8px;
                border-radius: 5px;
            }

            QTableWidget{
                background-color: white;
                border-radius: 5px;
            }

        """)

    # ==================================================
    # MEMBUAT CARD
    # ==================================================

    def buat_card(self, judul):

        frame = QFrame()

        frame.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 15px;
        """)

        layout = QVBoxLayout(frame)

        label_title = QLabel(judul)

        label_title.setAlignment(Qt.AlignCenter)

        label_value = QLabel("0")

        label_value.setAlignment(Qt.AlignCenter)

        label_value.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(label_title)
        layout.addWidget(label_value)

        frame.nilai = label_value

        return frame

    # ==================================================
    # LOAD DASHBOARD
    # ==================================================

    def load_dashboard(self):

        branch = self.combo_branch.currentText()

        # FILTER DATA

        if branch == "All Branch":

            data_filter = self.df

        else:

            data_filter = self.df[
                self.df["Branch"] == branch
            ]

        # TAMPILKAN TABEL

        self.tampilkan_tabel(data_filter)

        # BAR CHART

        sales_produk = data_filter.groupby(
            "Product line"
        )["Sales"].sum()

        self.chart_bar.tampilkan_bar_chart(
            sales_produk
        )

        # PIE CHART

        payment = data_filter[
            "Payment"
        ].value_counts()

        self.chart_pie.tampilkan_pie_chart(
            payment
        )

        # UPDATE CARD

        total_sales = round(
            data_filter["Sales"].sum(),
            2
        )

        jumlah_transaksi = len(data_filter)

        total_branch = data_filter[
            "Branch"
        ].nunique()

        self.card_sales.nilai.setText(
            f"${total_sales}"
        )

        self.card_transaksi.nilai.setText(
            str(jumlah_transaksi)
        )

        self.card_branch.nilai.setText(
            str(total_branch)
        )

    # ==================================================
    # TABEL
    # ==================================================

    def tampilkan_tabel(self, data):

        kolom = [
            "Invoice ID",
            "Branch",
            "City",
            "Customer type",
            "Product line",
            "Sales",
            "Payment"
        ]

        tampil_data = data[kolom].head(100)

        self.table.setColumnCount(len(kolom))
        self.table.setRowCount(len(tampil_data))

        self.table.setHorizontalHeaderLabels(kolom)

        for row in range(len(tampil_data)):

            for col in range(len(kolom)):

                item = QTableWidgetItem(
                    str(
                        tampil_data.iloc[row, col]
                    )
                )

                item.setFlags(
                    item.flags() ^ Qt.ItemIsEditable
                )

                self.table.setItem(
                    row,
                    col,
                    item
                )

    # ==================================================
    # SEARCH DATA
    # ==================================================

    def filter_table(self):

        keyword = self.search_input.text().lower()

        for row in range(self.table.rowCount()):

            ditemukan = False

            for col in range(self.table.columnCount()):

                item = self.table.item(row, col)

                if item is not None:

                    if keyword in item.text().lower():

                        ditemukan = True
                        break

            self.table.setRowHidden(
                row,
                not ditemukan
            )

    # ==================================================
    # EXPORT GRAFIK
    # ==================================================

    def export_chart(self):

        lokasi, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan Grafik",
            "",
            "PNG Files (*.png)"
        )

        if lokasi:

            self.chart_bar.fig.savefig(lokasi)

            QMessageBox.information(
                self,
                "Berhasil",
                "Grafik berhasil disimpan"
            )


# ======================================================
# MAIN PROGRAM
# ======================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Dashboard()

    window.show()

    sys.exit(app.exec())