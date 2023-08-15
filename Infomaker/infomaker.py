import os
import json, tqdm
from pdf_processing import *
import threading
from concurrent.futures import ThreadPoolExecutor

def get_merchant_details_thread(folder_path, variables):
    try:
        merchant_name, trader_name = get_merchant_details(os.path.join(folder_path, variables["file_name"]))
        variables["merchant_name"] = merchant_name
        variables["trader_name"] = trader_name
        return variables
    except Exception as e:
        print(f"Error getting merchant details in {folder_path}: {e}")

def get_table_details_thread(folder_path, variables):
    try:
        page_number, table_number, table_type, table, is_cut_off = get_table_details(os.path.join(folder_path, variables["file_name"]))
        variables["page_number"] = page_number
        variables["table_number"] = table_number
        variables["table_type"] = table_type
        variables["is_cut_off"] = is_cut_off
        return variables, table
    except Exception as e:
        print(f"Error getting table details in {folder_path}: {e}")

def save_table_to_csv_thread(folder_path, table):
    try:
        table.to_csv(os.path.join(folder_path, "table.csv"), index=False)
    except Exception as e:
        print(f"Error saving table.csv in {folder_path}: {e}")

def write_json(folder_path, variables):
    json_file_path = os.path.join(folder_path, "data.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(variables, json_file, indent=4)

def write_csv(folder_path, table):
    #check if table nontype
    try:
        csv_file_path = os.path.join(folder_path, "table.csv")
        table.to_csv(csv_file_path, index=False)
    except Exception as e:
        print(f"Error saving table.csv in {folder_path}: {e}")

# Define the directory where the folders are located
folders_path = 'folders'


# Iterate through the folders in the specified directory
for folder_name in tqdm.tqdm(os.listdir(folders_path)):
    folder_path = os.path.join(folders_path, folder_name)
    variables = {
        "file_name": "",
        "merchant_name": "",
        "trader_name": "",
        "page_number": "",
        "table_number": "",
        "table_type": "",
        "is_cut_off": "",
        
    }

    # Check if the path is a folder
    if os.path.isdir(folder_path):
        # Define the path for the JSON file inside the folder
        #get the pdf that is within the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                variables["file_name"] = filename
                break
        
        #if there is a csv file, skip
        if os.path.exists(os.path.join(folder_path, "table.csv")):
            continue

        # get the merchant name
        try:
            try:
                merchant_name, trader_name = get_merchant_details(os.path.join(folder_path, variables["file_name"]))
                variables["merchant_name"] = merchant_name
                variables["trader_name"] = trader_name
            except Exception as e:
                print(f"Error getting merchant details in {folder_path}: {e}")

            try:
                page_number, table_number, table_type, table, is_cut_off = get_table_details(os.path.join(folder_path, variables["file_name"]))
                variables["page_number"] = page_number
                variables["table_number"] = table_number
                variables["table_type"] = table_type
                variables["is_cut_off"] = is_cut_off
            except Exception as e:
                print(f"Error getting table details in {folder_path}: {e}")
            
            write_csv_thread = threading.Thread(target=write_csv, args=(folder_path, table))
            write_csv_thread.start()

        except Exception as e:
            print(f"Unexpected error in {folder_path}: {e}")

        write_thread = threading.Thread(target=write_json, args=(folder_path, variables))
        write_thread.start()

