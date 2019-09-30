import urllib2
from bs4 import BeautifulSoup
import json
ccimport os

def write_to_file(items_to_write):
	filewriter.writerow(items_to_write)

#Get Symbols from NSE
nse_url = "http://www.nse.com.ng/rest/api/issuers/companydirectory?" 
raw_data = urllib2.urlopen(nse_url)
nse_html = raw_data.read()
parsed_json = json.loads(nse_html)
symbols_array = []
for item in parsed_json:
	symbols_array.append([item['Symbol'],item['StockPriceCur'],item['LOW52WK_PRICE'],item['HIGH52WK_PRICE']])

#company_symbol = raw_input("Company Symbol: ")
accounts_to_get = ["BalanceSheet","IncomeStatement","CashFlow"]



for company_symbol in symbols_array:
	price = company_symbol[1]
	annual_high = company_symbol[2]
	annual_low = company_symbol[3]
	company_symbol = company_symbol[0]    	

	filename = "Financials/"+company_symbol + ".csv"
	f = open(filename,"wb")
	filewriter = csv.writer(f)	

	if company_symbol == "BETAGLAS":
		company_symbol = "DELTGLAS"

	print company_symbol
	for account_to_get in accounts_to_get:
		ft_url = "http://markets.ft.com/data/equities/tearsheet/financials?s=%s:LAG&subview=%s" %(company_symbol,account_to_get)

		#fetch raw html data
		connection = urllib2.urlopen(ft_url)
		raw_html = connection.read()

		#parsing
		soup = BeautifulSoup(raw_html, 'html.parser')
		data_table = soup.findAll("table", { "class" : "mod-ui-table" }) #gets table containing selected financials

		if len(data_table) > 0:
			#print account_to_get
			write_to_file([account_to_get,price,annual_low,annual_high])

			table_rows = data_table[0].findAll("tr")

			for row in table_rows:
				row_to_write = ['']
				for child in row.children:
					row_to_write.append(child.text)
				write_to_file(row_to_write)
			write_to_file([' '])
		else:
			os.remove(filename) 
			print "Note!"			
			break


	#row_to_write = data_table[0].find("t")
f.close()







