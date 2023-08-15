import io
import os
import PyPDF2
import numpy as np
import camelot
import re
from PyPDF2 import PdfFileReader
import pandas as pd
import fitz
from PyPDF2 import PdfFileReader, PdfFileWriter

from PyPDF2 import PdfFileReader, PdfFileWriter

def add_version_to_pdf_name(file, merchant):
    #rename the file to END with the "_v{merchant}" string
    try:
        os.rename(file, file.replace(".pdf", f"_v{merchant}.pdf"))
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    return True

def check_mfa_for_free_subscription(file):
    stringg = "DNA MAF with Free Subscription Period"
    #get all text from the first page
    reader = PdfFileReader(open(file, mode='rb'))
    pageObj = reader.getPage(0)
    text = pageObj.extractText()
    #if the text contains "This Merchant Application Form (the MAF) relates to the provision of the Services"
    if stringg in text:
        #close the file
        reader.stream.close()
        return True
    reader.stream.close()
    return False


def get_form_type(file):
    '''return the form type from the first page of the PDF file
    1: "This Merchant Application Form (the MAF) relates to the provision of the Services" (2023-2021)
    2: '''
    #we open it to see what strings are detected. 
    #1: 2023-2021 "This Merchant Application Form (the MAF) relates to the provision of the Services", "This Merchant Application Form  (the MAF ) relates to the provision of the Services"
    #get all text from the first page
    reader = PdfFileReader(open(file, mode='rb'))
    pageObj = reader.getPage(0)
    text = pageObj.extractText()
    #if the text contains "This Merchant Application Form (the MAF) relates to the provision of the Services"
    if "This Merchant Application Form (the MAF) relates to the provision of the Services" in text or "This Merchant Application Form  (the MAF ) relates to the provision of the Services" in text or "This Application relates to the provision of the Services, subject to and in accordance with the terms and":
        #close the file
        reader.stream.close()
        return 1
    return KeyError("Form type not found")

#

def get_merchant_details(file):
    tables = camelot.read_pdf(file, pages='1')
    #get merchant name
    #get trander name
    #return in a list
    try:
        merchant_name = str(tables[0].df.iloc[1].replace(r'^\s*$', np.nan, regex=True).dropna().reset_index(drop=True)[1])
    except:
        merchant_name = ""
    try:
        trader_name = str(tables[0].df.iloc[2].replace(r'^\s*$', np.nan, regex=True).dropna().reset_index(drop=True)[1])
    except:
        trader_name = ""
    del tables
    return [merchant_name, trader_name]


def get_page_number_of_merchant_fees_table(file):
    '''return the page number where "4.2." is found'''
    list_of_mentions = []
    reader = PdfFileReader(open(file, mode='rb'))
    for page in range(reader.getNumPages()):
        pageObj = reader.getPage(page)
        text = pageObj.extractText()
        #find which page "4.2." is on
        #get the first page where "4.2." is found
        if "4.2." in text:
            list_of_mentions.append([page+1, 1])
        if "Acquiring Services:" in text:
            list_of_mentions.append([page+1, 2])

    reader.stream.close()
    #if the list is empty, return False
    if len(list_of_mentions) == 0:
        return([-1, 0])
    #if the list is not empty, return the list with the lowest page number
    return(min(list_of_mentions))
            

def get_merchant_fees_table(file, page_number,table_number):
    '''return the merchant fees table from the PDF file'''
    #using camelot, read the table from the page number returned by get_page_number_of_merchant_fees_table
    try:
        tables = camelot.read_pdf(file, pages=str(page_number))
        #return the first table
        return tables[table_number].df
    except:
        print("ERROR: table not found")
        return False


def find_table_number(file, page_number):
    #find the table within the file and page number
    #where a row contains "Transaction Fees", "Blended Rate", "Description"
    #return the table number
    try:
        tables = camelot.read_pdf(file, pages=str(page_number))
        for table in range(len(tables)):
            df = tables[table].df
            try:
                if "Type of Fee:" in df.values:
                            return table
            except:pass
            try:
                if "Transaction Fees" in df.values:
                    if "Blended Rate" in df.values:
                        if "Description" in df.values:
                            return table
            except:pass
    except:pass
    return(-1)


def cut_table(df):
    '''return the table without the rows before "Transaction Fees"'''
    for row in range(len(df[0])):
        #if the row contains "Transaction Fees"
        if df[0][row] == "Transaction Fees":
            #cut out all rows before and including "Transaction Fees" and only keep whatever is after
            table =  df[row+1:] 
            table = table.replace(r'\n',' ', regex=True)
            #reset the index
            table = table.reset_index(drop=True)
            return table
        


def get_name_and_table(file):
    '''return the merchant name and merchant fees table from the PDF file'''
    #merchant_name = str(get_merchant_name(file))
    page_number, pixely = get_page_number_of_merchant_fees_table(file)
    table_number = find_table_number(file, page_number)
    if table_number == 0:
        return False
    table = get_merchant_fees_table(file, page_number, table_number)
    if type(table) == bool:
        return False
    table = cut_table(table)
    table = table.rename(columns={0: 'Transaction Fees', 1: 'Blended Rate', 2: 'Description'})
    #table = string_split_by_category_df(table)
    return table




def table_cut_off(file):
    # Set page number and table number
    page_number  = get_page_number_of_merchant_fees_table(file)[0]
    print(page_number)
    table_number = find_table_number(file, page_number)

    # Extract tables from PDF file
    tables = camelot.read_pdf(file, pages=str(page_number))

    # Get table object
    table = tables[table_number]

    # Check if table is cut off to next page
    if table.parsing_report['order'] > 1:
        print('Table is cut off to next page')
    else:
        print('Table is not cut off to next page')

def get_table_details(file):
    page_number = None
    table_type = None
    is_cut_off = None
    table_number = None
    table = None

    list_of_mentions = []
    reader = PdfFileReader(open(file, mode='rb'))
    for page in range(reader.getNumPages()):
        pageObj = reader.getPage(page)
        text = pageObj.extractText()
        if "4.2." in text:
            list_of_mentions.append([page+1, 1])
        if "Acquiring Services:" in text:
            list_of_mentions.append([page+1, 2])

    reader.stream.close()

    if len(list_of_mentions) == 0:
        page_number = -1
        table_type = 0
    else:
        final = min(list_of_mentions)
        page_number = final[0]
        table_type = final[1]

    if page_number == -1:
        return [None, None, None, None, None]

    try:
        tables = camelot.read_pdf(file, pages=f"{str(page_number)},{str(page_number+1)}")
    except:
        return [page_number, table_number, table_type, table, None]


    try:
        for table_idx in range(len(tables)):
            df = tables[table_idx].df
            try:
                if "Type of Fee:" in df.values:
                    table_number = table_idx
                    table = df
            except:
                pass

            try:
                if "Transaction Fees" in df.values:
                    if "Blended Rate" in df.values:
                        if "Description" in df.values:
                            table_number = table_idx
                            table = df
            except:
                pass

            try:
                if "Pay by Bank" in df.values:
                    table_number = table_idx
                    table = df
                elif "Authorisation fee (per Transaction)" in df.values:
                    table_number = table_idx
                    table = df
                
                elif "Authorisation fee"  in df.values:
                    table_number = table_idx
                    table = df
            except:
                pass
    except:
        return [page_number, table_number, table_type, table, None]

    if table_number is None:return [page_number, table_number, table_type, table, None]

    if table_number == 0:return [page_number, table_number, table_type, table, None]

        
    if tables[table_number-1].parsing_report['order'] > 1:
        table = pd.concat([tables[table_number-1].df, table], ignore_index=True)
        is_cut_off = True
        print("Here 3")
    else:
        is_cut_off = False
        print("Here 4")

    return [page_number, table_number, table_type, table, is_cut_off]
