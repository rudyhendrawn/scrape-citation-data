# scrape-citation-data
Script untuk scraping data sitasi berdasarkan nama dosen dan Google Scholar ID.

## Requirements
- Python version > 3.9
- [Selenium](https://selenium-python.readthedocs.io/)
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://requests.readthedocs.io/)
- [TQDM](https://tqdm.github.io/)

## Petunjuk Penggunaan
1. Pastikan memiliki daftar nama dosen dan Google Scholar ID dalam format Excel (wajib).
2. Daftar nama dosen pada dasarnya bersifat optional, namun untuk memudahkan dalam proses analisis data, disarankan untuk menyertakan daftar nama dosen.
3. File input harus memiliki setidaknya satu kolom dengan nama `scholar_id`.
4. File output akan berisi data sitasi yang berhasil di-scrape.

## Penggunaan
1. Pastikan semua requirements terpenuhi.
2. Clone repository ini.
3. Jalankan `python main.py --input_file <path input> --output_file <path output> --using_samples True --num_of_samples 3`
4. Contoh penggunaan:
```bash
python main.py --input_file data/input.xlsx --output_file data/output.csv --using_samples True --num_of_samples 3
```
5. Secara default, script ini akan hanya mengambil data sitasi dari 3 sampel data saja. Jika ingin mengambil semua data, gunakan `--using_samples False`.

## Contoh File Input
|No.| scholar_id |
|---|------------|
|1| cSku1GYAAAAJ |
|2| 8Z9eYs8AAAAJ |
|3| 8Z9eYs8AAAAJ |

## Contoh File Output
| article_id | year_x | num_of_citations_x | scholar_id | title | authors | publisher | year_y | num_of_citations_y | citations | article_url |
|------------|--------|--------------------|------------|-------|---------|-----------|--------|--------------------|-----------|------------|
| HlqEGQ0AAAAJ:-FonjvnnhkoC | 2019 | 10 | cSku1GYAAAAJ | Title 1 | Author 1 | Publisher 1 | 2019 |  | 19 | /citations?view_op=view_citation&hl=en&user=HlqEGQ0AAAAJ&citation_for_view=HlqEGQ0AAAAJ:-FonjvnnhkoC |
| HlqEGQ0AAAAJ:u5HHmVD_uO8C | 2019 | 10 | cSku1GYAAAAJ | Title 2 | Author 2 | Publisher 2 | 2019 |  | 19 | /citations?view_op=view_citation&hl=en&user=HlqEGQ0AAAAJ&citation_for_view=HlqEGQ0AAAAJ:u5HHmVD_uO8C |
| HlqEGQ0AAAAJ:u-x6o8ySG0sC | 2019 | 10 | cSku1GYAAAAJ | Title 3 | Author 3 | Publisher 3 | 2019 |  | 19 | /citations?view_op=view_citation&hl=en&user=HlqEGQ0AAAAJ&citation_for_view=HlqEGQ0AAAAJ:u-x6o8ySG0sC |
