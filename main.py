import os
import time
import argparse
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# Function to get publication data
def get_publication_data(scholar_id):
	"""
	Scrape publication data for a given Google Scholar ID.

	Args:
		scholar_id (str): Google Scholar ID of the researcher.

	Returns:
		list: A list of dictionaries containing publication data.
	"""
	url = f'https://scholar.google.com/citations?user={scholar_id}&hl=en'
	browser.get(url)
	time.sleep(delay_times_1)

	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	publications = []
	for row in soup.find_all('tr', class_='gsc_a_tr'):
		title_elem = row.find('a', class_='gsc_a_at')
		title = row.find('a', class_='gsc_a_at').text
		year = row.find('span', class_='gsc_a_hc').text
		citations = row.find('a', class_='gsc_a_ac').text
		authors_publisher = row.find_all('div', class_='gs_gray')
		authors = authors_publisher[0].text
		publisher = authors_publisher[1].text

		article_url = title_elem['href'] if title_elem else 'N/A'
		article_id = article_url.split('citation_for_view=')[1] if article_url != 'N/A' else 'N/A'

		publications.append({
			'scholar_id': scholar_id,
			'title': title,
			'authors': authors,
			'publisher': publisher,
			'year': year,
			'citations': citations,
			'article_url': article_url,
			'article_id': article_id,
		})

	return publications

def get_citation_data(article_id, article_url):
	"""
	Scrape citation data for a given article ID.

	Args:
		article_id (str): Article ID of the publication.
		article_url (str): URL of the publication.

	Returns:
		dict: A dictionary containing citation data per year.
	"""
	url = f'https://scholar.google.com{article_url}'
	try:
		browser.get(url)
		time.sleep(delay_times_1)  # Wait for the page to load
		html = browser.page_source
		soup = BeautifulSoup(html, 'html.parser')

		citations_per_year = {}

		# Find the graph wrapper
		graph_bars = soup.find('div', id='gsc_oci_graph_bars')
		if not graph_bars:
			print(f"No graph bars found for {url}")
			return citations_per_year

		# Extract year labels and citation counts
		years = graph_bars.find_all('span', class_='gsc_oci_g_t')
		citation_bars = graph_bars.find_all('a', class_='gsc_oci_g_a')

		# Ensure consistent pairing
		for year, bar in zip(years, citation_bars):
			year_value = year.text.strip()
			citation_count = bar.find('span', class_='gsc_oci_g_al').text.strip()
			citations_per_year[year_value] = int(citation_count)

		return citations_per_year
	except Exception as e:
		print(f'Error accessing {url}: {e}')
		return {}

def main(input_file, output_file, using_samples=True, num_of_samples=3):
	"""
	Main function to scrape Google Scholar citation data.

	Args:
		input_file (str): Input file containing the scholar ids.
		output_file (str): Output file to save the citation data.
		using_samples (bool): Using samples or not.
		num_of_samples (int): Number of samples to use.
	"""
	# Check if the input file exists
	if not os.path.exists(input_file):
		print(f"Input file {input_file} not found.")
		return
	
	# Initialize the browser options
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')

	# Initialize the browser for scraping article list
	global browser 
	browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

	# Delay times
	global delay_times_1
	delay_times_1 = 1

	# Load the scholar data
	if using_samples:
		df_idgs = pd.read_excel(input_file)
		df_samples = df_idgs.sample(num_of_samples)
		print(f"Using number of samples: {num_of_samples}")
		for index, row in df_samples.iterrows():
			print(f"Using Dosen Name: {row['NAMA']} with Scholar ID: {row['scholar_id']}")
	else:
		df_samples = pd.read_excel(input_file)
		print(f"Using all data in {input_file}")

	# DataFrame to store the publication data per scholar id
	df_publications = pd.DataFrame(columns=['scholar_id', 'title', 'authors', 'publisher', 'year', 'num_of_citations'])

	# Loop through the scholar ids to get the publication data
	for index, row in tqdm(df_samples.iterrows(), total=df_samples.shape[0], desc="Getting publication data"):
		scholar_id = row['scholar_id']
		publications = get_publication_data(scholar_id)
		df_publications = pd.concat([df_publications, pd.DataFrame(publications)], ignore_index=True)

	# Close the browser
	browser.quit()

	# Initialize the browser for scraping citation data per article
	browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

	# DataFrame to store the citation data per article id
	df_citations = pd.DataFrame(columns=['article_id', 'year', 'num_of_citations'])

	# Loop through the article ids to get the citation data
	for index, row in tqdm(df_publications.iterrows(), total=df_publications.shape[0], desc="Getting citation data per article"):
		article_id = row['article_id']
		article_url = row['article_url']
		# print(f"Accessing article ID {article_id} from {article_url}")

		citations_per_year = get_citation_data(article_id, article_url)

		# Insert citation data into new DataFrame
		for year, citations in citations_per_year.items():
			df_citations = pd.concat([
				df_citations,
				pd.DataFrame({'article_id': [article_id], 'year': [year], 'num_of_citations': [citations]})
			], ignore_index=True)

	# Close the browser
	browser.quit()

	# Merge citation_infos_df with results_df on article_id
	merged_df = pd.merge(df_citations, df_publications, on='article_id', how='inner')

	# Join the merged_df with df_samples on scholar_id
	final_df = pd.merge(merged_df, df_samples, on='scholar_id', how='inner')

	# Save the final_df to a Excel file
	# Check first if the output file is an CSV file or not
	try:
		if not output_file.endswith('.csv'):
			raise ValueError("Output file must be a CSV file.")
		final_df.to_csv(output_file, index=False)
	except ValueError as e:
		print(f"Warning: {e}")
		print("Printing the first 5 rows of the DataFrame:")
		print(final_df.head())


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Scrape Google Scholar citation data.')
	parser.add_argument('--input_file', type=str, help='Input file containing the scholar ids')
	parser.add_argument('--output_file', type=str, help='Output file to save the citation data, should be CSV file')
	parser.add_argument('--using_samples', type=bool, default=True, help='Using samples or not, default is True')
	parser.add_argument('--num_of_samples', type=int, default=3, help='Number of samples to use, default is 3')
	
	if not parser.parse_args().input_file:
		parser.print_help()
		exit()
	
	if not parser.parse_args().output_file:
		parser.print_help()
		exit()

	if not parser.parse_args().using_samples:
		parser.print_help()
		exit()
	
	args = parser.parse_args()
	main(args.input_file, args.output_file, args.using_samples, args.num_of_samples)