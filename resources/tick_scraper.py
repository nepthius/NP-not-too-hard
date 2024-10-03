def extract_and_save_ticker_name(input_file, output_file):
    ticker_name_list = []
    #open/read file
    with open(input_file, 'r') as file:
        #goes over each
        for line in file:
            # splits and extract
            columns = line.split('\t')
            if len(columns) >= 2:
                ticker = columns[0].strip()
                name = columns[1].strip()
                formatted_line = f"{ticker}:{name}"
                ticker_name_list.append(formatted_line)

    #writes to the file
    with open(output_file, 'w') as out_file:
        for item in ticker_name_list:
            out_file.write(item + '\n')


input_file = '../stocks.txt'  
output_file = 'formatted_ticker_name.txt' 


extract_and_save_ticker_name(input_file, output_file)
print(f"Saved to {output_file}")