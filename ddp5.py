import csv
import pwinput
import os
from prettytable import PrettyTable
from datetime import datetime
from colorama import Fore, init

os.system("cls")
init(autoreset=True)

# ==========================
# FILE CSV
# ==========================
FILE_AKUN = 'akun.csv'
FILE_LAYANAN = 'jenis_layanan.csv'
FILE_TRANSAKSI = 'transaksi.csv'
FILE_SALDO = 'saldo.csv'

MIN_SALDO = 25000
MAX_SALDO = 500000


# ==========================
# CEK AKUN
# ==========================
def cek_akun(nama, sandi):
    try:
        with open(FILE_AKUN, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama_pengguna"] == nama and row["sandi"] == sandi:
                    return row
    except FileNotFoundError:
        print("File akun.csv tidak ditemukan.")
    return None


# ==========================
# MENU UTAMA
# ==========================
def menu_utama():
    while True:
        print(Fore.CYAN + "\n╔════════════════════════════════════╗")
        print("   Selamat Datang di Barber Five 💈   ")
        print("   Siap Glow Up Bareng Kami?(˃ᴗ˂)      ")
        print(Fore.BLUE + "╚════════════════════════════════════╝")
        print("[1] Login Admin 👤")
        print("[2] Login Pengguna 💇")
        print("[3] Daftar Akun Baru 📁")
        print("[4] Keluar 🔚")

        try:
            pilihan = input("Pilih menu: ")
        except KeyboardInterrupt:
            print("\nJangan tekan CTRL + C ya!")
            continue
        except EOFError:
            print("\nJangan tekan CTRL + Z ya!")
            continue

        if pilihan == "1":
            login("admin")
        elif pilihan == "2":
            login("pengguna")
        elif pilihan == "3":
            daftar_akun_baru()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan sistem Barber Five.")
            break
        else:
            print("Pilihan tidak valid.")


# ==========================
# LOGIN
# ==========================
def login(role_dipilih):
    print(f"\n✦•┈๑⋅⋯ Login {role_dipilih} ⋯⋅๑┈•✦")
    try:
        nama = input("Nama pengguna: ")
        sandi = pwinput.pwinput("Sandi: ", mask="●")
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
        return

    akun = cek_akun(nama, sandi)

    if akun and akun["role"] == role_dipilih:
        print(f"\nLogin berhasil sebagai {akun['role']}")
        print(f"Selamat datang, {akun['nama_pengguna']}")
        if akun["role"] == "admin":
            menu_admin()
        elif akun["role"] == "pengguna":
            menu_pengguna(akun)
    else:
        print("Login gagal")
        print("Periksa kembali username, password, serta apakah akunmu telah terdaftar!")


# ==========================
# DAFTAR AKUN BARU
# ==========================
def daftar_akun_baru():
    print(Fore.CYAN+"\n====================================")
    print("+         DAFTAR AKUN BARU 📁      +")
    print(Fore.BLUE+"====================================")
    try:
        nama = input("Masukkan nama pengguna baru: ")
        sandi = pwinput.pwinput("Masukkan sandi: ", mask="●")
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
        return

    if not nama.strip():
        print("Nama tidak boleh kosong.")
        return

    try:
        with open(FILE_AKUN, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama_pengguna"] == nama:
                    print("Nama pengguna sudah terdaftar!")
                    return
    except FileNotFoundError:
        pass

    with open(FILE_AKUN, mode='a', newline='') as file:
        fieldnames = ['nama_pengguna', 'sandi', 'role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({'nama_pengguna': nama, 'sandi': sandi, 'role': 'pengguna'})

    print("Akun berhasil didaftarkan!")
    update_saldo_pengguna(nama, 0)
    print("Akun baru berhasil dibuat! Silakan login sebagai pengguna.")


# ==========================
# MENU ADMIN
# ==========================
def menu_admin():
    while True:
        print("\n╭───────[⚒Admin⚒]───────╮")
        print("1. Lihat Daftar Layanan")
        print("2. Tambah Layanan Baru")
        print("3. Edit Layanan")
        print("4. Hapus Layanan")
        print("5. Lihat Daftar Transaksi")
        print("6. Keluar")
        print("╰────────────👋─────────╯")

        try:
            pilihan = input("Pilih menu (1-6): ")
        except KeyboardInterrupt:
            print("\nJangan tekan CTRL + C ya!")
            continue
        except EOFError:
            print("\nJangan tekan CTRL + Z ya!")
            continue

        if pilihan == "1":
            lihat_layanan()
        elif pilihan == "2":
            tambah_layanan()
        elif pilihan == "3":
            edit_layanan()
        elif pilihan == "4":
            hapus_layanan()
        elif pilihan == "5":
            lihat_transaksi()
        elif pilihan == "6":
            print("\n──────────── ୨୧ ────────────")
            print("  Keluar dari menu admin      ")
            print("──────────── ୨୧ ────────────")
            break
        else:
            print("Pilihan tidak valid!")


def baca_layanan(): #CSV
    layanan = []
    try:
        with open(FILE_LAYANAN, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                layanan.append(row)
    except FileNotFoundError:
        pass
    return layanan


def tulis_layanan(layanan): #CSV
    with open(FILE_LAYANAN, mode='w', newline='') as file:
        fieldnames = ['id', 'nama_layanan', 'harga']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(layanan)

# ==========================
# MENAMPILKAN LAYANAN
# ==========================
def lihat_layanan(): 
    layanan = baca_layanan()
    if not layanan:
        print("Belum ada data layanan.")
        return
    tabel = PrettyTable(["ID", "Nama Layanan", "Harga"])
    for data in layanan:
        tabel.add_row([data['id'], data['nama_layanan'], data['harga']])
    print(tabel)

# ==========================
# TAMBAH LAYANAN
# ==========================
def tambah_layanan():
    layanan = baca_layanan()
    lihat_layanan()
    id_baru = str(len(layanan) + 1)

    while True:
        try:
            nama = input("Masukkan nama layanan baru: ")
            if not nama.strip():
                print("Nama tidak boleh kosong.")
                continue
            if nama.isdigit():
                print("Nama tidak boleh angka saja.")
                continue
            break
        except KeyboardInterrupt:
            print("\nJangan tekan CTRL + C ya!")
        except EOFError:
            print("\nJangan tekan CTRL + Z ya!")

    while True:
        try:
            harga = int(input("Masukkan harga layanan: "))
            break
        except ValueError:
            print("Harga harus angka.")
        except KeyboardInterrupt:
            print("\nJangan tekan CTRL + C ya!")
        except EOFError:
            print("\nJangan tekan CTRL + Z ya!")

    layanan.append({"id": id_baru, "nama_layanan": nama, "harga": harga})
    tulis_layanan(layanan)
    print("Layanan berhasil ditambahkan!")

# ==========================
# EDIT LAYANAN
# ==========================
def edit_layanan():
    layanan = baca_layanan()
    if not layanan:
        print("Belum ada data layanan.")
        return
    lihat_layanan()

    try:
        id_edit = str(int(input("Masukkan ID layanan yang ingin diubah: ")))
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return

    for data in layanan:
        if data["id"] == id_edit:
            while True:
                try:
                    nama = input("Masukkan nama layanan baru: ")
                    if not nama.strip():
                        print("Nama tidak boleh kosong.")
                    elif nama.isdigit():
                        print("Nama tidak boleh angka saja.")
                    else:
                        break
                except KeyboardInterrupt:
                    print("\nJangan tekan CTRL + C ya!")
                except EOFError:
                    print("\nJangan tekan CTRL + Z ya!")

            while True:
                try:
                    harga = int(input("Masukkan harga layanan baru: "))
                    break
                except ValueError:
                    print("Harga harus angka.")
                except KeyboardInterrupt:
                    print("\nJangan tekan CTRL + C ya!")
                except EOFError:
                    print("\nJangan tekan CTRL + Z ya!")

            tulis_layanan(layanan)
            print("Data layanan berhasil diubah!")
            return

    print("ID layanan tidak ditemukan!")

# ==========================
# HAPUS LAYANAN
# ==========================
def hapus_layanan():
    layanan = baca_layanan()
    if not layanan:
        print("Belum ada data layanan.")
        return
    lihat_layanan()
    try:
        id_hapus = input("Masukkan ID layanan yang ingin dihapus: ")
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
        return

    layanan_baru = [data for data in layanan if data["id"] != id_hapus]
    if len(layanan_baru) != len(layanan):
        for i, data in enumerate(layanan_baru, start=1):
            data["id"] = str(i)
        tulis_layanan(layanan_baru)
        print("Layanan berhasil dihapus!")
    else:
        print("ID layanan tidak ditemukan!")

# ==========================
# TRANSAKSI
# ==========================
def baca_transaksi():
    transaksi = []
    try:
        with open(FILE_TRANSAKSI, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaksi.append(row)
    except FileNotFoundError:
        pass
    return transaksi


def lihat_transaksi():
    transaksi = baca_transaksi()
    if not transaksi:
        print("Belum ada data transaksi.")
        return
    tabel = PrettyTable(["ID", "Pengguna", "Layanan", "Harga", "Tanggal"])
    for data in transaksi:
        tabel.add_row([data['id_transaksi'], data['nama_pengguna'], data['layanan'], data['harga'], data['tanggal']])
    print(tabel)


# ==========================
# SALDO
# ==========================
def baca_saldo(nama_pengguna):
    try:
        with open(FILE_SALDO, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama_pengguna"] == nama_pengguna:
                    return int(row["saldo"])
    except FileNotFoundError:
        pass
    return 0


def update_saldo_pengguna(nama_pengguna, saldo_baru):
    data = []
    found = False
    try:
        with open(FILE_SALDO, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["nama_pengguna"] == nama_pengguna:
                    row["saldo"] = str(saldo_baru)
                    found = True
                data.append(row)
    except FileNotFoundError:
        pass

    if not found:
        data.append({"nama_pengguna": nama_pengguna, "saldo": str(saldo_baru)})

    with open(FILE_SALDO, mode='w', newline='') as file:
        fieldnames = ["nama_pengguna", "saldo"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# ==========================
# MENU PENGGUNA
# ==========================
def menu_pengguna(akun):
    while True:
        print("\n╭──────[💈Menu Pengguna💈]─────────╮")
        print("1. Lihat Daftar Layanan")
        print("2. Buat Reservasi")
        print("3. Cek Saldo E-money")
        print("4. Top Up Saldo")
        print("5. Keluar")
        print("╰───────────────👋─────────────────╯")

        try:
            pilihan = input("Pilih menu (1-5): ")
        except KeyboardInterrupt:
            print("\nJangan tekan CTRL + C ya!")
            continue
        except EOFError:
            print("\nJangan tekan CTRL + Z ya!")
            continue

        if pilihan == "1":
            lihat_layanan()
        elif pilihan == "2":
            buat_reservasi(akun)
        elif pilihan == "3":
            saldo = baca_saldo(akun["nama_pengguna"])
            print(f"Saldo E-money Anda: Rp {saldo}")
        elif pilihan == "4":
            top_up_saldo(akun)
        elif pilihan == "5":
            print("\n──────────── ୨୧ ────────────")
            print("  Keluar dari menu pengguna.")
            print("──────────── ୨୧ ────────────")
            break
        else:
            print("Pilihan tidak valid!")


# ==========================
# RESERVASI
# ==========================
def buat_reservasi(akun):
    layanan = baca_layanan()
    if not layanan:
        print("Belum ada layanan tersedia.")
        return

    lihat_layanan()
    try:
        id_pilih = input("Masukkan ID layanan yang ingin dipesan: ")
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
        return

    for data in layanan:
        if data["id"] == id_pilih:
            harga = int(data["harga"])
            saldo = baca_saldo(akun["nama_pengguna"])

            if saldo < harga:
                print("Saldo Anda tidak cukup untuk melakukan reservasi.")
                return

            transaksi = baca_transaksi()
            id_transaksi = str(len(transaksi) + 1)
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            transaksi.append({
                "id_transaksi": id_transaksi,
                "nama_pengguna": akun["nama_pengguna"],
                "layanan": data["nama_layanan"],
                "harga": str(harga),
                "tanggal": tanggal
            })

            with open(FILE_TRANSAKSI, mode='w', newline='') as file:
                fieldnames = ["id_transaksi", "nama_pengguna", "layanan", "harga", "tanggal"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(transaksi)

            update_saldo_pengguna(akun["nama_pengguna"], saldo - harga)
            print(f"Reservasi berhasil! Layanan: {data['nama_layanan']}")
            print(f"Sisa saldo Anda: Rp {saldo - harga}")

            cetak_invoice(akun["nama_pengguna"], data["nama_layanan"], harga, saldo - harga, tanggal)
            return

    print("ID layanan tidak ditemukan.")


def cetak_invoice(nama, layanan, harga, saldo_sisa, tanggal):
    print("\n==========================================")
    print("         🧾 INVOICE BARBER FIVE       ")
    print("==========================================")
    print(f"Nama Pengguna : {nama}")
    print(f"Layanan       : {layanan}")
    print(f"Harga         : Rp {harga}")
    print(f"Sisa Saldo    : Rp {saldo_sisa}")
    print(f"Tanggal       : {tanggal}")
    print("==========================================")
    print("Terima kasih telah melakukan reservasi!\n")


# ==========================
# TOP UP SALDO
# ==========================
def top_up_saldo(akun):
    try:
        tambah = int(input("Masukkan jumlah top-up: "))
    except ValueError:
        print("Input tidak valid. Masukkan angka.")
        return
    except KeyboardInterrupt:
        print("\nJangan tekan CTRL + C ya!")
        return
    except EOFError:
        print("\nJangan tekan CTRL + Z ya!")
        return

    saldo_sekarang = baca_saldo(akun["nama_pengguna"])
    saldo_baru = saldo_sekarang + tambah

    if saldo_baru < MIN_SALDO:
        print("Minimal saldo adalah Rp25.000.")
        return
    elif saldo_baru > MAX_SALDO:
        print("Maksimal saldo yang diperbolehkan Rp500.000.")
        return

    update_saldo_pengguna(akun["nama_pengguna"], saldo_baru)
    print(f"Top-up berhasil! Saldo sekarang: Rp {saldo_baru}")


# ==========================
# JALANKAN PROGRAM
# ==========================

menu_utama()
