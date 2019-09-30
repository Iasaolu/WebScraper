import csv
import os
import numpy
import urllib2,json 

def check_valid(to_check):
	
	if (to_check[0] == "(" or to_check[-1] == ")"):
		return float(to_check[1:-1]) *-1
	elif to_check[0] == "-" and to_check[-1] != "-":
		to_check = float(to_check) * -1
	elif (to_check == "-" or to_check == "--"):
		return 0.0
	else:
		return float(to_check)



def find_ratio(numerator,denominator):
	if denominator < 1 or numerator < 1 or numerator == "N/A" or denominator == "N/A":
		return "N/A"
	else:
		try:
			return "{0:.2f}".format(float(numerator)/float(denominator))
		except ZeroDivisionError:
			return "N/A"
		except ValueError:
			return "N/A"

def find_difference(firstnum,secondnum):
	if firstnum == "N/A" or secondnum == "N/A":
		return "N/A"
	else:
		return float(firstnum) - float(secondnum)


def to_positive(to_change):
	if to_change < 0 and to_change != None:
		return to_change * -1
	else:
		return to_change


#get all prices
d  = {}
try:
	nseprices = ("http://www.nse.com.ng/rest/api/statistics/equities/?market=&sector=&orderby=&pageSize=1000&pageNo=0")
	connection = urllib2.urlopen(nseprices)
	raw_json = json.loads(connection.read())

	for de in raw_json:
		try:
			d[de["Symbol"]] = de["OpeningPrice"]
			s = float(de["OpeningPrice"])
		except TypeError as e:
			d[de["Symbol"]] = de["PrevClosingPrice"]
		#print(de["Symbol"] + " " + str(de["ClosePrice"]))
except urllib2.URLError as e: 
	pass


lowThresh = float(raw_input("Enter min percentage from annual low(decimal): "))
highThresh = float(raw_input("Enter max diff between annual low and high: "))
marginOfSafety = float(raw_input("Enter Margin of Safety: "))


#Perform analytics
directory_name = "Financials/"
all_financials = os.listdir(directory_name)
all_financials.remove('.DS_Store')

#index titles
item_name = 1
year_one = 2
year_two = 3
year_three = 4

#write text_file_results to files
text_file_results = open("Results.txt",'w+')
csv_file_results = open("Results.csv","wb")
res = open("UNDERVALUED.TXT","w")
csv_file_writer = csv.writer(csv_file_results)

for sheet_name in all_financials:
	company_name = sheet_name[:-4]
	#print company_name
	#company_symbol = raw_input("Enter Company Symbol: ")
	#filename = "Financials/"+company_symbol + ".csv"
	filename = directory_name+sheet_name
	financials = csv.reader(open(filename,'rU'))
	financial_data = list(financials)

	#get item names
	try:
		year_one_text = financial_data[42][year_one]
		year_two_text = financial_data[42][year_two]
		year_three_text = financial_data[42][year_three]

		net_assets_year_one = check_valid(financial_data[36][year_one].replace(",",""))
		net_assets_year_two = check_valid(financial_data[36][year_two].replace(",",""))
		net_assets_year_three = check_valid(financial_data[36][year_three].replace(",",""))

		net_income_year_one = check_valid(financial_data[57][year_one].replace(",",""))
		net_income_year_two = check_valid(financial_data[57][year_two].replace(",",""))
		net_income_year_three = check_valid(financial_data[57][year_three].replace(",",""))	

		total_assets_year_one = check_valid(financial_data[15][year_one].replace(",",""))
		total_assets_year_two = check_valid(financial_data[15][year_two].replace(",",""))
		total_assets_year_three = check_valid(financial_data[15][year_three].replace(",",""))
		
		total_current_assets_year_one = check_valid(financial_data[8][year_one].replace(",",""))
		total_current_assets_year_two = check_valid(financial_data[8][year_two].replace(",",""))
		total_current_assets_year_three = check_valid(financial_data[8][year_three].replace(",",""))

		total_current_liabilities_year_one = check_valid(financial_data[22][year_one].replace(",",""))
		total_current_liabilities_year_two = check_valid(financial_data[22][year_two].replace(",",""))
		total_current_liabilities_year_three = check_valid(financial_data[22][year_three].replace(",",""))
		
		total_dividends_paid_year_one = to_positive(check_valid(financial_data[106][year_one]))
		total_dividends_paid_year_two = to_positive(check_valid(financial_data[106][year_two]))
		total_dividends_paid_year_three = to_positive(check_valid(financial_data[106][year_three]))
		
		total_liabilities_year_one = check_valid(financial_data[28][year_one].replace(",",""))
		total_liabilities_year_two = check_valid(financial_data[28][year_two].replace(",",""))
		total_liabilities_year_three = check_valid(financial_data[28][year_three].replace(",",""))
		
		total_no_of_shares_year_one = check_valid(financial_data[38][year_one].replace(",",""))
		total_no_of_shares_year_two = check_valid(financial_data[38][year_two].replace(",",""))
		total_no_of_shares_year_three = check_valid(financial_data[38][year_three].replace(",",""))
		

		total_revenue_year_one = check_valid(financial_data[44][year_one].replace(",",""))
		total_revenue_year_two = check_valid(financial_data[44][year_two].replace(",",""))
		total_revenue_year_three = check_valid(financial_data[44][year_three].replace(",",""))

	except IndexError as e:
		pass
	
	try:
		#share_price = check_valid(financial_data[0][1])
		#get share price 
		try:
			share_price = (d[company_name])
		except KeyError as e:
			share_price  = check_valid(financial_data[0][1])
			# print ("\nKey error for  " + company_name + " FT price used instead\n")

		annual_high = financial_data[0][2]
		annual_low = financial_data[0][3]
	except IndexError as e:
		annual_high = "N/A"
		annual_low = "N/A"
		# print "Error at %s\n"%(company_name)

	

	#print financial_data[44][item_name]

	#Ratios
	book_value_per_share_year_one = find_ratio(net_assets_year_one,total_no_of_shares_year_one)
	book_value_per_share_year_two = find_ratio(net_assets_year_two,total_no_of_shares_year_two)
	book_value_per_share_year_three = find_ratio(net_assets_year_three,total_no_of_shares_year_three)

	current_ratio_year_one = find_ratio(total_current_assets_year_one,total_current_liabilities_year_one)
	current_ratio_year_two = find_ratio(total_current_assets_year_two,total_current_liabilities_year_two)
	current_ratio_year_three = find_ratio(total_current_assets_year_three,total_current_liabilities_year_three)

	debt_ratio_year_one = find_ratio(total_assets_year_one,total_liabilities_year_one)
	debt_ratio_year_two = find_ratio(total_assets_year_two,total_liabilities_year_two)
	debt_ratio_year_three = find_ratio(total_assets_year_three,total_liabilities_year_three)

	dividend_yield_year_one = find_ratio((find_ratio(total_dividends_paid_year_one,total_no_of_shares_year_one)),share_price)
	dividend_yield_year_two = find_ratio((find_ratio(total_dividends_paid_year_two,total_no_of_shares_year_two)),share_price)
	dividend_yield_year_three = find_ratio((find_ratio(total_dividends_paid_year_three,total_no_of_shares_year_three)),share_price)

	earnings_per_share_year_one = find_ratio(net_income_year_one,total_no_of_shares_year_one)
	earnings_per_share_year_two = find_ratio(net_income_year_two,total_no_of_shares_year_two)
	earnings_per_share_year_three = find_ratio(net_income_year_three,total_no_of_shares_year_three)

	net_margin_year_one = find_ratio(net_income_year_one,total_revenue_year_one)
	net_margin_year_two = find_ratio(net_income_year_two,total_revenue_year_two)
	net_margin_year_three = find_ratio(net_income_year_three,total_revenue_year_three)


	p_e_ratio_year_one = find_ratio(share_price,earnings_per_share_year_one)
	p_e_ratio_year_two = find_ratio(share_price,earnings_per_share_year_two)
	p_e_ratio_year_three = find_ratio(share_price,earnings_per_share_year_three)


	price_to_book_year_one = find_ratio(share_price,book_value_per_share_year_one)
	price_to_book_year_two = find_ratio(share_price,book_value_per_share_year_two)
	price_to_book_year_three = find_ratio(share_price,book_value_per_share_year_three)

	return_on_assets_year_one = find_ratio(net_income_year_one,total_assets_year_one)
	return_on_assets_year_two = find_ratio(net_income_year_two,total_assets_year_two)
	return_on_assets_year_three = find_ratio(net_income_year_three,total_assets_year_three)

	return_on_equity_year_one = find_ratio(earnings_per_share_year_one,book_value_per_share_year_one)
	return_on_equity_year_two = find_ratio(earnings_per_share_year_two,book_value_per_share_year_two)
	return_on_equity_year_three = find_ratio(earnings_per_share_year_three,book_value_per_share_year_three)

	margin_of_safety_year_one = find_difference(1,price_to_book_year_one)
	margin_of_safety_year_two = find_difference(1,price_to_book_year_two)
	margin_of_safety_year_three =find_difference(1,price_to_book_year_three)	

	#share price relationships
	relationship_to_high = find_ratio(share_price,annual_high)
	relationship_to_low = find_ratio(share_price,annual_low)
	relationship_to_book = find_ratio(share_price,book_value_per_share_year_three)


	try:
		text_file_results.writelines("\n")
		text_file_results.writelines("%s %s %s %s" % (company_name,year_three_text,year_two_text,year_one_text))
		text_file_results.writelines("\nAnnual Low: %s Annual High: %s Current Price: %s" % (annual_low,annual_high,share_price))
		text_file_results.writelines("\nBook Value: %s %s %s \nEPS: %s %s %s \n" %(book_value_per_share_year_three,book_value_per_share_year_two,book_value_per_share_year_one,earnings_per_share_year_three,earnings_per_share_year_two,earnings_per_share_year_one))
		text_file_results.writelines("ROE: %s %s %s \nROA: %s %s %s \n"%(return_on_equity_year_three,return_on_equity_year_two,return_on_equity_year_one,return_on_assets_year_three,return_on_assets_year_two,return_on_assets_year_one))
		text_file_results.writelines("Dividend Yield: %s %s %s \nNet Margin: %s %s %s \n"%(dividend_yield_year_three,dividend_yield_year_two,dividend_yield_year_one,net_margin_year_three,net_margin_year_two,net_margin_year_one))
		text_file_results.writelines("Debt Ratio: %s %s %s \nCurrent Ratio: %s %s %s \n"%(debt_ratio_year_three,debt_ratio_year_two,debt_ratio_year_one,current_ratio_year_three,current_ratio_year_two,current_ratio_year_one))
		text_file_results.writelines("P/E Ratio: %s %s %s \nP/Book: %s %s %s \n" % (p_e_ratio_year_three,p_e_ratio_year_two,p_e_ratio_year_one,price_to_book_year_three,price_to_book_year_two,price_to_book_year_one))
		text_file_results.writelines("Margin of Safety: %s %s %s \n"%(margin_of_safety_year_three,margin_of_safety_year_two,margin_of_safety_year_one))

		csv_file_writer.writerow([company_name])
		csv_file_writer.writerow(["","","Price",share_price])
		csv_file_writer.writerow(["","","Annual High",annual_high])
		csv_file_writer.writerow(["","","Annual Low",annual_low])
		csv_file_writer.writerow(["","Book Value",book_value_per_share_year_three,book_value_per_share_year_two,book_value_per_share_year_one])		
		csv_file_writer.writerow(["","",year_three_text,year_two_text,year_one_text])
		csv_file_writer.writerow(["","EPS",earnings_per_share_year_three,earnings_per_share_year_two,earnings_per_share_year_one])
		csv_file_writer.writerow(["","Return on Equity",return_on_equity_year_three,return_on_equity_year_two,return_on_equity_year_one])
		csv_file_writer.writerow(["","Return on Assets",return_on_assets_year_three,return_on_assets_year_two,return_on_assets_year_one])
		csv_file_writer.writerow(["","Dividend Yield",dividend_yield_year_three,dividend_yield_year_two,dividend_yield_year_one])
		csv_file_writer.writerow(["","Net Margin",net_margin_year_three,net_margin_year_two,net_margin_year_one])
		csv_file_writer.writerow(["","Debt Ratio",debt_ratio_year_three,debt_ratio_year_two,debt_ratio_year_one])
		csv_file_writer.writerow(["","Current Ratio",current_ratio_year_three,current_ratio_year_two,current_ratio_year_one])
		csv_file_writer.writerow(["","P/E Ratio",p_e_ratio_year_three,p_e_ratio_year_two,p_e_ratio_year_one])
		csv_file_writer.writerow(["","P/Book",price_to_book_year_three,price_to_book_year_two,price_to_book_year_one])
		csv_file_writer.writerow(["","Margin of Safety",margin_of_safety_year_three,margin_of_safety_year_two,margin_of_safety_year_one])
		csv_file_writer.writerow([' '])

		difflow = abs(float(share_price) - float(annual_low))/float(annual_low) <= lowThresh
		diffhigh = abs(float(annual_high) - float(annual_low))/float(annual_high) >= highThresh
		netnet = (float(book_value_per_share_year_three) - float(share_price))/float(book_value_per_share_year_three) > marginOfSafety

		if (difflow and diffhigh and netnet):
			res.write(company_name + " " + str(share_price) + " " + str(book_value_per_share_year_three) + " " + str(annual_low) + "\n")
			print(company_name + " " + str(share_price) + " Low: " + str(annual_low) + " High: " + str(annual_high) + " Book Val: " + str(book_value_per_share_year_three) +"\n")

		#print general analytics
		with open ("general.txt","a") as f:
			f.writelines("\n" + company_name + " Rel to high: " + relationship_to_high + " Rel to Low: " + relationship_to_low + " Rel to Book: " + relationship_to_book)
		# print("\n" + company_name + " Rel to high: " + relationship_to_high + " Rel to Low: " + relationship_to_low + " Rel to Book: " + relationship_to_book)

	except ValueError as e:
		pass
	except TypeError as e:
		pass
		# print ("Type error at " + company_name)

res.close()
text_file_results.close()
csv_file_results.close()





























