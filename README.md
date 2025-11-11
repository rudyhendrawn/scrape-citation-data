# scrape-citation-data
Script untuk scraping data sitasi dari Google Scholar berdasarkan nama dosen dan Google Scholar ID. Script ini mengumpulkan data publikasi dan jumlah sitasi per tahun untuk setiap artikel.

## Features
- Scraping data publikasi dari Google Scholar berdasarkan Scholar ID
- Mengumpulkan informasi sitasi per tahun untuk setiap artikel
- Support untuk sampling data (testing dengan jumlah sample terbatas)
- Output dalam format CSV untuk analisis lebih lanjut
- Logging detail untuk monitoring proses scraping

## Requirements
- Python version > 3.9
- [Selenium](https://selenium-python.readthedocs.io/) - Web scraping automation
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/) - Browser driver untuk Selenium
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML parsing
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) - Automatic WebDriver management

### Installation
```bash
pip install selenium beautifulsoup4 pandas webdriver-manager openpyxl
```

---

## Petunjuk Penggunaan

### Persiapan File Input
1. Pastikan memiliki daftar nama dosen dan Google Scholar ID dalam format Excel (.xlsx)
2. File input **wajib** memiliki kolom:
   - `scholar_id` - Google Scholar ID dosen
   - `NAMA` - Nama dosen (optional, untuk logging/tracking)
3. Daftar nama dosen bersifat optional, namun disarankan untuk memudahkan tracking proses scraping

### Struktur File Input
| No. | scholar_id   | NAMA          |
|-----|--------------|---------------|
| 1   | cSku1GYAAAAJ | Dr. John Doe  |
| 2   | 8Z9eYs8AAAAJ | Dr. Jane Smith|
| 3   | xyz123AAAAJ  | Dr. Bob Wilson|

---

## Cara Menggunakan

### 1. Clone Repository
```bash
git clone https://github.com/rudyhendrawn/scrape-citation-data.git
cd scrape-citation-data
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan Script

#### Menggunakan Sample Data (untuk testing)
```bash
python main.py --input_file data/input.xlsx --output_file data/output.csv --using_samples True --num_of_samples 3
```

#### Menggunakan Semua Data
```bash
python main.py --input_file data/input.xlsx --output_file data/output.csv --using_samples False
```

### Parameter Penjelasan
- `--input_file`: Path ke file Excel input yang berisi scholar_id
- `--output_file`: Path ke file CSV output (harus berformat .csv)
- `--using_samples`: `True` untuk menggunakan sample, `False` untuk semua data
- `--num_of_samples`: Jumlah sample yang digunakan (hanya jika `using_samples=True`)

---

## Output Data

### Struktur Output CSV
File output akan berisi kolom-kolom berikut:

| Kolom               | Deskripsi                                          |
|---------------------|----------------------------------------------------|
| article_id          | ID unik artikel dari Google Scholar                |
| year                | Tahun sitasi                                       |
| num_of_citations    | Jumlah sitasi pada tahun tersebut                  |
| scholar_id          | Google Scholar ID dosen                            |
| title               | Judul publikasi                                    |
| authors             | Daftar penulis                                     |
| publisher           | Nama penerbit/jurnal                               |
| citations           | Total sitasi artikel                               |
| article_url         | URL relatif ke halaman artikel di Google Scholar   |
| NAMA                | Nama dosen (dari file input)                       |

### Contoh Output
```csv
article_id,year,num_of_citations,scholar_id,title,authors,publisher,citations,article_url,NAMA
HlqEGQ0AAAAJ:-FonjvnnhkoC,2019,5,cSku1GYAAAAJ,Machine Learning Application,John Doe et al,IEEE,19,/citations?view_op=view_citation...,Dr. John Doe
HlqEGQ0AAAAJ:-FonjvnnhkoC,2020,8,cSku1GYAAAAJ,Machine Learning Application,John Doe et al,IEEE,19,/citations?view_op=view_citation...,Dr. John Doe
```

---

## Cara Kerja Script

1. **Load Data Input**: Membaca file Excel yang berisi scholar_id
2. **Scraping Publikasi**: Untuk setiap scholar_id, script akan:
   - Mengakses halaman Google Scholar
   - Mengambil semua publikasi (dengan klik "Show more" jika ada)
   - Mengekstrak data: judul, penulis, penerbit, tahun, dan jumlah sitasi
3. **Scraping Sitasi per Tahun**: Untuk setiap artikel:
   - Mengakses halaman detail artikel
   - Mengambil grafik sitasi per tahun
   - Menyimpan jumlah sitasi untuk setiap tahun
4. **Merging Data**: Menggabungkan data publikasi dengan data sitasi per tahun
5. **Export**: Menyimpan hasil ke file CSV

---

## Jupyter Notebook

Tersedia juga versi Jupyter Notebook (`get_citation_per_article.ipynb`) untuk eksplorasi dan testing interaktif dengan fitur:
- Step-by-step execution
- Data visualization capability
- Easier debugging
- Experimental ThreadPoolExecutor implementation (commented out - tidak stabil)

---

## Catatan Penting

⚠️ **Rate Limiting**: Google Scholar memiliki rate limiting. Jika melakukan terlalu banyak request dalam waktu singkat, IP Anda mungkin diblokir sementara.

💡 **Tips**:
- Gunakan `--using_samples True` untuk testing terlebih dahulu
- Untuk dataset besar, pertimbangkan untuk menjalankan script dalam batch
- Script menggunakan delay antar request untuk menghindari blocking
- ThreadPoolExecutor (concurrent scraping) masih dalam development dan belum stabil

⏱️ **Waktu Eksekusi**: 
- Estimasi: ~2-3 detik per artikel
- Untuk 100 artikel: ~3-5 menit

---

## Troubleshooting

### Error: "No graph bars found"
- Artikel tidak memiliki data sitasi atau format halaman berubah
- Script akan skip artikel tersebut dan melanjutkan

### Error: ChromeDriver version mismatch
- Script menggunakan `webdriver-manager` yang otomatis mendownload ChromeDriver yang sesuai
- Pastikan koneksi internet stabil saat pertama kali menjalankan

### Output file kosong
- Periksa apakah scholar_id valid
- Periksa log untuk error details
- Coba dengan `--using_samples True --num_of_samples 1` untuk testing

---

## License
This project is open source and available under the MIT License.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For questions or issues, please open an issue on GitHub.
