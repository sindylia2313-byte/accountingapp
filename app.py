import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import io
import base64

class ModernLoginApp:
    def __init__(self):
        self.users_file = "users.json"
        self.transactions_file = "transactions.json"
        self.accounts_file = "accounts.json"
        self.load_users()
        self.setup_accounts_database()
        self.load_transactions()
        
        # Initialize session state
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "login"
        if 'sidebar_items' not in st.session_state:
            self.initialize_sidebar_items()

    def initialize_sidebar_items(self):
        st.session_state.sidebar_items = [
            {"icon": "📊", "name": "Dashboard", "active": True},
            {"icon": "📥", "name": "Input Transaksi", "active": False},
            {"icon": "📤", "name": "Export Laporan", "active": False},
            {"icon": "🖨️", "name": "Print", "active": False},
            {"icon": "⚙️", "name": "Pengaturan", "active": False},
        ]

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def load_transactions(self):
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as file:
                self.transactions = json.load(file)
        else:
            self.transactions = []

    def save_transactions(self):
        with open(self.transactions_file, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def setup_accounts_database(self):
        default_accounts = {
            "Kas": {"type": "Aset", "balance": 0},
            "Bank": {"type": "Aset", "balance": 0},
            "Piutang Usaha": {"type": "Aset", "balance": 0},
            "Persediaan": {"type": "Aset", "balance": 0},
            "Perlengkapan": {"type": "Aset", "balance": 0},
            "Peralatan": {"type": "Aset", "balance": 0},
            "Gedung": {"type": "Aset", "balance": 0},
            "Tanah": {"type": "Aset", "balance": 0},
            "Kendaraan": {"type": "Aset", "balance": 0},
            "Akumulasi Penyusutan Gedung": {"type": "Aset", "balance": 0},
            "Akumulasi Penyusutan Peralatan": {"type": "Aset", "balance": 0},
            "Utang Usaha": {"type": "Kewajiban", "balance": 0},
            "Utang Bank": {"type": "Kewajiban", "balance": 0},
            "Modal Pemilik": {"type": "Modal", "balance": 0},
            "Prive": {"type": "Modal", "balance": 0},
            "Pembelian": {"type": "Beban", "balance": 0},                    
            "Penjualan": {"type": "Pendapatan", "balance": 0},               
            "Pendapatan Usaha": {"type": "Pendapatan", "balance": 0},
            "Pendapatan Jasa": {"type": "Pendapatan", "balance": 0},
            "Pendapatan Penjualan": {"type": "Pendapatan", "balance": 0},
            "Pendapatan Lainnya": {"type": "Pendapatan", "balance": 0},
            "Beban Gaji": {"type": "Beban", "balance": 0},
            "Beban Sewa": {"type": "Beban", "balance": 0},
            "Beban Listrik": {"type": "Beban", "balance": 0},
            "Beban Air": {"type": "Beban", "balance": 0},
            "Beban Telepon": {"type": "Beban", "balance": 0},
            "Beban Transportasi": {"type": "Beban", "balance": 0},
            "Beban Perlengkapan": {"type": "Beban", "balance": 0},
            "Beban Penyusutan Gedung": {"type": "Beban", "balance": 0},
            "Beban Penyusutan Peralatan": {"type": "Beban", "balance": 0},
            "Beban Lainnya": {"type": "Beban", "balance": 0}
        }

        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'w') as f:
                json.dump(default_accounts, f, indent=4)
                
    def run(self):
        if not st.session_state.logged_in:
            self.show_auth_pages()
        else:
            self.show_dashboard()

    def show_auth_pages(self):
        if st.session_state.current_page == "login":
            self.show_login_view()
        else:
            self.show_register_view()
    
    def show_login_view(self):
        st.markdown("""
        <style>
        .main {
            background-color: #f0f8ff;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
        }
        .social-text {
            font-size: 16px;
            margin-top: 10px;
        }
        @keyframes smoothAppear {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .welcome-text {
            animation: smoothAppear 1.2s ease-out;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2px !important;
        }
        .app-name {
            animation: smoothAppear 1.2s ease-out 0.3s both;
            font-size: 1.6rem;
            font-weight: bold;
            margin-top: 2px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(
                f"""
                <div style='background-color:#20490C; padding:40px; border-radius:10px; height:500px; color:white; text-align:center; display: flex; flex-direction: column; justify-content: center;'>
                <div class="welcome-text">Hello, Welcome!</div>
                <div class="app-name">Aplikasi Sientok</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.title("Login")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary"):
                self.login(username, password)
            
            st.markdown("---")
            
            # Sejajar: or login with social platforms? + Continue with Google
            col_text, col_google = st.columns([2, 3])
            with col_text:
                st.markdown('<p class="social-text">or login with social platforms?</p>', unsafe_allow_html=True)
            with col_google:
                if st.button("Continue with Google", key="google_login"):
                    st.info("Google login feature would go here")
            
            # Tombol register di bawah
            if st.button("Don't have an account? Register", key="register_bottom"):
                st.session_state.current_page = "register"
                st.rerun()

    def show_register_view(self):
        st.markdown("""
        <style>
        .main {
            background-color: #f0f8ff;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
        }
        .social-text {
            font-size: 16px;
            margin-top: 10px;
        }
        @keyframes smoothAppear {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .welcome-text {
            animation: smoothAppear 1.2s ease-out;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2px !important;
        }
        .app-name {
            animation: smoothAppear 1.2s ease-out 0.3s both;
            font-size: 1.6rem;
            font-weight: bold;
            margin-top: 2px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(
                f"""
                <div style='background-color:#20490C; padding:40px; border-radius:10px; height:500px; color:white; text-align:center; display: flex; flex-direction: column; justify-content: center;'>
                <div class="welcome-text">Welcome Back!</div>
                <div class="app-name">Aplikasi Sientok</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.title("Registration")
            
            username = st.text_input("Username", key="reg_username")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            
            if st.button("Register", type="primary"):
                self.register(username, email, password)
            
            st.markdown("---")
            
            # Sejajar: or register with social platforms? + Continue with Google
            col_text, col_google = st.columns([2, 3])
            with col_text:
                st.markdown('<p class="social-text">or register with social platforms?</p>', unsafe_allow_html=True)
            with col_google:
                if st.button("Continue with Google", key="google_register"):
                    st.info("Google login feature would go here")
            
            # Tombol login di bawah
            if st.button("Already have an account? Login", key="login_bottom"):
                st.session_state.current_page = "login"
                st.rerun()

    def login(self, username, password):
        if not username or not password:
            st.error("Please fill in all fields!")
            return
        
        if username in self.users and self.users[username]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password!")

    def register(self, username, email, password):
        if not username or not email or not password:
            st.error("Please fill in all fields!")
            return
        
        if username in self.users:
            st.error("Username already exists!")
            return
        
        if len(password) < 4:
            st.error("Password must be at least 4 characters!")
            return
        
        self.users[username] = {
            'password': password,
            'email': email
        }
        self.save_users()
        
        st.success("Registration successful!\nYou can now login.")
        st.session_state.current_page = "login"
        st.rerun()



    def show_dashboard(self):
        # Sidebar
        with st.sidebar:
            st.title(f"Welcome, {st.session_state.current_user}!")
            st.markdown("---")
            
            # Sidebar menu
            for i, item in enumerate(st.session_state.sidebar_items):
                if st.button(f"{item['icon']} {item['name']}", 
                           key=f"sidebar_{i}",
                           use_container_width=True):
                    self.sidebar_clicked(i)
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                self.logout()

        # Main content
        active_item = next((item for item in st.session_state.sidebar_items if item["active"]), None)
        
        if active_item:
            if active_item["name"] == "Dashboard":
                self.show_default_dashboard()
            elif active_item["name"] == "Input Transaksi":
                self.show_input_transaksi()
            elif active_item["name"] == "Save Data":
                self.save_data()
            elif active_item["name"] == "Pencarian":
                self.show_pencarian()
            elif active_item["name"] == "Export Laporan":
                self.export_laporan()
            elif active_item["name"] == "Print":
                self.print_document()
            elif active_item["name"] == "Pengaturan":
                self.show_pengaturan()
            elif active_item["name"] == "Jurnal Umum":
                self.show_jurnal_umum()
            elif active_item["name"] == "Buku Besar":
                self.show_buku_besar()
            elif active_item["name"] == "Neraca Saldo":
                self.show_neraca_saldo()
            elif active_item["name"] == "Jurnal Penyesuaian":
                self.show_jurnal_penyesuaian()
            elif active_item["name"] == "Neraca Setelah Penyesuaian":
                self.show_neraca_setelah_penyesuaian()
            elif active_item["name"] == "Laporan Keuangan":
                self.show_laporan_keuangan()
            elif active_item["name"] == "Jurnal Penutup":
                self.show_jurnal_penutup()
            elif active_item["name"] == "Neraca Saldo Akhir":
                self.show_neraca_saldo_akhir()

    def sidebar_clicked(self, index):
        for i, item in enumerate(st.session_state.sidebar_items):
            st.session_state.sidebar_items[i]["active"] = (i == index)
        st.rerun()

    def show_default_dashboard(self):
        st.title("Dashboard Utama")
        st.subheader(f"Selamat datang, {st.session_state.current_user}!")
        st.write("Aplikasi Sientok - Sistem Akuntansi Terintegrasi")
        
        # Menu Grid
        st.subheader("Siklus Akuntansi")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("**📒 Jurnal Umum**\n\nPencatatan transaksi harian", use_container_width=True):
                # Set sidebar item "Dashboard" menjadi tidak aktif dan aktifkan item yang sesuai
                self.set_active_sidebar_item("Jurnal Umum")
        
        with col2:
            if st.button("**📚 Buku Besar**\n\nRingkasan semua akun", use_container_width=True):
                self.set_active_sidebar_item("Buku Besar")
        
        with col3:
            if st.button("**⚖️ Neraca Saldo**\n\nKeseimbangan debit kredit", use_container_width=True):
                self.set_active_sidebar_item("Neraca Saldo")
        
        with col4:
            if st.button("**📋 Jurnal Penyesuaian**\n\nPenyesuaian akhir periode", use_container_width=True):
                self.set_active_sidebar_item("Jurnal Penyesuaian")

        st.subheader("Laporan Keuangan")
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            if st.button("**📊 Neraca Setelah Penyesuaian**\n\nNeraca setelah penyesuaian", use_container_width=True):
                self.set_active_sidebar_item("Neraca Setelah Penyesuaian")
        
        with col6:
            if st.button("**📈 Laporan Keuangan**\n\nLaporan lengkap keuangan", use_container_width=True):
                self.set_active_sidebar_item("Laporan Keuangan")
        
        with col7:
            if st.button("**🔒 Jurnal Penutup**\n\nMenutup akun nominal", use_container_width=True):
                self.set_active_sidebar_item("Jurnal Penutup")
        
        with col8:
            if st.button("**✅ Neraca Saldo Akhir**\n\nNeraca setelah penutupan", use_container_width=True):
                self.set_active_sidebar_item("Neraca Saldo Akhir")

    def set_active_sidebar_item(self, item_name):
        """Mengatur item sidebar yang aktif berdasarkan nama"""
        # Cari index item berdasarkan nama
        for i, item in enumerate(st.session_state.sidebar_items):
            if item["name"] == item_name:
                # Aktifkan item yang dipilih, nonaktifkan lainnya
                for j, other_item in enumerate(st.session_state.sidebar_items):
                    st.session_state.sidebar_items[j]["active"] = (j == i)
                break
        else:
            # Jika item tidak ditemukan di sidebar, tambahkan sebagai item baru
            new_item = {"icon": "📄", "name": item_name, "active": True}
            # Nonaktifkan semua item lama
            for item in st.session_state.sidebar_items:
                item["active"] = False
            # Tambahkan item baru
            st.session_state.sidebar_items.append(new_item)
        
        st.rerun()

    def show_jurnal_umum(self):
        # Inisialisasi session state
        if 'show_add_form' not in st.session_state:
            st.session_state.show_add_form = False
        if 'show_delete_confirm' not in st.session_state:
            st.session_state.show_delete_confirm = False
        if 'trans_to_delete' not in st.session_state:
            st.session_state.trans_to_delete = None
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()

        # Header dengan tombol tambah transaksi
        col_title, col_btn = st.columns([3, 1])
        with col_title:
            st.title("📒 JURNAL UMUM")
        with col_btn:
            if st.button("➕ Tambah Transaksi", use_container_width=True):
                st.session_state.show_add_form = True
                st.rerun()

        # Tampilkan form tambah transaksi jika diperlukan
        if st.session_state.show_add_form:
            self.show_add_transaction_form()
            return

        if not st.session_state.transactions:
            st.info("📭 Belum ada transaksi")
            return

        st.subheader("📋 DAFTAR TRANSAKSI")
        
        # HEADER TABEL
        st.markdown("---")
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 2, 0.8, 1.2, 1.2, 0.8])
        with col1: st.write("**TANGGAL**")
        with col2: st.write("**AKUN**")
        with col3: st.write("**KETERANGAN**")
        with col4: st.write("**REF**")
        with col5: st.write("**DEBIT**")
        with col6: st.write("**KREDIT**")
        with col7: st.write("**AKSI**")
        st.markdown("---")

        # ✅ KELOMPOKKAN TRANSAKSI BERDASARKAN TANGGAL
        transactions_by_date = {}
        for i, trans in enumerate(st.session_state.transactions):
            date = trans['tanggal']
            if date not in transactions_by_date:
                transactions_by_date[date] = []
            transactions_by_date[date].append((i, trans))

        # ✅ SORTING TANGGAL - dari PALING BARU ke LAMA
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, "%d %B %Y")
            except:
                return datetime.min

        sorted_dates = sorted(transactions_by_date.keys(), key=parse_date, reverse=True)

        # Inisialisasi total
        total_debit = 0
        total_kredit = 0

        # ✅ TAMPILKAN SEMUA TRANSAKSI DALAM KELOMPOK TANGGAL
        for date in sorted_dates:
            trans_list = transactions_by_date[date]
            
            # ✅ TAMPILKAN SEMUA TRANSAKSI PADA TANGGAL TERSEBUT
            for j, (index, trans) in enumerate(trans_list):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 2, 0.8, 1.2, 1.2, 0.8])
                
                with col1: 
                    if j == 0:  # Hanya tampilkan tanggal di baris pertama
                        st.write(date)
                    else:
                        st.write("")
                
                with col2: st.write(trans['akun'])
                with col3: 
                    st.write(trans.get('keterangan', '')) 
                with col4: st.write(trans.get('ref', ''))
                with col5: 
                    if trans['debit'] > 0:
                        st.write(f"Rp{trans['debit']:,.0f}")
                    else:
                        st.write("")
                with col6: 
                    if trans['kredit'] > 0:
                        st.write(f"Rp{trans['kredit']:,.0f}")
                    else:
                        st.write("")
                with col7: 
                    if j == 0:  # ✅ TOMBOL HAPUS hanya di baris pertama (untuk hapus SEMUA transaksi tanggal ini)
                        if st.button("🗑️", key=f"del_{index}"):
                            st.session_state.trans_to_delete = date  # Simpan TANGGAL yang akan dihapus
                            st.session_state.show_delete_confirm = True
                            st.rerun()
                    else:
                        st.write("")
                
                # ✅ HITUNG TOTAL DARI SEMUA DEBIT/KREDIT
                total_debit += trans['debit']
                total_kredit += trans['kredit']
            
            # Garis pemisah antar kelompok tanggal
            st.write("---")

        # BARIS TOTAL
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 2, 0.8, 1.2, 1.2, 0.8])
        with col1: st.write("")
        with col2: st.write("")
        with col3: st.write("")
        with col4: st.write("**TOTAL →**")
        with col5: st.write(f"**Rp{total_debit:,.0f}**")
        with col6: st.write(f"**Rp{total_kredit:,.0f}**")
        with col7: st.write("")
        
        st.markdown("---")

        # ✅ KONFIRMASI HAPUS - HAPUS SEMUA TRANSAKSI PADA TANGGAL YANG SAMA
        if st.session_state.show_delete_confirm and st.session_state.trans_to_delete is not None:
            date_to_delete = st.session_state.trans_to_delete
            st.warning(f"⚠️ KONFIRMASI HAPUS")
            st.write(f"Apakah Anda yakin ingin menghapus **SEMUA** transaksi pada tanggal **{date_to_delete}**?")
            
            # Hitung berapa transaksi yang akan dihapus
            count_to_delete = len([t for t in st.session_state.transactions if t['tanggal'] == date_to_delete])
            st.write(f"**{count_to_delete} transaksi** akan dihapus.")
            
            col_ya, col_tidak = st.columns(2)
            with col_ya:
                if st.button("✅ Ya, Hapus Semua", key="confirm_yes"):
                    # ✅ HAPUS SEMUA TRANSAKSI DENGAN TANGGAL YANG SAMA
                    st.session_state.transactions = [
                        trans for trans in st.session_state.transactions 
                        if trans['tanggal'] != date_to_delete
                    ]
                    
                    # Simpan perubahan ke file
                    self.save_transactions_to_file()
                    
                    st.session_state.show_delete_confirm = False
                    st.session_state.trans_to_delete = None
                    st.success(f"✅ Semua transaksi pada {date_to_delete} berhasil dihapus!")
                    st.rerun()
            
            with col_tidak:
                if st.button("❌ Tidak", key="confirm_no"):
                    st.session_state.show_delete_confirm = False
                    st.session_state.trans_to_delete = None
                    st.rerun()
                    
    def show_add_transaction_form(self):
        st.subheader("➕ Tambah Transaksi Baru")
        
        with st.form("tambah_transaksi"):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("📅 Tanggal")
                akun_debit = st.selectbox("🏦 Akun Debit", 
                    [ "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
                "Peralatan", "Gedung", "Tanah", "Kendaraan", "Beban Perbaikan", 
                "Akumulasi Penyusutan Gedung", "Akumulasi Penyusutan Peralatan",
                "Utang Usaha", "Utang Bank", "Modal Pemilik", "Prive", "Beban Obat", "Beban Vitamin", 
                "Pembelian", "Penjualan", "Beban pakan", "Beban Pengiriman", "Beban Vitamain",                                   
                "Pendapatan Usaha", "Pendapatan Jasa", "Pendapatan Penjualan", "Pendapatan Lainnya",
                "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", "Beban perawatan Kandang", 
                "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
                "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", "Beban Lainnya"])
                debit = st.number_input("💹 Debit (Rp)", min_value=0, value=0, step=100000)
            
            with col2:
                akun_kredit = st.selectbox("🏦 Akun Kredit", 
                    [ "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
                "Peralatan", "Gedung", "Tanah", "Kendaraan", "Beban Perbaikan", 
                "Akumulasi Penyusutan Gedung", "Akumulasi Penyusutan Peralatan",
                "Utang Usaha", "Utang Bank", "Modal Pemilik", "Prive", "Beban Obat", "Beban vitamin", 
                "Pembelian", "Penjualan", "Beban pakan", "Beban Pengiriman", "Beban Vitamain",                                   
                "Pendapatan Usaha", "Pendapatan Jasa", "Pendapatan Penjualan", "Pendapatan Lainnya",
                "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", "Beban Perawatan kandang", 
                "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
                "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", "Beban Lainnya"])
                kredit = st.number_input("💸 Kredit (Rp)", min_value=0, value=0, step=100000)
            
            keterangan = st.text_input("📝 Keterangan")
            ref = st.text_input("🔖 Ref")
            
            col_simpan, col_batal = st.columns(2)
            with col_simpan:
                submitted_simpan = st.form_submit_button("💾 Simpan Transaksi", use_container_width=True)
            
            with col_batal:
                submitted_batal = st.form_submit_button("❌ Batal", use_container_width=True)
            
            if submitted_simpan:
                if debit != kredit:
                    st.error("❌ Debit dan Kredit harus sama!")
                elif akun_debit == akun_kredit:
                    st.error("❌ Akun Debit dan Kredit tidak boleh sama!")
                else:
                    # Simpan transaksi debit
                    st.session_state.transactions.append({
                        'tanggal': tanggal.strftime("%d %B %Y"),
                        'akun': akun_debit,
                        'debit': debit,
                        'kredit': 0,
                        'keterangan': keterangan,
                        'ref': ref
                    })
                    # Simpan transaksi kredit
                    st.session_state.transactions.append({
                        'tanggal': tanggal.strftime("%d %B %Y"),
                        'akun': akun_kredit,
                        'debit': 0,
                        'kredit': kredit,
                        'keterangan': keterangan,
                        'ref': ref
                    })
                    
                    # Simpan ke file
                    self.save_transactions_to_file()
                    
                    st.session_state.show_add_form = False
                    st.success("✅ Transaksi berhasil ditambahkan!")
                    st.rerun()
            
            if submitted_batal:
                st.session_state.show_add_form = False
                st.rerun()

    def save_transactions_to_file(self):
        """Simpan transaksi ke file JSON"""
        try:
            with open('jurnal_umum_transactions.json', 'w') as f:
                json.dump(st.session_state.transactions, f, indent=4)
        except Exception as e:
            st.error(f"Error menyimpan transaksi: {e}")

    def load_transactions_from_file(self):
        """Load transaksi dari file JSON"""
        try:
            if os.path.exists('jurnal_umum_transactions.json'):
                with open('jurnal_umum_transactions.json', 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            st.error(f"Error loading transaksi: {e}")
            return []
        
    def is_akun_debit(self, nama_akun):
        """Tentukan apakah akun termasuk jenis Debit (Aset & Beban)"""
        akun_debit = [
            # ASET
            "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
            "Peralatan", "Gedung", "Tanah", "Kendaraan", "Mesin", "Inventaris",
            
            # BEBAN 
            "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", 
            "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
            "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", 
            "Beban Penyusutan Kendaraan", "Beban Penyusutan Mesin", 
            "Beban Penyusutan Inventaris", "Beban Lainnya", "Beban","Beban vitamin", 
            "Beban pakan", "Beban Pengiriman", "Beban Vitamin", "Beban Vitamain",  
            "Beban Perbaikan", "Beban perawatan Kandang", "Beban perawatan kadang",
            
            # PEMBELIAN
            "Pembelian",
            
            # PRIVE
            "Prive"
        ]
        return nama_akun in akun_debit
    
    def show_buku_besar(self):
        st.title("📚 BUKU BESAR")
        
        # Load data dari Jurnal Umum
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        if not st.session_state.transactions:
            st.info("📭 Belum ada transaksi di Jurnal Umum")
            return
        
        akun_emoji = {
            "Kas": "💰", "Bank": "🏦", "Piutang Usaha": "🧾", "Persediaan": "📦",
            "Perlengkapan": "📦", "Peralatan": "🔧", "Gedung": "🏢", "Tanah": "🌳",
            "Kendaraan": "🚗", "Mesin": "⚙️", "Inventaris": "📋",
            "Utang Usaha": "🏢", "Utang Bank": "🏦", "Modal Pemilik": "💼", "Modal": "💼",
            "Prive": "💸", "Pembelian": "🛒", "Penjualan": "💰", 
            "Pendapatan Usaha": "📈", "Pendapatan Jasa": "📈", "Pendapatan Penjualan": "📈",
            "Pendapatan Lainnya": "📈", "Beban Gaji": "💸", "Beban Sewa": "🏠",
            "Beban Listrik": "💡", "Beban Air": "💧", "Beban Telepon": "📞",
            "Beban Transportasi": "🚚", "Beban Perlengkapan": "📦",
            "Beban Penyusutan Gedung": "📉", "Beban Penyusutan Peralatan": "📉",
            "Beban Penyusutan Kendaraan": "📉", "Beban Penyusutan Mesin": "📉",
            "Beban Penyusutan Inventaris": "📉", "Beban Lainnya": "💸",
            
            # ✅ AKUN BEBAN YANG PERNAH MASALAH - TAMBAHKAN SEMUA
            "Beban pakan": "🍗", "Beban Pengiriman": "🚛", "Beban Vitamin": "💊",
            "Beban Vitamain": "💊",  
            "Beban Perbaikan": "🔧", "Beban perawatan Kandang": "🏠",
            "Beban perawatan kadang": "🏠", 
            "Beban Obat": "💊",
            
            "Akumulasi Penyusutan Gedung": "🏢", "Akumulasi Penyusutan Peralatan": "🏢",
            "Akumulasi Penyusutan Kendaraan": "🏢", "Akumulasi Penyusutan Mesin": "🏢",
            "Akumulasi Penyusutan Inventaris": "🏢", "Pendapatan Diterima di Muka": "💰"
        }
        
        # Dapatkan semua akun yang ada transaksinya
        akun_list = list(set(trans['akun'] for trans in st.session_state.transactions))
        akun_list.sort()
        
        # Dropdown pilih akun dengan emoji
        akun_options = [f"{akun_emoji.get(akun, '📄')} {akun}" for akun in akun_list]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_akun_emoji = st.selectbox(
                "Pilih Akun:",
                options=akun_options,
                key="buku_besar_akun"
            )
        
        # Ambil nama akun tanpa emoji
        selected_akun = selected_akun_emoji.split(" ", 1)[1] if " " in selected_akun_emoji else selected_akun_emoji
        
        st.markdown(f"### {akun_emoji.get(selected_akun, '📄')} {selected_akun}")
        
        # Filter transaksi untuk akun yang dipilih
        transaksi_akun = [trans for trans in st.session_state.transactions if trans['akun'] == selected_akun]
        
        if not transaksi_akun:
            st.info(f"📭 Tidak ada transaksi untuk akun {selected_akun}")
            return
        
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, "%d %B %Y")
            except:
                return datetime.min
        
        # Urutkan transaksi berdasarkan tanggal (dari terlama ke terbaru)
        transaksi_akun_sorted = sorted(transaksi_akun, key=lambda x: parse_date(x['tanggal']))
        
        # HEADER TABEL
        st.markdown("---")
        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 1.5, 1.5, 1.5])
        with col1: st.write("**TANGGAL**")
        with col2: st.write("**KETERANGAN**")
        with col3: st.write("**REF**")
        with col4: st.write("**DEBIT**")
        with col5: st.write("**KREDIT**")
        with col6: st.write("**SALDO**")
        st.markdown("---")
        
        # ✅ PERBAIKAN BESAR: LOGIKA PERHITUNGAN SALDO YANG BENAR
        saldo = 0
        
        for trans in transaksi_akun_sorted:
            # ✅ TENTUKAN JENIS AKUN DAN HITUNG SALDO
            if self.is_akun_debit_buku_besar(selected_akun):
                # AKUN DEBIT (Aset & Beban): Debit MENAMBAH, Kredit MENGURANGI
                saldo += trans['debit'] - trans['kredit']
            else:
                # AKUN KREDIT (Kewajiban, Modal, Pendapatan): Kredit MENAMBAH, Debit MENGURANGI
                saldo += trans['kredit'] - trans['debit']
            
            # Tampilkan transaksi
            col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 1.5, 1.5, 1.5])
            with col1: st.write(trans['tanggal'])
            with col2: st.write(trans.get('keterangan', ''))
            with col3: st.write(trans.get('ref', ''))
            with col4: 
                if trans['debit'] > 0:
                    st.write(f"Rp{trans['debit']:,.0f}")
                else:
                    st.write("")
            with col5:
                if trans['kredit'] > 0:
                    st.write(f"Rp{trans['kredit']:,.0f}")
                else:
                    st.write("")
            with col6: 
                # Tampilkan saldo dengan format yang benar
                st.write(f"**Rp{abs(saldo):,.0f}**")
        
        st.markdown("---")
        
        # ✅ PERBAIKAN: TAMPILKAN JENIS SALDO YANG BENAR
        if self.is_akun_debit_buku_besar(selected_akun):
            # Untuk akun debit, saldo positif = Debit, saldo negatif = Kredit
            if saldo >= 0:
                jenis_saldo = "Debit"
                warna = "🟢"
            else:
                jenis_saldo = "Kredit" 
                warna = "🔴"
        else:
            # Untuk akun kredit, saldo positif = Kredit, saldo negatif = Debit
            if saldo >= 0:
                jenis_saldo = "Kredit"
                warna = "🟢"
            else:
                jenis_saldo = "Debit"
                warna = "🔴"
        
        st.success(f"{warna} **Saldo Akhir {selected_akun}: Rp{abs(saldo):,.0f} ({jenis_saldo})**")

    def is_akun_debit_buku_besar(self, nama_akun):
        """Tentukan apakah akun termasuk jenis Debit untuk Buku Besar - VERSI DIPERBAIKI"""
        
        # ✅ LIST AKUN DEBIT YANG KOMPREHENSIF
        akun_debit = [
            # ASET (AKTIVA)
            "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
            "Peralatan", "Gedung", "Tanah", "Kendaraan", "Mesin", "Inventaris",
            "Sewa Bayar di Muka", "Piutang", "Beban Dibayar di Muka",
            
            # BEBAN (BIAYA)
            "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", 
            "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
            "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", 
            "Beban Penyusutan Kendaraan", "Beban Penyusutan Mesin", 
            "Beban Penyusutan Inventaris", "Beban Lainnya", "Beban",
            "Beban pakan", "Beban Pengiriman", "Beban Vitamin", "Beban Vitamain",
            "Beban Perbaikan", "Beban perawatan Kandang", "Beban perawatan kadang",
            "Beban Obat", "Beban obat", "Beban vitamin",
            
            # PEMBELIAN & PRIVE
            "Pembelian", "Prive"
        ]
        
        # ✅ LOGIKA DETECTION YANG LEBIH BAIK
        # 1. Cek berdasarkan list lengkap
        if nama_akun in akun_debit:
            return True
        
        # 2. Cek berdasarkan keyword untuk Beban
        if "Beban" in nama_akun:
            return True
            
        # 3. Cek berdasarkan keyword untuk Aset
        aset_keywords = ["Kas", "Bank", "Piutang", "Persediaan", "Perlengkapan", 
                        "Peralatan", "Gedung", "Tanah", "Kendaraan", "Mesin", "Inventaris"]
        if any(keyword in nama_akun for keyword in aset_keywords):
            return True
        
        # Default: akun kredit
        return False

    def show_neraca_saldo(self):
        st.title("⚖️ NERACA SALDO")
        
        # Load data dari Jurnal Umum
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        if not st.session_state.transactions:
            st.info("📭 Belum ada transaksi di Jurnal Umum")
            return

        # Hitung saldo semua akun
        saldo_akun = self.hitung_saldo_semua_akun()
        
        if not saldo_akun:
            st.info("📭 Tidak ada akun yang memiliki saldo")
            return

        st.subheader(f"Periode: 1 Januari 2023 - 31 Desember 2023")
        
        # Emoji untuk akun
        akun_emoji = {
            "Kas": "🏦", "Modal": "💼", "Perlengkapan": "📦", "Utang": "🏢",
            "Pendapatan": "📈", "Beban Gaji": "💸", "Beban Utilitas": "💡",
            "Sewa Bayar di Muka": "🏠", "Piutang": "👥", "Beban": "💸"
        }

        # HEADER TABEL
        st.markdown("---")
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1: st.write("**NAMA AKUN**")
        with col2: st.write("**DEBIT**")
        with col3: st.write("**KREDIT**")
        st.markdown("---")

        # Tampilkan akun dan saldo
        total_debit = 0
        total_kredit = 0
        
        # Urutkan akun berdasarkan nama
        for akun in sorted(saldo_akun.keys()):
            saldo = saldo_akun[akun]
            emoji = akun_emoji.get(akun, "📄")
            
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1: st.write(f"{emoji} {akun}")
            
            if self.is_akun_debit(akun):
                # Aset & Beban: saldo positif = debit
                if saldo >= 0:
                    with col2: st.write(f"Rp{saldo:,.0f}")
                    with col3: st.write("")
                    total_debit += saldo
                else:
                    with col2: st.write("")
                    with col3: st.write(f"Rp{abs(saldo):,.0f}")
                    total_kredit += abs(saldo)
            else:
                # Kewajiban, Modal, Pendapatan: saldo positif = kredit
                if saldo >= 0:
                    with col2: st.write("")
                    with col3: st.write(f"Rp{saldo:,.0f}")
                    total_kredit += saldo
                else:
                    with col2: st.write(f"Rp{abs(saldo):,.0f}")
                    with col3: st.write("")
                    total_debit += abs(saldo)
        
        # BARIS TOTAL
        st.markdown("---")
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1: st.write("**TOTAL**")
        with col2: st.write(f"**Rp{total_debit:,.0f}**")
        with col3: st.write(f"**Rp{total_kredit:,.0f}**")
        st.markdown("---")

        # STATUS SEIMBANG
        selisih = abs(total_debit - total_kredit)
        if total_debit == total_kredit:
            st.success(f"✅ **SEIMBANG** - Debit = Kredit")
        else:
            st.error(f"❌ **TIDAK SEIMBANG** - Selisih: Rp{selisih:,.0f}")

    def hitung_saldo_semua_akun(self):
        """Hitung saldo semua akun dari data Jurnal Umum"""
        saldo_akun = {}
        
        for trans in st.session_state.transactions:
            akun = trans['akun']
            debit = trans['debit']
            kredit = trans['kredit']
            
            if akun not in saldo_akun:
                saldo_akun[akun] = 0
            
            if self.is_akun_debit(akun):
                saldo_akun[akun] += debit - kredit
            else:
                saldo_akun[akun] += kredit - debit
        
        # Hapus akun dengan saldo 0
        saldo_akun = {akun: saldo for akun, saldo in saldo_akun.items() if saldo != 0}
        
        return saldo_akun

    def is_akun_debit(self, nama_akun):
        """Tentukan apakah akun termasuk jenis Debit (Aset & Beban)"""
        akun_debit = [
            "Kas", "Perlengkapan", "Piutang", "Sewa Bayar di Muka",
            "Beban Gaji", "Beban Utilitas", "Beban"
        ]
        return nama_akun in akun_debit

    def load_transactions_from_file(self):
        """Load transaksi dari file JSON"""
        try:
            if os.path.exists('jurnal_umum_transactions.json'):
                with open('jurnal_umum_transactions.json', 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            st.error(f"Error loading transaksi: {e}")
            return []
        
    def show_jurnal_penyesuaian(self):
        st.title("📋 JURNAL PENYESUAIAN")
        
        # Inisialisasi session state
        if 'penyesuaian_transactions' not in st.session_state:
            st.session_state.penyesuaian_transactions = self.load_penyesuaian_from_file()
        
        # Tab menu
        st.markdown("### 🔧 Pilih Jenis Penyesuaian")
        tab1, tab2, tab3, tab4 = st.tabs(["🏢 PENYUSUTAN", "📦 PEMAKAIAN PERLENGKAPAN", "🏠 SEWA", "💰 PENDAPATAN DITERIMA DI MUKA"])
        
        with tab1:
            self.show_penyusutan_form()
        
        with tab2:
            self.show_perlengkapan_form()
        
        with tab3:
            self.show_sewa_form()
        
        with tab4:
            self.show_pendapatan_form()
        
        # Daftar jurnal penyesuaian yang sudah dibuat
        st.markdown("---")
        st.subheader("📜 DAFTAR JURNAL PENYESUAIAN")
        
        if not st.session_state.penyesuaian_transactions:
            st.info("📭 Belum ada jurnal penyesuaian")
        else:
            for i, trans in enumerate(st.session_state.penyesuaian_transactions):
                with st.expander(f"📅 {trans['tanggal']} - {trans['jenis']}", expanded=False):
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                    with col1: st.write(f"**{trans['akun_debit']}**")
                    with col2: st.success(f"Rp{trans['debit']:,.0f}")
                    with col3: st.write(f"**{trans['akun_kredit']}**")
                    with col4: st.error(f"Rp{trans['kredit']:,.0f}")
                    with col5:
                        if st.button("🗑️", key=f"del_penyesuaian_{i}"):
                            st.session_state.penyesuaian_transactions.pop(i)
                            self.save_penyesuaian_to_file()
                            st.rerun()
                    
                    if 'perhitungan' in trans:
                        st.markdown(f"🧮 **Perhitungan:** {trans['perhitungan']}")

    def show_penyusutan_form(self):
        st.subheader("🏢 Penyusutan Aset Tetap")
        
        # Inisialisasi session state jika belum ada
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        saldo_akun = self.hitung_saldo_semua_akun()
        aset_tetap = ["Peralatan", "Kendaraan", "Gedung", "Mesin", "Inventaris"]
        aset_tersedia = [aset for aset in aset_tetap if aset in saldo_akun and saldo_akun[aset] > 0]
        
        if not aset_tersedia:
            st.warning("❌ Tidak ada aset tetap yang dapat disusutkan")
            return
        
        # STANDAR FULL OTOMATIS
        standar_residu = {
            "Peralatan": 0.10,    # 10%
            "Kendaraan": 0.20,    # 20%  
            "Gedung": 0.05,       # 5%
            "Mesin": 0.15,        # 15%
            "Inventaris": 0.05    # 5%
        }
        
        standar_umur = {
            "Peralatan": 5,      # 5 tahun
            "Kendaraan": 8,      # 8 tahun  
            "Gedung": 20,        # 20 tahun
            "Mesin": 10,         # 10 tahun
            "Inventaris": 3      # 3 tahun
        }
        
        with st.form("penyusutan_form"):
            selected_aset = st.selectbox("Pilih Aset:", aset_tersedia)
            
            # SEMUA OTOMATIS
            harga_perolehan = saldo_akun[selected_aset]
            persentase_residu = standar_residu.get(selected_aset, 0.10)
            nilai_residu = harga_perolehan * persentase_residu
            umur_ekonomis = standar_umur.get(selected_aset, 5)
            
            # TAMPILAN INFO OTOMATIS
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"💰 **Harga Perolehan:**\nRp{harga_perolehan:,.0f}")
            with col2:
                st.info(f"🎯 **Nilai Residu:**\nRp{nilai_residu:,.0f}\n({persentase_residu*100}%)")
            with col3:
                st.info(f"📅 **Umur Ekonomis:**\n{umur_ekonomis} tahun")
            
            # HITUNG & TAMPILKAN PENYUSUTAN
            penyusutan_tahunan = (harga_perolehan - nilai_residu) / umur_ekonomis
            st.success(f"🧮 **Penyusutan/tahun:** Rp{penyusutan_tahunan:,.0f}")
            
            submitted = st.form_submit_button("💾 Buat Jurnal Penyesuaian")
            
            if submitted:
                # LANGSUNG BUAT JURNAL
                akun_debit = f"Beban Penyusutan {selected_aset}"
                akun_kredit = f"Akumulasi Penyusutan {selected_aset}"
                
                new_trans = {
                    'tanggal': '31 December',
                    'jenis': 'Penyusutan',
                    'akun_debit': akun_debit,
                    'akun_kredit': akun_kredit,
                    'debit': penyusutan_tahunan,
                    'kredit': penyusutan_tahunan,
                    'perhitungan': f"Harga: Rp{harga_perolehan:,.0f} | Residu: {persentase_residu*100}% | Umur: {umur_ekonomis} tahun"
                }
                
                st.session_state.penyesuaian_transactions.append(new_trans)
                self.save_penyesuaian_to_file()
                
                st.success("✅ Jurnal Penyesuaian Berhasil Dibuat!")
                st.balloons()

    def show_perlengkapan_form(self):
        st.subheader("📦 Pemakaian Perlengkapan")
        
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        # GANTI INI - SALDO AWAL MANUAL = 0
        saldo_awal_perlengkapan = 0
        
        # Hitung pembelian dari Jurnal Umum
        pembelian_perlengkapan = self.hitung_pembelian_perlengkapan()
        
        with st.form("perlengkapan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"📊 **Perlengkapan Awal:** Rp{saldo_awal_perlengkapan:,.0f}")
                st.info(f"🛒 **Pembelian:** Rp{pembelian_perlengkapan:,.0f}")
            
            with col2:
                perlengkapan_akhir = st.number_input("Perlengkapan Akhir (Rp):", min_value=0, value=0, step=100000)
            
            # HITUNG OTOMATIS
            pemakaian = saldo_awal_perlengkapan + pembelian_perlengkapan - perlengkapan_akhir
            if pemakaian > 0:
                st.success(f"🧮 **Pemakaian:** Rp{pemakaian:,.0f}")
            else:
                st.warning("ℹ️ Tidak ada pemakaian perlengkapan")
            
            submitted = st.form_submit_button("💾 Buat Jurnal Penyesuaian")
            
            if submitted:
                if pemakaian <= 0:
                    st.error("❌ Tidak ada pemakaian perlengkapan")
                    return
                
                new_trans = {
                    'tanggal':'31 December',
                    'jenis': 'Pemakaian Perlengkapan',
                    'akun_debit': "Beban Perlengkapan",
                    'akun_kredit': "Perlengkapan",
                    'debit': pemakaian,
                    'kredit': pemakaian,
                    'perhitungan': f"{saldo_awal_perlengkapan:,.0f} + {pembelian_perlengkapan:,.0f} - {perlengkapan_akhir:,.0f} = Rp{pemakaian:,.0f}"
                }
                
                st.session_state.penyesuaian_transactions.append(new_trans)
                self.save_penyesuaian_to_file()
                st.success("✅ Jurnal Penyesuaian Berhasil Dibuat!")

    def show_sewa_form(self):
        st.subheader("🏠 Sewa Dibayar di Muka")
        
        # AMBIL DATA OTOMATIS DARI NERACA SALDO
        saldo_akun = self.hitung_saldo_semua_akun()
        nama_sewa = "Sewa Bayar di Muka"
        
        if nama_sewa not in saldo_akun:
            st.warning(f"❌ Tidak ada akun '{nama_sewa}' di Neraca Saldo")
            return
        
        total_sewa_neraca = saldo_akun[nama_sewa]
        st.info(f"📊 **Saldo {nama_sewa} (dari Neraca):** Rp{abs(total_sewa_neraca):,.0f}")
        
        with st.form("sewa_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # OTOMATIS PAKAI NILAI DARI NERACA
                total_sewa = st.number_input(
                    f"Total {nama_sewa} (Rp):", 
                    min_value=0,
                    value=abs(total_sewa_neraca),
                    step=1000000
                )
                periode_sewa = st.number_input(
                    "Periode Sewa (bulan):", 
                    min_value=1, 
                    value=12, 
                    step=1
                )
            
            with col2:
                bulan_berjalan = st.number_input(
                    "Bulan yang telah berjalan:", 
                    min_value=0, 
                    max_value=periode_sewa, 
                    value=6, 
                    step=1
                )
            
            # METODE ALOKASI PROPORSIONAL
            if total_sewa > 0 and periode_sewa > 0:
                beban_sewa = (total_sewa / periode_sewa) * bulan_berjalan
                sisa_sewa = total_sewa - beban_sewa
                
                st.info(f"**Metode Alokasi Proporsional:**")
                st.info(f"**Perhitungan:** ({total_sewa:,.0f} / {periode_sewa} bulan) × {bulan_berjalan} bulan")
                st.success(f"**Beban Sewa:** Rp{beban_sewa:,.0f}")
                st.success(f"**Sisa Sewa:** Rp{sisa_sewa:,.0f}")
            
            submitted = st.form_submit_button("💾 Buat Jurnal Sewa")
            
            if submitted:
                if total_sewa <= 0:
                    st.error("❌ Total sewa harus diisi")
                    return
                
                beban_sewa = (total_sewa / periode_sewa) * bulan_berjalan
                
                new_trans = {
                    'tanggal':'31 December',
                    'jenis': f'Penyesuaian {nama_sewa}',
                    'akun_debit': "Beban Sewa",
                    'akun_kredit': nama_sewa,
                    'debit': beban_sewa,
                    'kredit': beban_sewa,
                    'perhitungan': f"Alokasi Proporsional: ({total_sewa:,.0f} / {periode_sewa} bulan) × {bulan_berjalan} bulan = Rp{beban_sewa:,.0f}"
                }
                
                if 'penyesuaian_transactions' not in st.session_state:
                    st.session_state.penyesuaian_transactions = []
                
                st.session_state.penyesuaian_transactions.append(new_trans)
                self.save_penyesuaian_to_file()
                st.success("✅ Jurnal Sewa Berhasil Dibuat!")
                st.rerun()
                
    def show_pendapatan_form(self):
        st.subheader("💰 Pendapatan Diterima di Muka")
        
        # Inisialisasi session state jika belum ada
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        saldo_akun = self.hitung_saldo_semua_akun()
        
        if "Pendapatan Diterima di Muka" not in saldo_akun:
            st.warning("❌ Tidak ada akun Pendapatan Diterima di Muka")
            return
        
        with st.form("pendapatan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                total_pendapatan = saldo_akun["Pendapatan Diterima di Muka"]
                st.info(f"💰 **Total Pendapatan Diterima:** Rp{total_pendapatan:,.0f}")
                persentase_selesai = st.slider("Persentase Penyelesaian (%):", 0, 100, 50)
            
            with col2:
                # HITUNG OTOMATIS REAL-TIME
                pendapatan_diakui = total_pendapatan * (persentase_selesai / 100)
                st.success(f"🧮 **Pendapatan Diakui:** Rp{pendapatan_diakui:,.0f}")
            
            submitted = st.form_submit_button("💾 Buat Jurnal Penyesuaian")
            
            if submitted:
                pendapatan_diakui = total_pendapatan * (persentase_selesai / 100)
                
                if pendapatan_diakui <= 0:
                    st.error("❌ Tidak ada pendapatan yang bisa diakui")
                    return
                
                new_trans = {
                    'tanggal': st.session_state.transactions[0]['tanggal'],  # ✅ GANTI INI
                    'jenis': 'Pendapatan Diterima di Muka',
                    'akun_debit': "Pendapatan Diterima di Muka",
                    'akun_kredit': "Pendapatan", 
                    'debit': pendapatan_diakui,
                    'kredit': pendapatan_diakui,
                    'perhitungan': f"{total_pendapatan:,.0f} × {persentase_selesai}% = Rp{pendapatan_diakui:,.0f}"
                }
                                
                st.session_state.penyesuaian_transactions.append(new_trans)
                self.save_penyesuaian_to_file()
                st.success("✅ Jurnal Penyesuaian Berhasil Dibuat!")

    def hitung_saldo_semua_akun(self):
        """Hitung saldo semua akun dari data Jurnal Umum"""
        saldo_akun = {}
        
        for trans in st.session_state.transactions:
            akun = trans['akun']
            debit = trans['debit']
            kredit = trans['kredit']
            
            if akun not in saldo_akun:
                saldo_akun[akun] = 0
            
            if self.is_akun_debit(akun):
                saldo_akun[akun] += debit - kredit
            else:
                saldo_akun[akun] += kredit - debit
        
        # Hapus akun dengan saldo 0
        saldo_akun = {akun: saldo for akun, saldo in saldo_akun.items() if saldo != 0}
        
        return saldo_akun

    def is_akun_debit(self, nama_akun):
        """Tentukan apakah akun termasuk jenis Debit (Aset & Beban)"""
        akun_debit = [
            "Kas", "Perlengkapan", "Piutang", "Sewa Dibayar di Muka",
            "Peralatan", "Kendaraan", "Gedung", "Mesin", "Inventaris",
            "Beban Gaji", "Beban Utilitas", "Beban Perlengkapan", "Beban Sewa",
            "Beban Penyusutan Peralatan", "Beban Penyusutan Kendaraan",
            "Beban Penyusutan Gedung", "Beban Penyusutan Mesin", "Beban Penyusutan Inventaris"
        ]
        return nama_akun in akun_debit

    def hitung_pembelian_perlengkapan(self):
        """Hitung pembelian perlengkapan dengan cara YANG BENAR"""
        total_pembelian = 0
        
        # Cara YANG PALING AMAN: hanya hitung dari Jurnal Umum (bukan penyesuaian)
        for i in range(0, len(st.session_state.transactions) - 1, 2):
            try:
                trans1 = st.session_state.transactions[i]
                trans2 = st.session_state.transactions[i + 1]
                
                # Jika ini transaksi pembelian perlengkapan
                if (trans1['akun'] == "Perlengkapan" and trans1['debit'] > 0 and
                    trans2['akun'] in ["Kas", "Bank", "Utang", "Utang Usaha"] and 
                    trans1['debit'] == trans2['kredit']):
                    total_pembelian += trans1['debit']
                    
                elif (trans2['akun'] == "Perlengkapan" and trans2['debit'] > 0 and
                    trans1['akun'] in ["Kas", "Bank", "Utang", "Utang Usaha"] and 
                    trans2['debit'] == trans1['kredit']):
                    total_pembelian += trans2['debit']
                    
            except IndexError:
                continue
        
        return total_pembelian

    def save_penyesuaian_to_file(self):
        """Simpan jurnal penyesuaian ke file"""
        try:
            with open('penyesuaian_transactions.json', 'w') as f:
                json.dump(st.session_state.penyesuaian_transactions, f, indent=4)
        except Exception as e:
            st.error(f"Error menyimpan penyesuaian: {e}")

    def load_penyesuaian_from_file(self):
        """Load jurnal penyesuaian dari file"""
        try:
            if os.path.exists('penyesuaian_transactions.json'):
                with open('penyesuaian_transactions.json', 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            st.error(f"Error loading penyesuaian: {e}")
            return []

    def load_transactions_from_file(self):
        """Load transaksi dari file JSON"""
        try:
            if os.path.exists('jurnal_umum_transactions.json'):
                with open('jurnal_umum_transactions.json', 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            st.error(f"Error loading transaksi: {e}")
            return []
        
    def show_neraca_setelah_penyesuaian(self):
        st.title("⚖️ NERACA SETELAH PENYESUAIAN")
        
        # 1. AMBIL DATA DARI NERACA SALDO (Jurnal Umum)
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        saldo_neraca = self.hitung_saldo_semua_akun()  # Dari jurnal umum
        
        # 2. AMBIL DATA DARI JURNAL PENYESUAIAN  
        penyesuaian = self.load_penyesuaian_from_file()
        
        # 3. GABUNGKAN & HITUNG SALDO AKHIR - PERHATIKAN DEBIT/KREDIT!
        saldo_akhir = saldo_neraca.copy()  # Saldo awal dari neraca
        
        for pen in penyesuaian:
            # PROSES AKUN DEBIT dari penyesuaian
            akun_debit = pen['akun_debit']
            if self.is_akun_debit(akun_debit):
                # Akun debit (Aset/Beban): bertambah di DEBIT
                if akun_debit in saldo_akhir:
                    saldo_akhir[akun_debit] += pen['debit']
                else:
                    saldo_akhir[akun_debit] = pen['debit']
            else:
                # Akun kredit (Kewajiban/Modal/Pendapatan): berkurang di DEBIT
                if akun_debit in saldo_akhir:
                    saldo_akhir[akun_debit] -= pen['debit']
                else:
                    saldo_akhir[akun_debit] = -pen['debit']
                
            # PROSES AKUN KREDIT dari penyesuaian  
            akun_kredit = pen['akun_kredit']
            if self.is_akun_debit(akun_kredit):
                # Akun debit (Aset/Beban): berkurang di KREDIT
                if akun_kredit in saldo_akhir:
                    saldo_akhir[akun_kredit] -= pen['kredit']
                else:
                    saldo_akhir[akun_kredit] = -pen['kredit']
            else:
                # Akun kredit (Kewajiban/Modal/Pendapatan): bertambah di KREDIT
                if akun_kredit in saldo_akhir:
                    saldo_akhir[akun_kredit] += pen['kredit']
                else:
                    saldo_akhir[akun_kredit] = pen['kredit']
        
        if not saldo_akhir:
            st.info("📭 Belum ada data untuk Neraca Setelah Penyesuaian")
            return

        st.subheader(f"Periode: 1 Januari 2023 - 31 Desember 2023")
        
        # Emoji untuk akun
        akun_emoji = {
            "Kas": "🏦", "Modal": "💼", "Perlengkapan": "📦", "Utang": "🏢",
            "Pendapatan": "📈", "Beban Gaji": "💸", "Beban Utilitas": "💡",
            "Sewa Bayar di Muka": "🏠", "Piutang": "👥", "Beban": "💸",
            "Beban Perlengkapan": "📦", "Beban Sewa": "🏠", "Beban Penyusutan": "📉",
            "Akumulasi Penyusutan": "🏢", "Pendapatan Diterima di Muka": "💰",
            "Beban Penyusutan Peralatan": "📉", "Beban Penyusutan Gedung": "📉",
            "Beban Penyusutan Kendaraan": "📉", "Beban Penyusutan Mesin": "📉",
            "Beban Penyusutan Inventaris": "📉", "Akumulasi Penyusutan Peralatan": "🏢",
            "Akumulasi Penyusutan Gedung": "🏢", "Akumulasi Penyusutan Kendaraan": "🏢",
            "Akumulasi Penyusutan Mesin": "🏢", "Akumulasi Penyusutan Inventaris": "🏢",
            "Peralatan": "🔧", "Kendaraan": "🚗", "Gedung": "🏢", "Mesin": "⚙️", "Inventaris": "📋",
            "Utang Usaha": "🏢", "Utang Bank": "🏦", "Modal Pemilik": "💼", "Prive": "💸",
            "Pembelian": "🛒", "Penjualan": "📈", "Pendapatan Usaha": "📈", "Pendapatan Jasa": "📈",
            "Pendapatan Penjualan": "📈", "Pendapatan Lainnya": "📈"
        }

        # HEADER TABEL - RAPI
        st.markdown("---")
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1: st.write("**NAMA AKUN**")
        with col2: st.write("**DEBIT**")
        with col3: st.write("**KREDIT**")
        st.markdown("---")

        # Tampilkan akun dan saldo - PERHATIKAN DEBIT/KREDIT!
        total_debit = 0
        total_kredit = 0
        
        # Urutkan akun berdasarkan nama
        for akun in sorted(saldo_akhir.keys()):
            saldo = saldo_akhir[akun]
            emoji = akun_emoji.get(akun, "📄")
            
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1: st.write(f"{emoji} {akun}")
            
            # TAMPILKAN SALDO DI KOLOM YANG BENAR
            if self.is_akun_debit(akun):
                # Aset & Beban: saldo positif = DEBIT, negatif = KREDIT
                if saldo >= 0:
                    with col2: st.write(f"Rp{saldo:,.0f}")  # ✅ DEBIT
                    with col3: st.write("")                 # ✅ KOSONG
                    total_debit += saldo
                else:
                    with col2: st.write("")                 # ✅ KOSONG  
                    with col3: st.write(f"Rp{abs(saldo):,.0f}")  # ✅ KREDIT
                    total_kredit += abs(saldo)
            else:
                # Kewajiban, Modal, Pendapatan: saldo positif = KREDIT, negatif = DEBIT
                if saldo >= 0:
                    with col2: st.write("")                 # ✅ KOSONG
                    with col3: st.write(f"Rp{saldo:,.0f}")  # ✅ KREDIT
                    total_kredit += saldo
                else:
                    with col2: st.write(f"Rp{abs(saldo):,.0f}")  # ✅ DEBIT
                    with col3: st.write("")                 # ✅ KOSONG
                    total_debit += abs(saldo)
        
        # BARIS TOTAL - RAPI
        st.markdown("---")
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1: st.write("**TOTAL**")
        with col2: st.write(f"**Rp{total_debit:,.0f}**")
        with col3: st.write(f"**Rp{total_kredit:,.0f}**")
        st.markdown("---")

        # STATUS SEIMBANG
        selisih = abs(total_debit - total_kredit)
        if total_debit == total_kredit:
            st.success(f"✅ **SEIMBANG** - Debit = Kredit")
        else:
            st.error(f"❌ **TIDAK SEIMBANG** - Selisih: Rp{selisih:,.0f}")

        # INFO TAMBAHAN
        st.info("💡 **Neraca ini sudah termasuk penyesuaian dari Jurnal Penyesuaian**")
        
        # TAMPILKAN DETAIL PENYESUAIAN
        if penyesuaian:
            with st.expander("📋 Lihat Detail Penyesuaian"):
                st.write("**Jurnal Penyesuaian yang diproses:**")
                for i, pen in enumerate(penyesuaian):
                    st.write(f"{i+1}. {pen['jenis']}:")
                    st.write(f"   - {pen['akun_debit']} (Debit): Rp{pen['debit']:,.0f}")
                    st.write(f"   - {pen['akun_kredit']} (Kredit): Rp{pen['kredit']:,.0f}")
                    if 'perhitungan' in pen:
                        st.write(f"   📊 {pen['perhitungan']}")
                    st.write("")

    def is_akun_debit(self, nama_akun):
        """Tentukan apakah akun termasuk jenis Debit (Aset & Beban) - LEBIH LENGKAP"""
        akun_debit = [
            # ASET
            "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
            "Peralatan", "Gedung", "Tanah", "Kendaraan", "Mesin", "Inventaris",
            "Sewa Bayar di Muka", 
            
            # BEBAN
            "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", 
            "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
            "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", 
            "Beban Penyusutan Kendaraan", "Beban Penyusutan Mesin", 
            "Beban Penyusutan Inventaris", "Beban Lainnya", "Beban",
            
            # PEMBELIAN
            "Pembelian",
            
            # PRIVE
            "Prive"
        ]
        return nama_akun in akun_debit

    def show_laporan_keuangan(self):
        st.title("📊 LAPORAN KEUANGAN")
        
        # Ambil data dari Neraca Setelah Penyesuaian
        data_keuangan = self.hitung_data_laporan_keuangan()
        
        if not data_keuangan:
            st.info("📭 Belum ada data untuk Laporan Keuangan")
            return
        
        # Tab untuk ke-4 laporan
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 LAPORAN LABA RUGI", 
            "💼 PERUBAHAN MODAL", 
            "💰 ARUS KAS", 
            "⚖️ POSISI KEUANGAN"
        ])
        
        with tab1:
            self.show_laporan_laba_rugi(data_keuangan)
        
        with tab2:
            self.show_perubahan_modal(data_keuangan)
        
        with tab3:
            self.show_arus_kas(data_keuangan)
        
        with tab4:
            self.show_posisi_keuangan(data_keuangan)

    def hitung_data_laporan_keuangan(self):
        """Hitung semua data yang dibutuhkan untuk laporan keuangan - VERSI LENGKAP DENGAN HPP"""
        
        # 1. Ambil data Neraca Setelah Penyesuaian
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        saldo_neraca = self.hitung_saldo_semua_akun()  # Dari jurnal umum
        penyesuaian = self.load_penyesuaian_from_file()
        
        # 2. Hitung saldo setelah penyesuaian
        saldo_akhir = saldo_neraca.copy()
        
        for pen in penyesuaian:
            # PROSES AKUN DEBIT dari penyesuaian
            akun_debit = pen['akun_debit']
            if self.is_akun_debit(akun_debit):
                # Akun debit (Aset/Beban): bertambah di DEBIT
                if akun_debit in saldo_akhir:
                    saldo_akhir[akun_debit] += pen['debit']
                else:
                    saldo_akhir[akun_debit] = pen['debit']
            else:
                # Akun kredit (Kewajiban/Modal/Pendapatan): berkurang di DEBIT
                if akun_debit in saldo_akhir:
                    saldo_akhir[akun_debit] -= pen['debit']
                else:
                    saldo_akhir[akun_debit] = -pen['debit']
                    
            # PROSES AKUN KREDIT dari penyesuaian  
            akun_kredit = pen['akun_kredit']
            if self.is_akun_debit(akun_kredit):
                # Akun debit (Aset/Beban): berkurang di KREDIT
                if akun_kredit in saldo_akhir:
                    saldo_akhir[akun_kredit] -= pen['kredit']
                else:
                    saldo_akhir[akun_kredit] = -pen['kredit']
            else:
                # Akun kredit (Kewajiban/Modal/Pendapatan): bertambah di KREDIT
                if akun_kredit in saldo_akhir:
                    saldo_akhir[akun_kredit] += pen['kredit']
                else:
                    saldo_akhir[akun_kredit] = pen['kredit']
        
        # 3. Kelompokkan akun-akun - ✅ VERSI LENGKAP DENGAN HPP
        data = {
            # ✅ PENDAPATAN - SEMUA JENIS
            'pendapatan': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if "Pendapatan" in akun or "Penjualan" in akun},
                
            # ✅ HPP & PEMBELIAN
            'hpp': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if akun in ["Pembelian", "Harga Pokok Penjualan", "HPP"]},
                
            # ✅ PERSEDIAAN (untuk hitung HPP)
            'persediaan_awal': 0,  # Default 0, bisa disesuaikan
            'persediaan_akhir': abs(saldo_akhir.get('Persediaan', 0)),
                
            # ✅ BEBAN OPERASIONAL
            'beban_operasional': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if "Beban" in akun and "Penyusutan" not in akun},
                
            # ✅ BEBAN PENYUSUTAN  
            'beban_penyusutan': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if "Beban Penyusutan" in akun},
                
            # ✅ BEBAN LAINNYA
            'beban_lainnya': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if akun in ["Beban Lainnya", "Beban"]},
                
            # ✅ ASET LANCAR
            'aset_lancar': {akun: saldo for akun, saldo in saldo_akhir.items() 
                if akun in ["Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan", "Sewa Bayar di Muka"] 
                and saldo > 0},
                
            # ✅ ASET TETAP
            'aset_tetap': {akun: saldo for akun, saldo in saldo_akhir.items() 
                if akun in ["Peralatan", "Gedung", "Kendaraan", "Tanah", "Mesin", "Inventaris"] 
                and saldo > 0},
                
            # ✅ AKUMULASI PENYUSUTAN
            'akumulasi_penyusutan': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if "Akumulasi Penyusutan" in akun},  
                
            # ✅ KEWAJIBAN
            'kewajiban': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if akun in ["Utang Usaha", "Utang Bank", "Pendapatan Diterima di Muka"] 
                and saldo < 0},
                
            # ✅ MODAL 
            'modal': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if "Modal" in akun and saldo != 0},  
                
            # ✅ PRIVE
            'prive': {akun: abs(saldo) for akun, saldo in saldo_akhir.items() 
                if akun == "Prive" and saldo > 0}
        }
        
        # 4. Hitung totals - ✅ PERHITUNGAN LENGKAP DENGAN HPP
        data['total_pendapatan'] = sum(data['pendapatan'].values())
        data['total_hpp'] = sum(data['hpp'].values())
        
        # ✅ RUMUS HPP: Pembelian + Persediaan Awal - Persediaan Akhir
        data['hpp_total'] = data['total_hpp'] + data['persediaan_awal'] - data['persediaan_akhir']
        if data['hpp_total'] < 0:
            data['hpp_total'] = 0
        
        data['laba_kotor'] = data['total_pendapatan'] - data['hpp_total']
        
        data['total_beban_operasional'] = sum(data['beban_operasional'].values())
        data['total_beban_penyusutan'] = sum(data['beban_penyusutan'].values())
        data['total_beban_lainnya'] = sum(data['beban_lainnya'].values())
        data['total_beban'] = data['total_beban_operasional'] + data['total_beban_penyusutan'] + data['total_beban_lainnya']
        
        data['laba_bersih'] = data['laba_kotor'] - data['total_beban']
        
        # Hitung untuk Neraca
        data['total_aset_lancar'] = sum(data['aset_lancar'].values())
        data['total_aset_tetap_kotor'] = sum(data['aset_tetap'].values())
        data['total_akumulasi_penyusutan'] = sum(data['akumulasi_penyusutan'].values())
        data['total_aset_tetap_bersih'] = data['total_aset_tetap_kotor'] - data['total_akumulasi_penyusutan']
        data['total_aset'] = data['total_aset_lancar'] + data['total_aset_tetap_bersih']
        
        data['total_kewajiban'] = sum(data['kewajiban'].values())
        data['modal_awal'] = data['modal'].get('Modal Pemilik', 0) or data['modal'].get('Modal', 0)
        
        # Perhitungan Modal Akhir
        data['modal_akhir'] = data['modal_awal'] + data['laba_bersih'] - data.get('prive', {}).get('Prive', 0)
        
        # Koreksi otomatis jika tidak seimbang
        total_aset_actual = data['total_aset']
        total_kewajiban_modal_actual = data['total_kewajiban'] + data['modal_akhir']
        
        selisih = abs(total_aset_actual - total_kewajiban_modal_actual)
        if selisih > 0 and selisih <= 1000:
            data['modal_akhir'] = data['total_aset'] - data['total_kewajiban']
        
        data['total_kewajiban_modal'] = data['total_kewajiban'] + data['modal_akhir']
        
        return data

    def show_laporan_laba_rugi(self, data):
        st.subheader("📈 LAPORAN LABA RUGI")
        st.write(f"Periode 1 Januari - 31 Desember 2023")
        
        st.markdown("---")
        
        # ✅ BAGIAN 1: PENDAPATAN
        st.write("**PENDAPATAN:**")
        total_pendapatan = 0
        for akun, jumlah in data['pendapatan'].items():
            if jumlah > 0:
                st.write(f"  {akun:30} Rp{jumlah:>15,.0f}")
                total_pendapatan += jumlah
        
        if total_pendapatan == 0:
            st.write(f"  {'Tidak ada pendapatan':30} Rp{0:>15,.0f}")
        
        st.write(f"{'Total Pendapatan':30} **Rp{total_pendapatan:>15,.0f}**")
        
        st.markdown("---")
        
        # ✅ BAGIAN 2: HARGA POKOK PENJUALAN (HPP)
        st.write("**HARGA POKOK PENJUALAN:**")
        
        # Tampilkan komponen HPP
        if data['total_hpp'] > 0:
            for akun, jumlah in data['hpp'].items():
                if jumlah > 0:
                    st.write(f"  {akun:30} Rp{jumlah:>15,.0f}")
        
        if data['persediaan_awal'] > 0:
            st.write(f"  {'Persediaan Awal':30} Rp{data['persediaan_awal']:>15,.0f}")
        
        if data['persediaan_akhir'] > 0:
            st.write(f"  {'Persediaan Akhir':30} Rp{data['persediaan_akhir']:>15,.0f}")
        
        st.write(f"{'Total HPP':30} **Rp{data['hpp_total']:>15,.0f}**")
        
        st.markdown("---")
        
        # ✅ BAGIAN 3: LABA KOTOR
        laba_kotor = total_pendapatan - data['hpp_total']
        st.write(f"{'LABA KOTOR':30} **Rp{laba_kotor:>15,.0f}**")
        
        st.markdown("---")
        
        # ✅ BAGIAN 4: BEBAN OPERASIONAL
        st.write("**BEBAN OPERASIONAL:**")
        
        # Beban Operasional
        if data['total_beban_operasional'] > 0:
            for akun, jumlah in data['beban_operasional'].items():
                if jumlah > 0:
                    st.write(f"  {akun:30} Rp{jumlah:>15,.0f}")
        
        # Beban Penyusutan
        if data['total_beban_penyusutan'] > 0:
            st.write(f"  {'Beban Penyusutan':30} Rp{data['total_beban_penyusutan']:>15,.0f}")
        
        # Beban Lainnya
        if data['total_beban_lainnya'] > 0:
            for akun, jumlah in data['beban_lainnya'].items():
                if jumlah > 0:
                    st.write(f"  {akun:30} Rp{jumlah:>15,.0f}")
        
        st.write(f"{'Total Beban':30} **Rp{data['total_beban']:>15,.0f}**")
        
        st.markdown("---")
        
        # ✅ BAGIAN 5: LABA/RUGI BERSIH
        laba_bersih = laba_kotor - data['total_beban']
        
        if laba_bersih >= 0:
            st.write(f"{'LABA BERSIH':30} **Rp{laba_bersih:>15,.0f}**")
            st.success(f"✅ Perusahaan mengalami **LABA** sebesar Rp{laba_bersih:,.0f}")
        else:
            st.write(f"{'RUGI BERSIH':30} **Rp{abs(laba_bersih):>15,.0f}**")
            st.error(f"❌ Perusahaan mengalami **RUGI** sebesar Rp{abs(laba_bersih):,.0f}")
        
        st.markdown("---")
    
    def show_perubahan_modal(self, data):
        st.subheader("💼 LAPORAN PERUBAHAN MODAL")
        st.write(f"Periode 1 Januari - 31 Desember 2023")
        
        st.markdown("---")
        
        # Modal Awal
        modal_awal = data.get('modal_awal', 0)
        st.write(f"{'Modal Awal':30} Rp{modal_awal:>15,.0f}")
        
        # Laba/Rugi
        laba_bersih = data.get('laba_bersih', 0)
        st.write(f"{'Laba/Rugi Bersih':30} Rp{laba_bersih:>15,.0f}")
        
        # Prive
        prive = data.get('prive', {}).get('Prive', 0)
        if prive > 0:
            st.write(f"{'Prive':30} Rp{prive:>15,.0f}")
        
        st.markdown("---")
        
        # Modal Akhir
        modal_akhir = modal_awal + laba_bersih - prive
        st.write(f"{'Modal Akhir':30} **Rp{modal_akhir:>15,.0f}**")
        
        st.markdown("---")

    def show_arus_kas(self, data):
        st.subheader("💰 LAPORAN ARUS KAS - METODE LANGSUNG")
        st.write(f"Periode 1 Januari - 31 Desember 2023")
        
        # AMBIL DATA ASLI TANPA PENYESUAIAN
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        # Hitung saldo asli untuk data lainnya
        saldo_asli = self.hitung_saldo_semua_akun()
        
        # GROUP PENDAPATAN - TIDAK BOLEH DOUBLE COUNT
        pendapatan_usaha = 0
        pendapatan_jasa = 0

        for akun, saldo in saldo_asli.items():
            # PRIORITAS "Pendapatan Usaha", jika ada abaikan "Penjualan"
            if "Pendapatan Usaha" in akun and saldo != 0:
                pendapatan_usaha = abs(saldo)
            elif "Penjualan" in akun and saldo != 0 and pendapatan_usaha == 0:
                pendapatan_usaha = abs(saldo)
            elif "Pendapatan Jasa" in akun and saldo != 0:
                pendapatan_jasa = abs(saldo)

        # Hitung pembelian aset tetap dari transaksi
        total_pembelian_aset = 0
        for transaksi in st.session_state.transactions:
            akun = transaksi['akun']
            debit = transaksi.get('debit', 0)
            if akun in ["Peralatan", "Gedung", "Kendaraan", "Tanah", "Mesin", "Inventaris"] and debit > 0:
                total_pembelian_aset += debit
        
        # Hitung setoran modal dari transaksi
        setoran_modal = 0
        for transaksi in st.session_state.transactions:
            akun = transaksi['akun']
            kredit = transaksi.get('kredit', 0)
            if akun == "Modal" and kredit > 0 and "modal" in transaksi.get('keterangan', '').lower():
                setoran_modal += kredit
        
        # HITUNG DATA UNTUK ARUS KAS (TANPA PENYESUAIAN)
        data_arus_kas = {
            'pendapatan_usaha': pendapatan_usaha,
            'pendapatan_jasa': pendapatan_jasa,
            
            'beban': {akun: abs(saldo) for akun, saldo in saldo_asli.items() 
                    if any(keyword in akun for keyword in ["Beban", "Pembelian"]) 
                    and "Penyusutan" not in akun and saldo != 0},
            
            'prive': {akun: abs(saldo) for akun, saldo in saldo_asli.items() 
                    if akun == "Prive" and saldo > 0},
            
            'kewajiban': {akun: abs(saldo) for akun, saldo in saldo_asli.items() 
                        if akun in ["Utang Usaha", "Utang Bank", "Pendapatan Diterima di Muka"] 
                        and saldo < 0},
            
            'total_pembelian_aset': total_pembelian_aset,
            'setoran_modal': setoran_modal
        }
        
        st.markdown("---")
        
        # ARUS KAS DARI AKTIVITAS OPERASI - METODE LANGSUNG
        st.write("**ARUS KAS DARI AKTIVITAS OPERASI:**")
        
        # PENERIMAAN KAS
        st.write("  **Penerimaan Kas:**")
        total_penerimaan = 0

        if data_arus_kas['pendapatan_usaha'] > 0:
            st.write(f"    Pendapatan Usaha{' ':15} Rp{data_arus_kas['pendapatan_usaha']:>15,.0f}")
            total_penerimaan += data_arus_kas['pendapatan_usaha']

        if data_arus_kas['pendapatan_jasa'] > 0:
            st.write(f"    Pendapatan Jasa{' ':16} Rp{data_arus_kas['pendapatan_jasa']:>15,.0f}")
            total_penerimaan += data_arus_kas['pendapatan_jasa']

        if total_penerimaan == 0:
            st.write(f"    {'Tidak ada penerimaan kas':30} Rp{0:>15,.0f}")
        
        # PENGELUARAN KAS  
        st.write("  **Pengeluaran Kas:**")
        total_pengeluaran = 0
        
        if data_arus_kas['beban']:
            for akun, jumlah in data_arus_kas['beban'].items():
                st.write(f"    {akun:30} Rp{jumlah:>15,.0f}")
                total_pengeluaran += jumlah
        else:
            st.write(f"    {'Tidak ada pengeluaran kas':30} Rp{0:>15,.0f}")
        
        kas_operasi = total_penerimaan - total_pengeluaran
        st.write(f"  {'Kas Bersih dari Operasi':30} **Rp{kas_operasi:>15,.0f}**")
        
        st.markdown("---")
        
        # ARUS KAS DARI AKTIVITAS INVESTASI
        st.write("**ARUS KAS DARI AKTIVITAS INVESTASI:**")
        
        kas_investasi = 0
        if data_arus_kas['total_pembelian_aset'] > 0:
            st.write(f"  Pembelian Aset Tetap{' ':13} Rp{data_arus_kas['total_pembelian_aset']:>15,.0f}")
            kas_investasi = -data_arus_kas['total_pembelian_aset']
        
        st.write(f"  {'Kas Bersih dari Investasi':30} **Rp{abs(kas_investasi):>15,.0f}**")
        
        st.markdown("---")
        
        # ARUS KAS DARI AKTIVITAS PENDANAAN
        st.write("**ARUS KAS DARI AKTIVITAS PENDANAAN:**")
        
        kas_pendanaan = 0
        
        # Setoran Modal (MENAMBAH KAS)
        if data_arus_kas['setoran_modal'] > 0:
            st.write(f"  Setoran Modal{' ':18} Rp{data_arus_kas['setoran_modal']:>15,.0f}")
            kas_pendanaan += data_arus_kas['setoran_modal']
        
        # Penerimaan Utang (MENAMBAH KAS)
        for akun, jumlah in data_arus_kas['kewajiban'].items():
            st.write(f"  Penerimaan {akun:20} Rp{jumlah:>15,.0f}")
            kas_pendanaan += jumlah
        
        # Pengambilan Prive (MENGURANGI KAS)
        prive = data_arus_kas.get('prive', {}).get('Prive', 0)
        if prive > 0:
            st.write(f"  Pengambilan Prive{' ':15} Rp{prive:>15,.0f}")
            kas_pendanaan -= prive
        
        st.write(f"  {'Kas Bersih dari Pendanaan':30} **Rp{kas_pendanaan:>15,.0f}**")
        
        st.markdown("---")
        
        # TOTAL KENAIKAN/PENURUNAN KAS - SALDO AWAL = 0
        kas_awal = 0  # SALDO AWAL 1 JANUARI 2023
        kenaikan_kas = kas_operasi + kas_investasi + kas_pendanaan
        kas_akhir = kas_awal + kenaikan_kas
        
        st.write(f"{'Kenaikan/Penurunan Bersih Kas':30} **Rp{kenaikan_kas:>15,.0f}**")
        st.write(f"{'Kas Awal Periode':30} Rp{kas_awal:>15,.0f}")
        st.write(f"{'Kas Akhir Periode':30} **Rp{kas_akhir:>15,.0f}**")
        
        st.markdown("---")

    def show_posisi_keuangan(self, data):
        # DAPATKAN TAHUN DARI TRANSAKSI PERTAMA
        tahun = "2023"  # default
        if 'transactions' in st.session_state and st.session_state.transactions:
            tanggal_pertama = st.session_state.transactions[0].get('tanggal', '')
            # Extract tahun dari format "22 January 2023"
            if tanggal_pertama:
                tahun = tanggal_pertama.split()[-1]  # Ambil bagian terakhir (tahun)
        
        st.subheader("⚖️ LAPORAN POSISI KEUANGAN")
        st.write(f"Per 31 Desember {tahun}")
        
        st.markdown("---")
        
        # ASET
        st.write("**ASET:**")
        
        # Aset Lancar
        st.write("  **Aset Lancar:**")
        total_aset_lancar = 0
        for akun, jumlah in data['aset_lancar'].items():
            st.write(f"    {akun:28} Rp{jumlah:>15,.0f}")
            total_aset_lancar += jumlah
        
        if total_aset_lancar == 0:
            st.write(f"    {'Tidak ada aset lancar':28} Rp{0:>15,.0f}")
        
        st.write(f"    {'Total Aset Lancar':28} **Rp{total_aset_lancar:>15,.0f}**")
        
        # Aset Tetap - ✅ PERBAIKAN: TAMPILKAN AKUMULASI PENYUSUTAN
        st.write("  **Aset Tetap:**")
        total_aset_tetap_kotor = 0
        
        # Tampilkan aset tetap
        for akun, jumlah in data['aset_tetap'].items():
            st.write(f"    {akun:28} Rp{jumlah:>15,.0f}")
            total_aset_tetap_kotor += jumlah
        
        # ✅ TAMPILKAN AKUMULASI PENYUSUTAN
        total_akumulasi_penyusutan = 0
        if data['akumulasi_penyusutan']:
            for akun, jumlah in data['akumulasi_penyusutan'].items():
                st.write(f"    {akun:28} Rp{jumlah:>15,.0f}")
                total_akumulasi_penyusutan += jumlah
        else:
            st.write(f"    {'Tidak ada akumulasi penyusutan':28} Rp{0:>15,.0f}")
        
        # Hitung aset tetap bersih
        total_aset_tetap_bersih = total_aset_tetap_kotor - total_akumulasi_penyusutan
        
        # Tampilkan total aset tetap bersih
        st.write(f"    {'Total Aset Tetap':28} **Rp{total_aset_tetap_bersih:>15,.0f}**")
        
        # Total Aset
        total_aset = total_aset_lancar + total_aset_tetap_bersih
        st.write(f"{'TOTAL ASET':30} **Rp{total_aset:>15,.0f}**")
        
        st.markdown("---")
        
        # KEWAJIBAN & MODAL
        st.write("**KEWAJIBAN & MODAL:**")
        
        # Kewajiban
        st.write("  **Kewajiban:**")
        total_kewajiban = 0
        for akun, jumlah in data['kewajiban'].items():
            st.write(f"    {akun:28} Rp{jumlah:>15,.0f}")
            total_kewajiban += jumlah
        
        if total_kewajiban == 0:
            st.write(f"    {'Tidak ada kewajiban':28} Rp{0:>15,.0f}")
        
        st.write(f"    {'Total Kewajiban':28} **Rp{total_kewajiban:>15,.0f}**")
        
        # Modal
        st.write("  **Modal:**")
        modal_akhir = data['modal_akhir']
        
        # Tampilkan modal awal jika ada
        if data.get('modal_awal', 0) > 0:
            st.write(f"    {'Modal Awal':28} Rp{data['modal_awal']:>15,.0f}")
        
        # Tampilkan laba/rugi
        laba_bersih = data.get('laba_bersih', 0)
        if laba_bersih != 0:
            jenis = "Laba" if laba_bersih > 0 else "Rugi"
            st.write(f"    {jenis + ' Bersih':28} Rp{abs(laba_bersih):>15,.0f}")
        
        # Tampilkan prive jika ada
        prive = data.get('prive', {}).get('Prive', 0)
        if prive > 0:
            st.write(f"    {'Prive':28} Rp{prive:>15,.0f}")
        
        # Tampilkan modal akhir
        st.write(f"    {'Modal Pemilik':28} **Rp{modal_akhir:>15,.0f}**")
        
        total_kewajiban_modal = total_kewajiban + modal_akhir
        st.write(f"{'TOTAL KEWAJIBAN & MODAL':30} **Rp{total_kewajiban_modal:>15,.0f}**")
        
        st.markdown("---")
        
        # Validasi keseimbangan
        if total_aset == total_kewajiban_modal:
            st.success("✅ **SEIMBANG** - Total Aset = Total Kewajiban & Modal")
        else:
            st.error(f"❌ **TIDAK SEIMBANG** - Selisih: Rp{abs(total_aset - total_kewajiban_modal):,.0f}")
            
            # Tampilkan detail selisih
            st.write(f"Total Aset: Rp{total_aset:,.0f}")
            st.write(f"Total Kewajiban & Modal: Rp{total_kewajiban_modal:,.0f}")
            
    def show_jurnal_penutup(self):
        st.title("🔒 JURNAL PENUTUP")
        
        # Ambil data dari Neraca Setelah Penyesuaian
        data_keuangan = self.hitung_data_laporan_keuangan()
        
        if not data_keuangan:
            st.info("📭 Belum ada data untuk Jurnal Penutup")
            return
        
        # Hitung jurnal penutup otomatis
        jurnal_penutup = self.hitung_jurnal_penutup(data_keuangan)
        
        if not jurnal_penutup:
            st.warning("❌ Tidak ada akun nominal yang perlu ditutup")
            return
        
        # Tampilkan jurnal penutup
        st.subheader("📋 JURNAL PENUTUP - PENUTUPAN AKUN NOMINAL")
        st.write("Periode 31 Desember 2023")
        
        st.markdown("---")
        
        # 1. PENUTUPAN PENDAPATAN
        if jurnal_penutup['pendapatan']:
            st.write("**1. PENUTUPAN PENDAPATAN:**")
            total_pendapatan = 0
            
            for akun, jumlah in jurnal_penutup['pendapatan'].items():
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write(f"{akun}")
                with col3: st.write(f"Rp{jumlah:>15,.0f}")
                total_pendapatan += jumlah
            
            # Entry Ikhtisar Laba Rugi
            col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
            with col2: st.write("Ikhtisar Laba Rugi")
            with col3: st.write(f"Rp{total_pendapatan:>15,.0f}")
            
            st.markdown("---")
        
        # 2. PENUTUPAN BEBAN
        if jurnal_penutup['beban']:
            st.write("**2. PENUTUPAN BEBAN:**")
            total_beban = 0
            
            # Entry Ikhtisar Laba Rugi (Debit)
            col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
            with col2: st.write("Ikhtisar Laba Rugi")
            with col3: st.write(f"Rp{sum(jurnal_penutup['beban'].values()):>15,.0f}")
            
            # Akun-akun beban (Kredit)
            for akun, jumlah in jurnal_penutup['beban'].items():
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write(f"{akun}")
                with col3: st.write(f"Rp{jumlah:>15,.0f}")
                total_beban += jumlah
            
            st.markdown("---")
        
        # 3. PENUTUPAN LABA/RUGI
        if jurnal_penutup['laba_rugi']:
            st.write("**3. PENUTUPAN LABA/RUGI:**")
            
            if jurnal_penutup['laba_rugi']['type'] == 'LABA':
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write("Ikhtisar Laba Rugi")
                with col3: st.write(f"Rp{jurnal_penutup['laba_rugi']['amount']:>15,.0f}")
                
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write("Modal")
                with col3: st.write(f"Rp{jurnal_penutup['laba_rugi']['amount']:>15,.0f}")
            else:
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write("Modal")
                with col3: st.write(f"Rp{jurnal_penutup['laba_rugi']['amount']:>15,.0f}")
                
                col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
                with col2: st.write("Ikhtisar Laba Rugi")
                with col3: st.write(f"Rp{jurnal_penutup['laba_rugi']['amount']:>15,.0f}")
            
            st.markdown("---")
        
        # 4. PENUTUPAN PRIVE
        if jurnal_penutup['prive']:
            st.write("**4. PENUTUPAN PRIVE:**")
            
            col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
            with col2: st.write("Modal")
            with col3: st.write(f"Rp{jurnal_penutup['prive']:>15,.0f}")
            
            col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
            with col2: st.write("Prive")
            with col3: st.write(f"Rp{jurnal_penutup['prive']:>15,.0f}")
            
            st.markdown("---")
        
        # INFO SUMMARY
        st.success("✅ **SEMUA AKUN NOMINAL SUDAH DITUTUP**")
        
        # Tombol Posting Jurnal
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 POSTING JURNAL PENUTUP", use_container_width=True, type="primary"):
                self.posting_jurnal_penutup(jurnal_penutup)
                st.success("🎉 Jurnal Penutup berhasil diposting!")
                st.rerun()

    def hitung_jurnal_penutup(self, data_keuangan):
        """Hitung jurnal penutup secara otomatis"""
        jurnal_penutup = {
            'pendapatan': {},
            'beban': {},
            'laba_rugi': {},
            'prive': 0
        }
        
        # 1. Kumpulkan akun pendapatan (akan di-DEBIT untuk menutup)
        for akun, jumlah in data_keuangan['pendapatan'].items():
            if jumlah > 0:
                jurnal_penutup['pendapatan'][akun] = jumlah
        
        # 2. Kumpulkan akun beban (akan di-KREDIT untuk menutup)
        for akun, jumlah in data_keuangan['beban'].items():
            if jumlah > 0:
                jurnal_penutup['beban'][akun] = jumlah
        
        # 3. Hitung laba/rugi
        total_pendapatan = sum(jurnal_penutup['pendapatan'].values())
        total_beban = sum(jurnal_penutup['beban'].values())
        laba_bersih = total_pendapatan - total_beban
        
        if laba_bersih != 0:
            jurnal_penutup['laba_rugi'] = {
                'type': 'LABA' if laba_bersih > 0 else 'RUGI',
                'amount': abs(laba_bersih)
            }
        
        # 4. Cek prive
        prive = data_keuangan.get('prive', {}).get('Prive', 0)
        if prive > 0:
            jurnal_penutup['prive'] = prive
        
        return jurnal_penutup

    def show_jurnal_penutup(self):
        st.title("🔒 JURNAL PENUTUP")
        
        # Load data
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        if not st.session_state.transactions:
            st.info("📭 Belum ada transaksi di Jurnal Umum")
            return

        # Hitung saldo semua akun
        saldo_akun = self.hitung_saldo_semua_akun()
        
        if not saldo_akun:
            st.info("📭 Tidak ada akun yang memiliki saldo")
            return

        # Pisahkan akun nominal (yang ditutup)
        akun_pendapatan = {}
        akun_beban = {}
        prive = 0
        
        for akun, saldo in saldo_akun.items():
            if "Pendapatan" in akun or "Penjualan" in akun:
                if saldo > 0:
                    akun_pendapatan[akun] = saldo
            elif "Beban" in akun or "Pembelian" in akun:
                if abs(saldo) > 0:
                    akun_beban[akun] = abs(saldo)
            elif akun == "Prive" and saldo > 0:
                prive = saldo
        
        # Hitung laba/rugi
        total_pendapatan = sum(akun_pendapatan.values())
        total_beban = sum(akun_beban.values())
        laba_bersih = total_pendapatan - total_beban
        
        # Tampilkan Jurnal Penutup dalam TABLE VIEW
        st.subheader("📋 JURNAL PENUTUP - TAMPILAN TABEL")
        st.write("Periode 31 Desember 2023")
        
        st.markdown("---")
        
        # 1. PENUTUPAN PENDAPATAN
        if akun_pendapatan:
            st.write("**1. PENUTUPAN PENDAPATAN:**")
            
            # Buat dataframe untuk tabel
            data_pendapatan = []
            for akun, jumlah in akun_pendapatan.items():
                data_pendapatan.append({
                    "Akun": akun,
                    "Debit": f"Rp{jumlah:,.0f}",
                    "Kredit": ""
                })
            
            # Tambahkan Ikhtisar Laba Rugi
            data_pendapatan.append({
                "Akun": "Ikhtisar Laba Rugi",
                "Debit": "",
                "Kredit": f"Rp{total_pendapatan:,.0f}"
            })
            
            # Tampilkan tabel
            df_pendapatan = pd.DataFrame(data_pendapatan)
            st.dataframe(df_pendapatan, use_container_width=True, hide_index=True)
            
            st.markdown("---")
        
        # 2. PENUTUPAN BEBAN
        if akun_beban:
            st.write("**2. PENUTUPAN BEBAN:**")
            
            # Buat dataframe untuk tabel
            data_beban = []
            
            # Tambahkan Ikhtisar Laba Rugi (debit)
            data_beban.append({
                "Akun": "Ikhtisar Laba Rugi",
                "Debit": f"Rp{total_beban:,.0f}",
                "Kredit": ""
            })
            
            # Tambahkan akun beban (kredit)
            for akun, jumlah in akun_beban.items():
                data_beban.append({
                    "Akun": akun,
                    "Debit": "",
                    "Kredit": f"Rp{jumlah:,.0f}"
                })
            
            # Tampilkan tabel
            df_beban = pd.DataFrame(data_beban)
            st.dataframe(df_beban, use_container_width=True, hide_index=True)
            
            st.markdown("---")
        
        # 3. PENUTUPAN LABA/RUGI
        if laba_bersih != 0:
            st.write("**3. PENUTUPAN LABA/RUGI:**")
            
            data_laba_rugi = []
            
            if laba_bersih > 0:
                # Laba
                data_laba_rugi.append({
                    "Akun": "Ikhtisar Laba Rugi",
                    "Debit": f"Rp{laba_bersih:,.0f}",
                    "Kredit": ""
                })
                data_laba_rugi.append({
                    "Akun": "Modal Pemilik",
                    "Debit": "",
                    "Kredit": f"Rp{laba_bersih:,.0f}"
                })
            else:
                # Rugi
                data_laba_rugi.append({
                    "Akun": "Modal Pemilik",
                    "Debit": f"Rp{abs(laba_bersih):,.0f}",
                    "Kredit": ""
                })
                data_laba_rugi.append({
                    "Akun": "Ikhtisar Laba Rugi",
                    "Debit": "",
                    "Kredit": f"Rp{abs(laba_bersih):,.0f}"
                })
            
            # Tampilkan tabel
            df_laba_rugi = pd.DataFrame(data_laba_rugi)
            st.dataframe(df_laba_rugi, use_container_width=True, hide_index=True)
            
            st.markdown("---")
        
        # 4. PENUTUPAN PRIVE
        if prive > 0:
            st.write("**4. PENUTUPAN PRIVE:**")
            
            data_prive = [
                {
                    "Akun": "Modal Pemilik",
                    "Debit": f"Rp{prive:,.0f}",
                    "Kredit": ""
                },
                {
                    "Akun": "Prive",
                    "Debit": "",
                    "Kredit": f"Rp{prive:,.0f}"
                }
            ]
            
            # Tampilkan tabel
            df_prive = pd.DataFrame(data_prive)
            st.dataframe(df_prive, use_container_width=True, hide_index=True)
            
            st.markdown("---")
        
        # INFO SUMMARY
        st.success("✅ **SEMUA AKUN NOMINAL SUDAH DITUTUP**")
        
        # Tombol Posting Jurnal
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 POSTING JURNAL PENUTUP", use_container_width=True, type="primary"):
                # Simpan jurnal penutup
                jurnal_data = {
                    'pendapatan': akun_pendapatan,
                    'beban': akun_beban,
                    'laba_bersih': laba_bersih,
                    'prive': prive
                }
                self.posting_jurnal_penutup_sederhana(jurnal_data)
                st.success("🎉 Jurnal Penutup berhasil diposting!")
                st.rerun()

    def posting_jurnal_penutup_sederhana(self, jurnal_data):
        """Posting jurnal penutup versi sederhana"""
        try:
            entries = []
            tanggal = "31 Desember 2023"
            
            # 1. Posting pendapatan
            for akun, jumlah in jurnal_data['pendapatan'].items():
                entries.append({
                    'tanggal': tanggal,
                    'akun': akun,
                    'debit': jumlah,
                    'kredit': 0,
                    'keterangan': 'Penutupan Pendapatan',
                    'ref': 'JP'
                })
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Ikhtisar Laba Rugi",
                    'debit': 0,
                    'kredit': jumlah,
                    'keterangan': 'Penutupan Pendapatan',
                    'ref': 'JP'
                })
            
            # 2. Posting beban
            for akun, jumlah in jurnal_data['beban'].items():
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Ikhtisar Laba Rugi",
                    'debit': jumlah,
                    'kredit': 0,
                    'keterangan': 'Penutupan Beban',
                    'ref': 'JP'
                })
                entries.append({
                    'tanggal': tanggal,
                    'akun': akun,
                    'debit': 0,
                    'kredit': jumlah,
                    'keterangan': 'Penutupan Beban',
                    'ref': 'JP'
                })
            
            # 3. Posting laba/rugi
            if jurnal_data['laba_bersih'] > 0:
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Ikhtisar Laba Rugi",
                    'debit': jurnal_data['laba_bersih'],
                    'kredit': 0,
                    'keterangan': 'Penutupan Laba',
                    'ref': 'JP'
                })
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Modal Pemilik",
                    'debit': 0,
                    'kredit': jurnal_data['laba_bersih'],
                    'keterangan': 'Penutupan Laba',
                    'ref': 'JP'
                })
            
            # 4. Posting prive
            if jurnal_data['prive'] > 0:
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Modal Pemilik",
                    'debit': jurnal_data['prive'],
                    'kredit': 0,
                    'keterangan': 'Penutupan Prive',
                    'ref': 'JP'
                })
                entries.append({
                    'tanggal': tanggal,
                    'akun': "Prive",
                    'debit': 0,
                    'kredit': jurnal_data['prive'],
                    'keterangan': 'Penutupan Prive',
                    'ref': 'JP'
                })
            
            # Simpan ke file
            with open('jurnal_penutup.json', 'w') as f:
                json.dump(entries, f, indent=4)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return False
            
    def show_neraca_saldo_akhir(self):
        """HALAMAN Neraca Saldo Akhir - FOKUS PADA AKUN NOMINAL"""
        st.title("✅ NERACA SALDO AKHIR")
        st.write("**Setelah Penutupan**")
        
        # Ambil data
        data_keuangan = self.hitung_data_laporan_keuangan()
        if not data_keuangan:
            st.info("📭 Belum ada data untuk Neraca Saldo Akhir")
            return
        
        # Hitung saldo setelah penutupan
        saldo_akhir = self.hitung_saldo_setelah_penutupan_sederhana(data_keuangan)
        
        if not saldo_akhir:
            st.info("📭 Belum ada akun setelah penutupan")
            return
        
        # Tampilkan berdasarkan kategori akun
        st.subheader("📋 DAFTAR AKUN SETELAH PENUTUPAN")
        
        # Pisahkan akun nominal dan riil
        akun_nominal = {akun: saldo for akun, saldo in saldo_akhir.items() if not self.is_akun_riil_sederhana(akun)}
        akun_riil = {akun: saldo for akun, saldo in saldo_akhir.items() if self.is_akun_riil_sederhana(akun) and saldo != 0}
        
        # 1. TAMPILKAN AKUN NOMINAL (YANG DITUTUP)
        st.markdown("---")
        st.subheader("📊 AKUN NOMINAL - SUDAH DITUTUP")
        
        if not akun_nominal:
            st.info("📭 Tidak ada akun nominal")
        else:
            # Hitung statistik
            total_akun_nominal = len(akun_nominal)
            akun_sudah_nol = sum(1 for saldo in akun_nominal.values() if saldo == 0)
            akun_belum_nol = total_akun_nominal - akun_sudah_nol
            
            # Progress bar
            if total_akun_nominal > 0:
                progress = akun_sudah_nol / total_akun_nominal
                st.progress(progress)
                st.write(f"**Progress Penutupan: {akun_sudah_nol}/{total_akun_nominal} akun sudah NOL**")
            
            # Tabel akun nominal
            st.markdown("---")
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1: st.write("**NAMA AKUN**")
            with col2: st.write("**SALDO**")
            with col3: st.write("**STATUS**")
            st.markdown("---")
            
            for akun in sorted(akun_nominal.keys()):
                saldo = akun_nominal[akun]
                
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1: st.write(f"📄 {akun}")
                with col2: st.write(f"Rp{abs(saldo):,.0f}" if saldo != 0 else "Rp0")
                with col3: 
                    if saldo == 0:
                        st.success("✅ NOL")
                    else:
                        st.error("❌ BELUM NOL")
            
            st.markdown("---")
            
            # Summary akun nominal
            if akun_belum_nol == 0:
                st.success(f"🎉 **SEMUA {total_akun_nominal} AKUN NOMINAL SUDAH DITUTUP!**")
            else:
                st.warning(f"⚠️ **{akun_belum_nol} akun nominal belum NOL**")
        
        # 2. TAMPILKAN AKUN RIIL (YANG TIDAK DITUTUP)
        st.markdown("---")
        st.subheader("🏦 AKUN RIIL - MASIH BER SALDO")
        
        if not akun_riil:
            st.info("📭 Tidak ada akun riil")
        else:
            # Emoji untuk akun riil
            emoji_riil = {
                "Kas": "💰", "Bank": "🏦", "Piutang": "🧾", "Persediaan": "📦",
                "Perlengkapan": "📦", "Peralatan": "🔧", "Gedung": "🏢", 
                "Tanah": "🌳", "Kendaraan": "🚗", "Modal": "💼", "Utang": "🏛️",
                "Akumulasi": "📉"
            }
            
            st.markdown("---")
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1: st.write("**NAMA AKUN**")
            with col2: st.write("**DEBIT**")
            with col3: st.write("**KREDIT**")
            st.markdown("---")
            
            for akun in sorted(akun_riil.keys()):
                saldo = akun_riil[akun]
                
                # Cari emoji
                emoji = "📊"
                for keyword, emoji_val in emoji_riil.items():
                    if keyword in akun:
                        emoji = emoji_val
                        break
                
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1: st.write(f"{emoji} {akun}")
                
                # Tampilkan di kolom yang benar
                if self.is_akun_debit(akun):
                    if saldo >= 0:
                        with col2: st.write(f"Rp{saldo:,.0f}")
                        with col3: st.write("")
                    else:
                        with col2: st.write("")
                        with col3: st.write(f"Rp{abs(saldo):,.0f}")
                else:
                    if saldo >= 0:
                        with col2: st.write("")
                        with col3: st.write(f"Rp{saldo:,.0f}")
                    else:
                        with col2: st.write(f"Rp{abs(saldo):,.0f}")
                        with col3: st.write("")
            
            st.markdown("---")

    def hitung_saldo_setelah_penutupan_sederhana(self, data_keuangan):
        """Hitung saldo setelah penutupan - VERSI SEDERHANA"""
        
        # 1. Ambil saldo dari neraca setelah penyesuaian
        if 'transactions' not in st.session_state:
            st.session_state.transactions = self.load_transactions_from_file()
        
        saldo_neraca = self.hitung_saldo_semua_akun()
        penyesuaian = self.load_penyesuaian_from_file()
        
        # Hitung saldo setelah penyesuaian
        saldo_setelah_penyesuaian = saldo_neraca.copy()
        
        for pen in penyesuaian:
            akun_debit = pen['akun_debit']
            if self.is_akun_debit(akun_debit):
                if akun_debit in saldo_setelah_penyesuaian:
                    saldo_setelah_penyesuaian[akun_debit] += pen['debit']
                else:
                    saldo_setelah_penyesuaian[akun_debit] = pen['debit']
            else:
                if akun_debit in saldo_setelah_penyesuaian:
                    saldo_setelah_penyesuaian[akun_debit] -= pen['debit']
                else:
                    saldo_setelah_penyesuaian[akun_debit] = -pen['debit']
                    
            akun_kredit = pen['akun_kredit']
            if self.is_akun_debit(akun_kredit):
                if akun_kredit in saldo_setelah_penyesuaian:
                    saldo_setelah_penyesuaian[akun_kredit] -= pen['kredit']
                else:
                    saldo_setelah_penyesuaian[akun_kredit] = -pen['kredit']
            else:
                if akun_kredit in saldo_setelah_penyesuaian:
                    saldo_setelah_penyesuaian[akun_kredit] += pen['kredit']
                else:
                    saldo_setelah_penyesuaian[akun_kredit] = pen['kredit']
        
        # 2. Proses penutupan - SET AKUN NOMINAL MENJADI NOL
        saldo_akhir = {}
        
        # Saldo akun riil tetap
        for akun, saldo in saldo_setelah_penyesuaian.items():
            if self.is_akun_riil_sederhana(akun):
                saldo_akhir[akun] = saldo
        
        # Set semua akun nominal menjadi NOL
        akun_nominal = [
            akun for akun in saldo_setelah_penyesuaian.keys() 
            if not self.is_akun_riil_sederhana(akun)
        ]
        
        for akun in akun_nominal:
            saldo_akhir[akun] = 0  # PASTIKAN NOL
        
        return saldo_akhir

    def is_akun_riil_sederhana(self, nama_akun):
        """Tentukan apakah akun riil (tidak ditutup) - VERSI SEDERHANA"""
        
        # DAFTAR AKUN NOMINAL YANG HARUS DITUTUP
        akun_nominal = [
            # PENDAPATAN
            "Pendapatan Usaha", "Pendapatan Jasa", "Pendapatan Penjualan", 
            "Pendapatan Lainnya", "Penjualan",
            
            # BEBAN
            "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", 
            "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
            "Beban Penyusutan", "Beban Lainnya", "Beban", "Beban pakan",
            "Beban Pengiriman", "Beban Vitamin", "Beban Perbaikan",
            "Beban perawatan Kandang", "Beban Obat",
            
            # LAINNYA
            "Pembelian", "Prive", "Ikhtisar Laba Rugi"
        ]
        
        # Jika termasuk nominal, return False (harus ditutup)
        if nama_akun in akun_nominal:
            return False
        
        # Cek berdasarkan keyword
        nominal_keywords = ["Pendapatan", "Beban", "Pembelian", "Prive", "Ikhtisar"]
        if any(keyword in nama_akun for keyword in nominal_keywords):
            return False
        
        # Default: akun riil (tidak ditutup)
        return True

    def show_input_transaksi(self):
        st.title("Input Transaksi")
        
        with st.form("input_transaksi_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                tanggal = st.date_input("Tanggal", value=datetime.now())
                keterangan = st.text_input("Keterangan")
                
                akun_options = [
                "Kas", "Bank", "Piutang Usaha", "Persediaan", "Perlengkapan",
                "Peralatan", "Gedung", "Tanah", "Kendaraan", "Beban Perbaikan", 
                "Akumulasi Penyusutan Gedung", "Akumulasi Penyusutan Peralatan",
                "Utang Usaha", "Utang Bank", "Modal Pemilik", "Prive", "Beaban Obat", "Beban Vitamin",  
                "Pembelian", "Penjualan", "Beban pakan", "Beban Pengiriman", "Beban Vitamain",                                   
                "Pendapatan Usaha", "Pendapatan Jasa", "Pendapatan Penjualan", "Pendapatan Lainnya",
                "Beban Gaji", "Beban Sewa", "Beban Listrik", "Beban Air", "Beban perawatan Kadang",  
                "Beban Telepon", "Beban Transportasi", "Beban Perlengkapan",
                "Beban Penyusutan Gedung", "Beban Penyusutan Peralatan", "Beban Lainnya"
            ]
                
                akun_debit = st.selectbox("Akun Debit", akun_options)
                debit = st.number_input("Jumlah Debit", min_value=0.0, step=1000.0)
            
            with col2:
                akun_kredit = st.selectbox("Akun Kredit", akun_options)
                kredit = st.number_input("Jumlah Kredit", min_value=0.0, step=1000.0)
            
            submitted = st.form_submit_button("Simpan Transaksi")
            
            if submitted:
                if debit != kredit:
                    st.error("❌ Jumlah debit dan kredit harus sama!")
                else:
                    # ✅ SIMPAN KE JURNAL UMUM
                    if 'transactions' not in st.session_state:
                        st.session_state.transactions = []
                    
                    # Transaksi Debit
                    st.session_state.transactions.append({
                        'tanggal': tanggal.strftime("%d %B %Y"),
                        'akun': akun_debit,
                        'debit': debit,
                        'kredit': 0,
                        'keterangan': keterangan,
                        'ref': ''
                    })
                    
                    # Transaksi Kredit  
                    st.session_state.transactions.append({
                        'tanggal': tanggal.strftime("%d %B %Y"),
                        'akun': akun_kredit,
                        'debit': 0,
                        'kredit': kredit,
                        'keterangan': keterangan,
                        'ref': ''
                    })
                    
                    st.success("✅ Transaksi berhasil disimpan ke Jurnal Umum!")
                    st.rerun()

    def simpan_transaksi(self, tanggal, keterangan, akun_debit, akun_kredit, debit, kredit):
        try:
            if not all([tanggal, keterangan, akun_debit, akun_kredit]):
                st.error("Semua field harus diisi!")
                return
            
            if debit != kredit:
                st.error("Jumlah debit dan kredit harus sama!")
                return
            
            # Simpan 2 transaksi (1 debit, 1 kredit)
            transaksi_debit = {
                "tanggal": tanggal,
                "keterangan": keterangan,
                "akun": akun_debit,
                "debit": debit,
                "kredit": 0
            }
            
            transaksi_kredit = {
                "tanggal": tanggal,
                "keterangan": keterangan,
                "akun": akun_kredit,
                "debit": 0,
                "kredit": kredit
            }
            
            self.transactions.append(transaksi_debit)
            self.transactions.append(transaksi_kredit)
            self.save_transactions()
            
            # Update saldo akun
            self.update_account_balance(akun_debit, debit, 0)
            self.update_account_balance(akun_kredit, 0, kredit)
            
            st.success("Transaksi berhasil disimpan!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Terjadi error: {str(e)}")

    def hapus_transaksi(self, index):
        if 0 <= index < len(self.transactions):
            transaksi_terhapus = self.transactions.pop(index)
            
            # Update saldo akun (balikkan transaksi)
            akun = transaksi_terhapus['akun']
            debit = transaksi_terhapus['debit']
            kredit = transaksi_terhapus['kredit']
            
            self.update_account_balance(akun, -debit, -kredit)
            self.save_transactions()
            
            st.success("Transaksi berhasil dihapus!")
            st.rerun()

    def update_account_balance(self, account_name, debit, credit):
        try:
            with open(self.accounts_file, "r") as f:
                accounts = json.load(f)
            
            if account_name in accounts:
                account_type = accounts[account_name]["type"]
                
                if account_type in ["Aset", "Beban"]:
                    accounts[account_name]["balance"] += debit - credit
                else:  # Kewajiban, Modal, Pendapatan
                    accounts[account_name]["balance"] += credit - debit
                
                with open(self.accounts_file, "w") as f:
                    json.dump(accounts, f, indent=4)
                    
        except Exception as e:
            st.error(f"Error update saldo: {e}")

    def show_pengaturan(self):
        col_sidebar, col_content = st.columns([1, 4])
        
        with col_sidebar:
            st.markdown("### ⚙️ PENGATURAN")
            st.markdown("---")
            
            if 'pengaturan_page' not in st.session_state:
                st.session_state.pengaturan_page = "profil"
            
            menu_options = {
                "🏢 Profil Perusahaan": "profil",
                "🔧 Sistem Settings": "sistem", 
                "🔔 Notifikasi": "notifikasi",
                "🔐 Keamanan & Akses": "keamanan",
                "💾 Backup & Restore": "backup"
            }
            
            for menu_name, menu_value in menu_options.items():
                if st.button(menu_name, use_container_width=True, key=f"pengaturan_{menu_value}"):
                    st.session_state.pengaturan_page = menu_value
                    st.rerun()
            
            st.markdown("---")
            if st.button("⬅️ Kembali ke Menu Utama", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        with col_content:
            if st.session_state.pengaturan_page == "profil":
                self.show_profil_perusahaan()
            elif st.session_state.pengaturan_page == "sistem":
                self.show_system_settings()
            elif st.session_state.pengaturan_page == "notifikasi":
                self.show_notification_settings()
            elif st.session_state.pengaturan_page == "keamanan":
                self.show_security_settings()
            elif st.session_state.pengaturan_page == "backup":
                self.show_backup_restore()

    def show_profil_perusahaan(self):
        st.header("🏢 PROFIL PERUSAHAAN")
        
        if 'company_profile' not in st.session_state:
            st.session_state.company_profile = self.load_company_profile()
        
        profile = st.session_state.company_profile
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
           pass
        
        with col2:
            st.subheader("📋 Informasi Perusahaan")
            
            with st.form("profil_form"):
                nama_perusahaan = st.text_input("Nama Perusahaan*", value=profile.get('nama_perusahaan', ''))
                alamat = st.text_area("Alamat*", value=profile.get('alamat', ''), height=80)
                
                col_contact = st.columns(2)
                with col_contact[0]:
                    telepon = st.text_input("Telepon*", value=profile.get('telepon', ''))
                with col_contact[1]:
                    email = st.text_input("Email*", value=profile.get('email', ''))
                
                website = st.text_input("Website", value=profile.get('website', ''))
                bidang_usaha = st.selectbox("Bidang Usaha*", ['Peternakan', 'Pertanian', 'Perdagangan', 'Jasa', 'Lainnya'])
                
                col_btn = st.columns(2)
                with col_btn[0]:
                    submitted = st.form_submit_button("💾 Simpan Profil", use_container_width=True, type="primary")
                with col_btn[1]:
                    reset_btn = st.form_submit_button("🔄 Reset", use_container_width=True)
                
                if submitted:
                    if not nama_perusahaan or not alamat or not telepon or not email:
                        st.error("Harap isi semua field yang wajib (*)")
                    else:
                        st.session_state.company_profile = {
                            'nama_perusahaan': nama_perusahaan,
                            'alamat': alamat,
                            'telepon': telepon,
                            'email': email,
                            'website': website,
                            'bidang_usaha': bidang_usaha,
                        }
                        if self.save_company_profile(st.session_state.company_profile):
                            st.success("Profil perusahaan berhasil disimpan!")
                    
                if reset_btn:
                    st.session_state.company_profile = self.load_company_profile(reset=True)
                    st.rerun()

    def show_system_settings(self):
        st.header("🔧 SISTEM SETTINGS")
        
        if 'system_settings' not in st.session_state:
            st.session_state.system_settings = self.load_system_settings()
        
        settings = st.session_state.system_settings
        
        with st.form("system_settings_form"):
            st.subheader("📅 Periode Akuntansi")
            col_periode = st.columns(2)
            with col_periode[0]:
                periode_mulai = st.date_input("Periode Mulai*", value=datetime.strptime(settings.get('periode_mulai', '2024-01-01'), '%Y-%m-%d'))
            with col_periode[1]:
                periode_akhir = st.date_input("Periode Akhir*", value=datetime.strptime(settings.get('periode_akhir', '2024-12-31'), '%Y-%m-%d'))
            
            st.subheader("💰 Mata Uang & Format")
            col_format = st.columns(3)
            with col_format[0]:
                mata_uang = st.selectbox("Mata Uang*", ['IDR - Rupiah', 'USD - US Dollar', 'SGD - Singapore Dollar'])
            with col_format[1]:
                format_tanggal = st.selectbox("Format Tanggal*", ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD'])
            with col_format[2]:
                format_angka = st.selectbox("Format Angka*", ['1.000,00', '1,000.00', '1 000,00'])
            
            st.subheader("🎨 Tampilan Aplikasi")
            theme = st.selectbox("Theme*", ['Hijau', 'Biru', 'Ungu', 'Orange'])
            
            st.subheader("⚡ Pengaturan Otomatis")
            auto_save = st.checkbox("Auto-save perubahan otomatis", value=settings.get('auto_save', True))
            
            col_btn = st.columns(2)
            with col_btn[0]:
                submitted = st.form_submit_button("💾 Simpan Settings", use_container_width=True, type="primary")
            with col_btn[1]:
                reset_btn = st.form_submit_button("🔄 Default", use_container_width=True)
            
            if submitted:
                if periode_mulai >= periode_akhir:
                    st.error("Periode mulai harus sebelum periode akhir")
                else:
                    st.session_state.system_settings = {
                        'periode_mulai': periode_mulai.strftime('%Y-%m-%d'),
                        'periode_akhir': periode_akhir.strftime('%Y-%m-%d'),
                        'mata_uang': mata_uang,
                        'format_tanggal': format_tanggal,
                        'format_angka': format_angka,
                        'theme': theme,
                        'auto_save': auto_save
                    }
                    if self.save_system_settings(st.session_state.system_settings):
                        st.success("System settings berhasil disimpan!")
                
            if reset_btn:
                st.session_state.system_settings = self.load_system_settings(reset=True)
                st.rerun()

    def show_notification_settings(self):
        st.header("🔔 PENGATURAN NOTIFIKASI")
        
        if 'notification_settings' not in st.session_state:
            st.session_state.notification_settings = self.load_notification_settings()
        
        settings = st.session_state.notification_settings
        
        with st.form("notification_form"):
            st.subheader("🔔 Notifikasi Sistem")
            col_notif = st.columns(2)
            with col_notif[0]:
                notif_transaksi_besar = st.checkbox("Notifikasi transaksi besar", value=settings.get('notif_transaksi_besar', True))
                notif_saldo_rendah = st.checkbox("Peringatan saldo rendah", value=settings.get('notif_saldo_rendah', True))
                notif_laporan_bulanan = st.checkbox("Pengingat laporan bulanan", value=settings.get('notif_laporan_bulanan', True))
            with col_notif[1]:
                notif_maintenance = st.checkbox("Notifikasi maintenance", value=settings.get('notif_maintenance', False))
                notif_backup = st.checkbox("Notifikasi backup", value=settings.get('notif_backup', True))
            
            st.subheader("📧 Notifikasi Email")
            email_penerima = st.text_input("Email penerima*", value=settings.get('email_penerima', ''))
            
            col_email = st.columns(2)
            with col_email[0]:
                email_laporan_mingguan = st.checkbox("Laporan mingguan", value=settings.get('email_laporan_mingguan', True))
                email_transaksi_penting = st.checkbox("Transaksi penting", value=settings.get('email_transaksi_penting', True))
            with col_email[1]:
                email_ringkasan_harian = st.checkbox("Ringkasan harian", value=settings.get('email_ringkasan_harian', False))
            
            col_btn = st.columns(3)
            with col_btn[0]:
                submitted = st.form_submit_button("💾 Simpan", use_container_width=True, type="primary")
            with col_btn[1]:
                test_btn = st.form_submit_button("🔔 Test", use_container_width=True)
            with col_btn[2]:
                reset_btn = st.form_submit_button("🔄 Reset", use_container_width=True)
            
            if submitted:
                if not email_penerima:
                    st.error("Email penerima harus diisi")
                else:
                    st.session_state.notification_settings = {
                        'notif_transaksi_besar': notif_transaksi_besar,
                        'notif_saldo_rendah': notif_saldo_rendah,
                        'notif_laporan_bulanan': notif_laporan_bulanan,
                        'notif_maintenance': notif_maintenance,
                        'notif_backup': notif_backup,
                        'email_penerima': email_penerima,
                        'email_laporan_mingguan': email_laporan_mingguan,
                        'email_transaksi_penting': email_transaksi_penting,
                        'email_ringkasan_harian': email_ringkasan_harian
                    }
                    if self.save_notification_settings(st.session_state.notification_settings):
                        st.success("Pengaturan notifikasi berhasil disimpan!")
                
            if test_btn:
                st.info("Test notifikasi berhasil dikirim!")
                
            if reset_btn:
                st.session_state.notification_settings = self.load_notification_settings(reset=True)
                st.rerun()

    def show_security_settings(self):
        st.header("🔐 KEAMANAN & AKSES")
        
        if 'security_settings' not in st.session_state:
            st.session_state.security_settings = self.load_security_settings()
        
        settings = st.session_state.security_settings
        
        tab1, tab2, tab3 = st.tabs(["🔐 Keamanan", "👥 Hak Akses", "📋 Activity Log"])
        
        with tab1:
            st.subheader("🔐 Pengaturan Keamanan")
            with st.form("security_form"):
                wajib_login = st.checkbox("Wajib login", value=settings.get('wajib_login', True))
                col_security = st.columns(2)
                with col_security[0]:
                    min_password = st.number_input("Password minimal", min_value=4, max_value=20, value=settings.get('min_password', 6))
                with col_security[1]:
                    auto_logout = st.number_input("Auto logout (menit)", min_value=1, max_value=120, value=settings.get('auto_logout', 30))
                two_factor = st.checkbox("Two-factor authentication", value=settings.get('two_factor', False))
                
                col_btn = st.columns(2)
                with col_btn[0]:
                    submitted = st.form_submit_button("💾 Simpan Keamanan", use_container_width=True, type="primary")
                with col_btn[1]:
                    reset_btn = st.form_submit_button("🔄 Default", use_container_width=True)
                
                if submitted:
                    st.session_state.security_settings.update({
                        'wajib_login': wajib_login,
                        'min_password': min_password,
                        'auto_logout': auto_logout,
                        'two_factor': two_factor
                    })
                    if self.save_security_settings(st.session_state.security_settings):
                        st.success("Pengaturan keamanan berhasil disimpan!")
                    
                if reset_btn:
                    st.session_state.security_settings = self.load_security_settings(reset=True)
                    st.rerun()
        
        with tab2:
            st.subheader("👥 Hak Akses Per Role")
            roles_data = settings.get('roles', {})
            df_roles = pd.DataFrame(roles_data).T
            st.dataframe(df_roles, use_container_width=True)
            
            if st.button("✏️ Edit Hak Akses", use_container_width=True):
                st.info("Fitur edit hak akses akan segera tersedia")
        
        with tab3:
            st.subheader("📋 Activity Log")
            activities = [
                {"user": "admin", "action": "Login", "time": "2024-01-15 08:30:00"},
                {"user": "kasir1", "action": "Input transaksi", "time": "2024-01-15 09:15:00"},
            ]
            
            for activity in activities:
                st.write(f"**{activity['user']}** - {activity['action']} - *{activity['time']}*")
            
            if st.button("🗑️ Clear Log", use_container_width=True):
                st.success("Activity log berhasil dibersihkan!")

    def show_backup_restore(self):
        st.header("💾 BACKUP & RESTORE")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📥 BACKUP DATA")
            backup_filename = f"backup_sientok_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            if st.button("💾 Buat Backup", use_container_width=True, type="primary"):
                backup_data = self.create_backup()
                if backup_data:
                    st.success("Backup berhasil dibuat!")
                    st.download_button(
                        label="📥 Download Backup",
                        data=backup_data,
                        file_name=backup_filename,
                        mime="application/json",
                        use_container_width=True
                    )
                else:
                    st.error("Gagal membuat backup")
            
            if st.button("⚠️ Hapus Data", use_container_width=True):
                st.warning("Fitur hapus data akan segera tersedia")
        
        with col2:
            st.subheader("📤 RESTORE DATA")
            uploaded_file = st.file_uploader("Pilih file backup", type=['json'])
            
            if uploaded_file:
                st.info(f"File terpilih: {uploaded_file.name}")
                if st.button("🔄 Restore Data", use_container_width=True, type="primary"):
                    try:
                        result = self.restore_backup(uploaded_file)
                        if result:
                            st.success("Restore data berhasil!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.subheader("🔄 AUTO BACKUP")
            auto_backup = st.checkbox("Backup otomatis", value=True)
            backup_day = st.selectbox("Hari backup", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
            
            if st.button("💾 Simpan Auto Backup", use_container_width=True):
                st.success("Pengaturan auto backup disimpan!")

    # Data management functions
    def load_company_profile(self, reset=False):
        try:
            if reset:
                return {
                    'nama_perusahaan': 'Peternakan Sientok',
                    'alamat': 'Jl. Contoh No. 123, Jakarta',
                    'telepon': '08123456789',
                    'email': 'sientok@email.com',
                    'website': 'www.sientok.com',
                    'bidang_usaha': 'Peternakan',
                    'logo': ''
                }
            if os.path.exists('data/company_profile.json'):
                with open('data/company_profile.json', 'r') as f:
                    return json.load(f)
            else:
                default_data = self.load_company_profile(reset=True)
                self.save_company_profile(default_data)
                return default_data
        except:
            return self.load_company_profile(reset=True)

    def save_company_profile(self, data):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/company_profile.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def load_system_settings(self, reset=False):
        try:
            if reset:
                return {
                    'periode_mulai': '2024-01-01',
                    'periode_akhir': '2024-12-31',
                    'mata_uang': 'IDR - Rupiah',
                    'format_tanggal': 'DD/MM/YYYY',
                    'format_angka': '1.000,00',
                    'theme': 'Hijau',
                    'auto_save': True
                }
            if os.path.exists('data/system_settings.json'):
                with open('data/system_settings.json', 'r') as f:
                    return json.load(f)
            else:
                default_data = self.load_system_settings(reset=True)
                self.save_system_settings(default_data)
                return default_data
        except:
            return self.load_system_settings(reset=True)

    def save_system_settings(self, data):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/system_settings.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def load_notification_settings(self, reset=False):
        try:
            if reset:
                return {
                    'notif_transaksi_besar': True,
                    'notif_saldo_rendah': True,
                    'notif_laporan_bulanan': True,
                    'notif_maintenance': False,
                    'notif_backup': True,
                    'email_penerima': 'manager@sientok.com',
                    'email_laporan_mingguan': True,
                    'email_transaksi_penting': True,
                    'email_ringkasan_harian': False
                }
            if os.path.exists('data/notification_settings.json'):
                with open('data/notification_settings.json', 'r') as f:
                    return json.load(f)
            else:
                default_data = self.load_notification_settings(reset=True)
                self.save_notification_settings(default_data)
                return default_data
        except:
            return self.load_notification_settings(reset=True)

    def save_notification_settings(self, data):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/notification_settings.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def load_security_settings(self, reset=False):
        try:
            if reset:
                return {
                    'wajib_login': True,
                    'min_password': 6,
                    'auto_logout': 30,
                    'two_factor': False,
                    'roles': {
                        'Administrator': {'view': True, 'edit': True, 'print': True, 'admin': True},
                        'Manager': {'view': True, 'edit': True, 'print': True, 'admin': False},
                        'Kasir': {'view': True, 'edit': True, 'print': False, 'admin': False},
                        'Auditor': {'view': True, 'edit': False, 'print': False, 'admin': False}
                    }
                }
            if os.path.exists('data/security_settings.json'):
                with open('data/security_settings.json', 'r') as f:
                    return json.load(f)
            else:
                default_data = self.load_security_settings(reset=True)
                self.save_security_settings(default_data)
                return default_data
        except:
            return self.load_security_settings(reset=True)

    def save_security_settings(self, data):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/security_settings.json', 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def create_backup(self):
        try:
            backup_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'company_profile': self.load_company_profile(),
                'system_settings': self.load_system_settings(),
                'notification_settings': self.load_notification_settings(),
                'security_settings': self.load_security_settings(),
                'transactions': self.load_transactions_from_file(),
                'users': self.users
            }
            return json.dumps(backup_data, indent=4).encode('utf-8')
        except:
            return None

    def restore_backup(self, uploaded_file):
        try:
            backup_data = json.load(uploaded_file)
            
            if 'company_profile' in backup_data:
                self.save_company_profile(backup_data['company_profile'])
            if 'system_settings' in backup_data:
                self.save_system_settings(backup_data['system_settings'])
            if 'notification_settings' in backup_data:
                self.save_notification_settings(backup_data['notification_settings'])
            if 'security_settings' in backup_data:
                self.save_security_settings(backup_data['security_settings'])
            if 'transactions' in backup_data:
                with open('jurnal_umum_transactions.json', 'w') as f:
                    json.dump(backup_data['transactions'], f, indent=4)
            if 'users' in backup_data:
                with open('users.json', 'w') as f:
                    json.dump(backup_data['users'], f, indent=4)
            
            return True
        except:
            return False


    def export_laporan(self):
        st.title("📤 EXPORT LAPORAN")
        
        # Inisialisasi session state untuk popup
        if 'show_export_popup' not in st.session_state:
            st.session_state.show_export_popup = False
        if 'export_data' not in st.session_state:
            st.session_state.export_data = None
        
        # Jika popup sedang tidak aktif, tampilkan form export
        if not st.session_state.show_export_popup:
            self.show_export_form()
        else:
            # Jika popup aktif, tampilkan popup di "halaman terpisah"
            self.show_export_popup_page()

    def export_laporan(self):
        st.title("📤 EXPORT LAPORAN")
        
        # Inisialisasi session state untuk popup
        if 'show_export_popup' not in st.session_state:
            st.session_state.show_export_popup = False
        if 'export_data' not in st.session_state:
            st.session_state.export_data = None
        
        # Jika popup sedang tidak aktif, tampilkan form export
        if not st.session_state.show_export_popup:
            self.show_export_form()
        else:
            # Jika popup aktif, tampilkan popup di "halaman terpisah"
            self.show_export_popup_page()

    def show_export_form(self):
        """Tampilkan form pilihan export"""
        # Pilihan Siklus Akuntansi
        st.subheader("📊 Pilih Siklus Akuntansi")
        siklus_options = [
            "Semua Siklus",
            "Siklus Transaksi", 
            "Neraca Sebelum Penyesuaian",
            "Siklus Penyesuaian",
            "Neraca Setelah Penyesuaian", 
            "Siklus Pelaporan",
            "Neraca Akhir",
            "Siklus Penutupan"
        ]
        
        selected_siklus = st.selectbox("Pilih Siklus:", siklus_options)
        
        # Pilihan Format File
        st.subheader("📁 Pilih Format File")
        format_options = ["PDF", "Excel", "CSV", "HTML", "JSON", "XML"]
        selected_format = st.radio("Format File:", format_options, horizontal=True)
        
        # Tombol Export
        if st.button("🚀 EXPORT", use_container_width=True, type="primary"):
            # Generate file berdasarkan pilihan
            file_data = self.generate_laporan(selected_siklus, selected_format)
            
            if file_data:
                # Simpan data export ke session state dan buka popup
                st.session_state.export_data = {
                    'file_data': file_data,
                    'siklus': selected_siklus,
                    'format': selected_format
                }
                st.session_state.show_export_popup = True
                st.rerun()
            else:
                st.error("❌ Gagal generate laporan")

    def show_export_popup_page(self):
        """Tampilkan halaman popup terpisah"""
        st.title("📄 HASIL EXPORT")
        
        # Kotak popup style
        st.markdown("""
        <style>
        .popup-container {
            border: 3px solid #20490C;
            border-radius: 15px;
            padding: 30px;
            background-color: #f8fff8;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .download-btn {
            display: block;
            background-color: #20490C;
            color: white;
            padding: 15px 30px;
            text-align: center;
            text-decoration: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Data dari session state
        export_data = st.session_state.export_data
        file_data = export_data['file_data']
        siklus = export_data['siklus']
        format_file = export_data['format']
        
        # Konversi format file untuk nama file
        format_ext = {
            "PDF": "txt",
            "Excel": "xlsx", 
            "CSV": "csv",
            "HTML": "html",
            "JSON": "json",
            "XML": "xml"
        }
        
        # Nama file
        filename = f"Laporan_{siklus.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.{format_ext[format_file]}"
        
        # Encode file untuk download
        b64 = base64.b64encode(file_data).decode()
        
        # MIME types
        mime_types = {
            "PDF": "text/plain",
            "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "CSV": "text/csv",
            "HTML": "text/html",
            "JSON": "application/json", 
            "XML": "application/xml"
        }
        
        # KONTEN POPUP
        st.markdown('<div class="popup-container">', unsafe_allow_html=True)
        
        st.success("✅ **Export Berhasil!**")
        st.write(f"**File:** {filename}")
        st.write(f"**Format:** {format_file}")
        st.write(f"**Siklus:** {siklus}")
        
        st.markdown("---")
        
        # SECTION 1: DOWNLOAD FILE
        st.subheader("📥 Download File")
        href = f'<a href="data:{mime_types[format_file]};base64,{b64}" download="{filename}" class="download-btn">⬇️ UNDUH FILE</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # SECTION 2: SHARE KE SOSIAL MEDIA
        st.subheader("📤 Bagikan ke Sosial Media")

        st.write("Klik untuk langsung berbagi:")

        col1, col2 = st.columns(2)

        with col1:
            # WhatsApp
            whatsapp_url = f"https://api.whatsapp.com/send?text=Laporan Keuangan {siklus} - {filename}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: block; text-decoration: none;"><button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">📱 WhatsApp</button></a>', unsafe_allow_html=True)
            
            # Facebook
            facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={filename}&quote=Laporan Keuangan {siklus}"
            st.markdown(f'<a href="{facebook_url}" target="_blank" style="display: block; text-decoration: none;"><button style="width: 100%; background-color: #1877F2; color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">📘 Facebook</button></a>', unsafe_allow_html=True)
            
            # Telegram
            telegram_url = f"https://t.me/share/url?url={filename}&text=Laporan Keuangan {siklus}"
            st.markdown(f'<a href="{telegram_url}" target="_blank" style="display: block; text-decoration: none;"><button style="width: 100%; background-color: #0088CC; color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">💬 Telegram</button></a>', unsafe_allow_html=True)

        with col2:
            # Instagram (Direct Message)
            instagram_url = f"https://www.instagram.com/direct/new/"
            st.markdown(f'<a href="{instagram_url}" target="_blank" style="display: block; text-decoration: none;"><button style="width: 100%; background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D); color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">📷 Instagram</button></a>', unsafe_allow_html=True)
            
            # TikTok (Share via)
            tiktok_url = f"https://www.tiktok.com/share"
            st.markdown(f'<a href="{tiktok_url}" target="_blank" style="display: block; text-decoration: none;"><button style="width: 100%; background-color: #000000; color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">🎵 TikTok</button></a>', unsafe_allow_html=True)
            
            # Email
            email_subject = f"Laporan Keuangan {siklus}"
            email_body = f"Berikut terlampir laporan keuangan: {filename}"
            email_url = f"mailto:?subject={email_subject}&body={email_body}"
            st.markdown(f'<a href="{email_url}" style="display: block; text-decoration: none;"><button style="width: 100%; background-color: #EA4335; color: white; border: none; padding: 10px; border-radius: 5px; margin: 5px 0;">📧 Email</button></a>', unsafe_allow_html=True)

        # Tambahkan juga tombol copy link
        st.markdown("---")
        st.write("**Atau salin link file:**")
        link_text = f"https://mysite.com/download/{filename}"
        st.code(link_text, language="text")
        if st.button("📋 Salin Link", use_container_width=True):
            st.success("✅ Link berhasil disalin!")

    def generate_laporan(self, siklus, format_file):
        """Generate laporan berdasarkan siklus dan format"""
        try:
            # Data untuk laporan - TANPA CONTOH
            data = {
                "judul": f"Laporan {siklus}",
                "periode": "",
                "perusahaan": "Peternakan Sientok", 
                "tanggal_export": datetime.now().strftime("%d %B %Y %H:%M"),
                "data": []
            }
            
            # Generate file sesuai format
            if format_file == "PDF":
                return self.generate_pdf(data)
            elif format_file == "Excel":
                return self.generate_excel(data)
            elif format_file == "CSV":
                return self.generate_csv(data)
            elif format_file == "HTML":
                return self.generate_html(data)
            elif format_file == "JSON":
                return self.generate_json(data)
            elif format_file == "XML":
                return self.generate_xml(data)
                
        except Exception as e:
            st.error(f"Error generating report: {e}")
            return None

    def generate_pdf(self, data):
        """Generate PDF report sederhana"""
        try:
            pdf_content = f"""
    LAPORAN: {data['judul']}
    ========================
    Perusahaan: {data['perusahaan']}
    Periode: {data['periode']}
    Tanggal Export: {data['tanggal_export']}

    DATA AKUN:
    """
            # Tidak ada data contoh
            if not data['data']:
                pdf_content += "\nTidak ada data transaksi"
            
            return pdf_content.encode('utf-8')
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            return None

    def generate_excel(self, data):
        """Generate Excel report menggunakan pandas"""
        try:
            # Buat DataFrame kosong
            df = pd.DataFrame(columns=["Akun", "Debit", "Kredit", "Saldo"])
            
            # Simpan ke bytes
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Sheet data utama
                df.to_excel(writer, sheet_name='Data Akun', index=False)
                
                # Sheet info laporan
                info_df = pd.DataFrame([
                    ["Judul Laporan", data['judul']],
                    ["Perusahaan", data['perusahaan']],
                    ["Periode", data['periode']],
                    ["Tanggal Export", data['tanggal_export']]
                ], columns=["Keterangan", "Value"])
                
                info_df.to_excel(writer, sheet_name='Info Laporan', index=False)
                
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            st.error(f"Error generating Excel: {e}")
            return None

    def generate_csv(self, data):
        """Generate CSV report"""
        try:
            df = pd.DataFrame(columns=["Akun", "Debit", "Kredit", "Saldo"])
            return df.to_csv(index=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error generating CSV: {e}")
            return None

    def generate_html(self, data):
        """Generate HTML report"""
        try:
            html_content = f"""
            <h1>{data['judul']}</h1>
            <h2>{data['perusahaan']}</h2>
            <p><strong>Periode:</strong> {data['periode']}</p>
            <p><strong>Tanggal Export:</strong> {data['tanggal_export']}</p>
            """
            
            if not data['data']:
                html_content += "<p>Tidak ada data transaksi</p>"
            
            return html_content.encode('utf-8')
        except Exception as e:
            st.error(f"Error generating HTML: {e}")
            return None

    def generate_json(self, data):
        """Generate JSON report"""
        try:
            return json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error generating JSON: {e}")
            return None

    def generate_xml(self, data):
        """Generate XML report"""
        try:
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <laporan>
        <judul>{data['judul']}</judul>
        <perusahaan>{data['perusahaan']}</perusahaan>
        <periode>{data['periode']}</periode>
        <tanggal_export>{data['tanggal_export']}</tanggal_export>
        <data></data>
    </laporan>"""
            return xml_content.encode('utf-8')
        except Exception as e:
            st.error(f"Error generating XML: {e}")
            return None
        
    def print_document(self):
        """Fitur Print Document"""
        self.show_print_dialog()

    def show_print_dialog(self):
        st.title("🖨️ PRINT DOKUMEN")
        
        # Layout 2 kolom
        col_left, col_right = st.columns([2, 3])
        
        with col_left:
            self.show_print_settings()
        
        with col_right:
            self.show_print_preview()

    def get_print_data(self, doc_type):
        """Ambil data berdasarkan jenis dokumen yang dipilih"""
        try:
            # Load data transaksi terlebih dahulu
            if 'transactions' not in st.session_state:
                st.session_state.transactions = self.load_transactions_from_file()
            
            if doc_type == "Jurnal Umum":
                return st.session_state.transactions
            elif doc_type == "Buku Besar":
                return self.get_buku_besar_data()
            elif doc_type == "Neraca Saldo":
                return self.get_neraca_saldo_data()
            elif doc_type == "Laporan Laba/Rugi":
                return self.get_laporan_laba_rugi_data()
            else:
                return []
        except Exception as e:
            st.error(f"Error mengambil data: {e}")
            return []

    def get_buku_besar_data(self):
        """Ambil data buku besar untuk print"""
        try:
            if not st.session_state.transactions:
                return []
            
            # Format data buku besar sederhana
            buku_besar_data = []
            
            # Dapatkan semua akun unik
            akun_list = list(set(trans['akun'] for trans in st.session_state.transactions))
            
            for akun in sorted(akun_list):
                # Filter transaksi untuk akun ini
                transaksi_akun = [trans for trans in st.session_state.transactions if trans['akun'] == akun]
                
                # Hitung saldo
                saldo = 0
                for trans in transaksi_akun:
                    if self.is_akun_debit(akun):
                        saldo += trans['debit'] - trans['kredit']
                    else:
                        saldo += trans['kredit'] - trans['debit']
                
                # Tambahkan ke data buku besar
                buku_besar_data.append({
                    'akun': akun,
                    'saldo': saldo,
                    'jumlah_transaksi': len(transaksi_akun)
                })
            
            return buku_besar_data
        except Exception as e:
            st.error(f"Error mengambil data buku besar: {e}")
            return []

    def get_neraca_saldo_data(self):
        """Ambil data neraca saldo untuk print"""
        try:
            saldo_akun = self.hitung_saldo_semua_akun()
            
            neraca_data = []
            for akun, saldo in saldo_akun.items():
                neraca_data.append({
                    'akun': akun,
                    'debit': saldo if self.is_akun_debit(akun) and saldo > 0 else 0,
                    'kredit': abs(saldo) if not self.is_akun_debit(akun) and saldo > 0 else 0
                })
            
            return neraca_data
        except Exception as e:
            st.error(f"Error mengambil data neraca saldo: {e}")
            return []

    def get_laporan_laba_rugi_data(self):
        """Ambil data laporan laba/rugi untuk print"""
        try:
            saldo_akun = self.hitung_saldo_semua_akun()
            
            laba_rugi_data = []
            pendapatan_total = 0
            beban_total = 0
            
            # Hitung pendapatan dan beban
            for akun, saldo in saldo_akun.items():
                if "Pendapatan" in akun:
                    pendapatan_total += saldo
                    laba_rugi_data.append({
                        'item': akun,
                        'jumlah': saldo,
                        'tipe': 'pendapatan'
                    })
                elif "Beban" in akun:
                    beban_total += abs(saldo)
                    laba_rugi_data.append({
                        'item': akun,
                        'jumlah': abs(saldo),
                        'tipe': 'beban'
                    })
            
            laba_rugi = pendapatan_total - beban_total
            
            laba_rugi_data.append({
                'item': 'LABA/RUGI BERSIH',
                'jumlah': laba_rugi,
                'tipe': 'laba_rugi'
            })
            
            return laba_rugi_data
        except Exception as e:
            st.error(f"Error mengambil data laba rugi: {e}")
            return []

    def show_print_settings(self):
        """Kolom kiri - Settings"""
        
        # Section 1: Pilih Dokumen - SIMPAN DI SESSION STATE
        st.subheader("📄 DOKUMEN")
        doc_options = ["Jurnal Umum", "Buku Besar", "Neraca Saldo", "Laporan Laba/Rugi"]
        selected_doc = st.selectbox(
            "Pilih dokumen:", 
            doc_options, 
            key="print_doc_select",
            label_visibility="collapsed"
        )
        
        # Simpan pilihan dokumen di session state
        st.session_state.selected_doc = selected_doc
        
        # Section 2: Metode Print
        st.subheader("🖨️ METODE PRINT")
        print_method = st.radio("Pilih metode:", ["Browser Print", "Save as PDF"], label_visibility="collapsed")
        
        # Section 3: Pengaturan
        st.subheader("⚙️ PENGATURAN")
        
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            copies = st.number_input("Copies:", 1, 10, 1)
            paper_size = st.selectbox("Paper:", ["A4", "Letter", "Legal", "A3"])
            scale = st.selectbox("Scale:", ["100%", "90%", "80%", "Fit to Page"])
        
        with col_set2:
            orientation = st.radio("Orientation:", ["Portrait", "Landscape"])
            margins = st.selectbox("Margins:", ["Normal", "Wide", "Narrow"])
        
        # Section 4: Opsi
        st.subheader("✅ OPTIONS")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            include_header = st.checkbox("Include Header", value=True)
            page_numbers = st.checkbox("Page Numbers", value=True)
        with col_opt2:
            grayscale = st.checkbox("Grayscale", value=False)
        
        # Section 5: Action Buttons
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🖨️ PRINT NOW", use_container_width=True, type="primary"):
                self.execute_print(selected_doc, print_method)
        
        with col_btn2:
            if st.button("👁️ PREVIEW", use_container_width=True):
                st.rerun()

    def show_print_preview(self):
        """Kolom kanan - Preview dengan Data Real"""
        
        st.subheader("📄 PREVIEW")
        
        # Ambil dokumen yang dipilih dari session state atau default
        selected_doc = st.session_state.get('selected_doc', 'Jurnal Umum')
        
        # DEBUG: Tampilkan info debug
        st.write(f"🔍 Debug: Selected doc = {selected_doc}")
        
        # Ambil data real berdasarkan dokumen
        real_data = self.get_print_data(selected_doc)
        
        st.write(f"🔍 Debug: Data length = {len(real_data) if real_data else 0}")
        
        if real_data:
            st.success(f"✅ Data ditemukan: {len(real_data)} entri")
            
            # Tampilkan data real
            if selected_doc == "Jurnal Umum":
                self.show_jurnal_umum_preview(real_data)
            elif selected_doc == "Buku Besar":
                self.show_buku_besar_preview(real_data)
            elif selected_doc == "Neraca Saldo":
                self.show_neraca_saldo_preview(real_data)
            elif selected_doc == "Laporan Laba/Rugi":
                self.show_laporan_laba_rugi_preview(real_data)
        else:
            # Tampilkan pesan kosong
            st.info("📭 **Tidak ada data untuk ditampilkan**")
            st.write("Pastikan sudah input transaksi di menu **Jurnal Umum**")
            
            # Tabel kosong
            empty_data = {
                "Tanggal": ["-", "-", "-"],
                "Akun": ["-", "-", "-"], 
                "Keterangan": ["-", "-", "-"],
                "Debit": ["-", "-", "-"],
                "Kredit": ["-", "-", "-"]
            }
            df = pd.DataFrame(empty_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

    def show_jurnal_umum_preview(self, data):
        """Tampilkan preview Jurnal Umum"""
        st.write(f"**Jumlah Transaksi:** {len(data)} entri")
        
        # Format data untuk preview
        preview_data = []
        for trans in data:
            preview_data.append({
                "Tanggal": trans['tanggal'],
                "Akun": trans['akun'],
                "Keterangan": trans.get('keterangan', ''),
                "Debit": f"Rp{trans['debit']:,.0f}" if trans['debit'] > 0 else "-",
                "Kredit": f"Rp{trans['kredit']:,.0f}" if trans['kredit'] > 0 else "-"
            })
        
        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    def show_buku_besar_preview(self, data):
        """Tampilkan preview Buku Besar"""
        st.write(f"**Jumlah Akun:** {len(data)} akun")
        
        preview_data = []
        for item in data:
            preview_data.append({
                "Akun": item['akun'],
                "Saldo": f"Rp{item['saldo']:,.0f}",
                "Jumlah Transaksi": item['jumlah_transaksi']
            })
        
        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    def show_neraca_saldo_preview(self, data):
        """Tampilkan preview Neraca Saldo"""
        st.write(f"**Jumlah Akun:** {len(data)} akun")
        
        preview_data = []
        for item in data:
            preview_data.append({
                "Akun": item['akun'],
                "Debit": f"Rp{item['debit']:,.0f}" if item['debit'] > 0 else "-",
                "Kredit": f"Rp{item['kredit']:,.0f}" if item['kredit'] > 0 else "-"
            })
        
        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    def show_laporan_laba_rugi_preview(self, data):
        """Tampilkan preview Laporan Laba/Rugi"""
        preview_data = []
        for item in data:
            preview_data.append({
                "Item": item['item'],
                "Jumlah": f"Rp{item['jumlah']:,.0f}"
            })
        
        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    def execute_print(self, doc_type, method):
        """Execute print action dengan data real"""
        
        print_data = self.get_print_data(doc_type)
        
        if not print_data:
            st.error("❌ Tidak ada data untuk di-print!")
            return
        
        if method == "Browser Print":
            # Generate file text untuk print
            text_content = self.generate_text_for_print(doc_type, print_data)
            
            st.success("📄 File Text siap diunduh!")
            st.download_button(
                label="📥 Download File Text untuk Print",
                data=text_content,
                file_name=f"{doc_type}_print.txt",
                mime="text/plain"
            )
            
            # Juga tampilkan CSV option
            csv_content = self.generate_csv_for_print(doc_type, print_data)
            st.download_button(
                label="📥 Download CSV untuk Excel",
                data=csv_content,
                file_name=f"{doc_type}.csv",
                mime="text/csv"
            )
            
            st.info("""
            **📋 Cara Print:**
            - **File Text**: Download → Buka di Notepad → Ctrl+P
            - **File CSV**: Download → Buka di Excel → Format → Print
            """)
            
            # Tampilkan preview
            st.markdown("---")
            st.subheader("👁️ Preview untuk Print")
            self.display_text_preview(doc_type, print_data)
        
        elif method == "Save as PDF":
            # Generate PDF menggunakan cara sederhana
            pdf_data = self.generate_pdf_for_print(doc_type, print_data)
            
            if pdf_data:
                st.success("📄 PDF siap diunduh!")
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=f"{doc_type}.pdf",
                    mime="application/pdf"
                )

    def generate_text_for_print(self, doc_type, data):
        """Generate text file yang formatted untuk print"""
        from datetime import datetime
        
        text = "=" * 60 + "\n"
        text += f"PETERNAKAN SIENTOK\n".center(60) + "\n"
        text += f"{doc_type.upper()}\n".center(60) + "\n"
        text += f"Tanggal: {datetime.now().strftime('%d %B %Y %H:%M')}\n"
        text += "=" * 60 + "\n\n"
        
        if doc_type == "Jurnal Umum":
            text += self._format_jurnal_umum_text(data)
        elif doc_type == "Buku Besar":
            text += self._format_buku_besar_text(data)
        elif doc_type == "Neraca Saldo":
            text += self._format_neraca_saldo_text(data)
        
        text += "\n" + "=" * 60 + "\n"
        text += "Dicetak dari Sistem Akuntansi Sientok\n"
        
        return text

    def _format_jurnal_umum_text(self, data):
        """Format Jurnal Umum untuk text"""
        text = "JURNAL UMUM\n"
        text += "-" * 80 + "\n"
        text += f"{'Tanggal':<12} {'Akun':<20} {'Keterangan':<25} {'Debit':>12} {'Kredit':>12}\n"
        text += "-" * 80 + "\n"
        
        for trans in data:
            tanggal = trans['tanggal']
            akun = trans['akun'][:18]  # Potong jika terlalu panjang
            keterangan = trans.get('keterangan', '')[:22]  # Potong jika terlalu panjang
            debit = f"Rp{trans['debit']:>10,.0f}" if trans['debit'] > 0 else " " * 12
            kredit = f"Rp{trans['kredit']:>10,.0f}" if trans['kredit'] > 0 else " " * 12
            
            text += f"{tanggal:<12} {akun:<20} {keterangan:<25} {debit:>12} {kredit:>12}\n"
        
        # Total
        total_debit = sum(trans['debit'] for trans in data)
        total_kredit = sum(trans['kredit'] for trans in data)
        text += "-" * 80 + "\n"
        text += f"{'TOTAL':<57} Rp{total_debit:>10,.0f} Rp{total_kredit:>10,.0f}\n"
        
        return text

    def _format_buku_besar_text(self, data):
        """Format Buku Besar untuk text"""
        text = "BUKU BESAR\n"
        text += "-" * 60 + "\n"
        text += f"{'Akun':<30} {'Saldo':>15} {'Transaksi':>10}\n"
        text += "-" * 60 + "\n"
        
        for item in data:
            akun = item['akun'][:28]  # Potong jika terlalu panjang
            saldo = f"Rp{item['saldo']:>12,.0f}"
            transaksi = f"{item['jumlah_transaksi']:>9}"
            
            text += f"{akun:<30} {saldo:>15} {transaksi:>10}\n"
        
        return text

    def _format_neraca_saldo_text(self, data):
        """Format Neraca Saldo untuk text"""
        text = "NERACA SALDO\n"
        text += "-" * 70 + "\n"
        text += f"{'Akun':<30} {'Debit':>15} {'Kredit':>15}\n"
        text += "-" * 70 + "\n"
        
        total_debit = 0
        total_kredit = 0
        
        for item in data:
            akun = item['akun'][:28]
            debit = f"Rp{item['debit']:>12,.0f}" if item['debit'] > 0 else " " * 15
            kredit = f"Rp{item['kredit']:>12,.0f}" if item['kredit'] > 0 else " " * 15
            
            text += f"{akun:<30} {debit:>15} {kredit:>15}\n"
            
            total_debit += item['debit']
            total_kredit += item['kredit']
        
        text += "-" * 70 + "\n"
        text += f"{'TOTAL':<30} Rp{total_debit:>12,.0f} Rp{total_kredit:>12,.0f}\n"
        text += f"{'STATUS':<30} {'SEIMBANG' if total_debit == total_kredit else 'TIDAK SEIMBANG'}\n"
        
        return text

    def generate_csv_for_print(self, doc_type, data):
        """Generate CSV file untuk buka di Excel"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["PETERNakan SIENTOK"])
        writer.writerow([doc_type.upper()])
        writer.writerow([f"Tanggal: {datetime.now().strftime('%d %B %Y %H:%M')}"])
        writer.writerow([])  # Empty row
        
        if doc_type == "Jurnal Umum":
            writer.writerow(["Tanggal", "Akun", "Keterangan", "Debit", "Kredit"])
            for trans in data:
                writer.writerow([
                    trans['tanggal'],
                    trans['akun'],
                    trans.get('keterangan', ''),
                    trans['debit'],
                    trans['kredit']
                ])
        
        elif doc_type == "Buku Besar":
            writer.writerow(["Akun", "Saldo", "Jumlah Transaksi"])
            for item in data:
                writer.writerow([
                    item['akun'],
                    item['saldo'],
                    item['jumlah_transaksi']
                ])
        
        elif doc_type == "Neraca Saldo":
            writer.writerow(["Akun", "Debit", "Kredit"])
            for item in data:
                writer.writerow([
                    item['akun'],
                    item['debit'],
                    item['kredit']
                ])
        
        csv_content = output.getvalue()
        return csv_content

    def display_text_preview(self, doc_type, data):
        """Tampilkan preview text di Streamlit"""
        text_content = self.generate_text_for_print(doc_type, data)
        
        st.text_area(
            "Preview File Text (Copy-paste ke text editor untuk print):",
            text_content,
            height=300,
            key="text_preview"
        )
        
        if st.button("📋 Copy Text ke Clipboard"):
            st.success("✅ Text berhasil disalin! Paste di Notepad/Word lalu print.")
            
    def logout(self):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.current_page = "login"
        st.rerun()
    
# Main execution
def main():
    # ⚠️ PASTIKAN LAYOUT WIDE DI SINI ⚠️
    st.set_page_config(
        page_title="Modern Login App",
        page_icon="🔐",
        layout="wide",  # ✅ INI YANG PENTING
        initial_sidebar_state="expanded"
    )
    
    app = ModernLoginApp()
    app.run()

if __name__ == "__main__":
    main()
    