import os
import csv
from datetime import datetime, timedelta

# Define paths
base_paths = {
    "DERIVITEC": r"//192.168.12.79/derivs/Bespoke/Derivitec/Reference/daily/",
    "XIGNITE": r"//192.168.12.79/derivs/Bespoke/Xignite/Reference/daily/",
    "BARCHART": r"//192.168.12.79/derivs/Bespoke/Barchart/Reference/daily/"
}

master_paths = {
    "DERIVITEC": r"//192.168.12.79/derivs/Bespoke/Derivitec/Reference/master/",
    "XIGNITE": r"//192.168.12.79/derivs/Bespoke/Xignite/Reference/master/",
    "BARCHART": r"//192.168.12.79/derivs/Bespoke/Barchart/Reference/master/"
}

# Define required exchanges and country codes
required_files = {
    "DERIVITEC": {
        "XEEE": "DE", "XMGE": "US", "XCBF": "US", "XCBT": "US", "XCEC": "US", 
        "XCME": "US", "XNYM": "US", "XMOD": "CA", "IFUS": "US", "BVMF": "BR", 
        "IFEU": "GB", "XMRV": "ES", "XOSE": "JP", "XLIS": "PT", "XMIL": "IT", 
        "XEUR": "DE", "XLME": "GB", "XEUE": "NL", "XWAR": "PL", 
        "XPAR": "FR", "XMAT": "FR", "NDEX": "NL", "XSES": "SG", "XIST": "TR", 
        "XSFA": "ZA", "XKLS": "MY", "XDCE": "CN", "XHKF": "HK", "XKRX": "KR", 
        "XNSE": "IN", "CCFX": "CN", "XZCE": "CN", "XTAF": "TW", "TFEX": "TH", 
        "XSGE": "CN"
    },
    "XIGNITE": {
        "XCME": "US", "XCBF": "US", "XMOD": "CA", "XCEC": "US", "XNYM": "US", 
        "IFUS": "US", "XHEL": "FI", "XSTO": "SE", "OPRA": "US", "XCBO": "US", 
        "IFEU": "GB", "XEUR": "DE", "XOSL": "NO", "XCBT": "US", "XMGE": "US"
    },
    "BARCHART": {
        "XMRV": "ES", "NDEX": "NL", "XKRX": "KR"
    }
}

# Suffixes to check (excluding 'err' ones)
valid_suffixes = ["NO_DIFF", "HOL", "NTD"]

# Get yesterday's date for filenames (e.g., 20250304)
yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y%m%d")

# Get today's date for the second field (e.g., 2025-03-05)
today_date = datetime.today().strftime("%Y-%m-%d")

# Define output file path
output_file = r"C:\Users\k.kaliagina\Desktop\Derivatives training\everyday forms\morning_check\morning_check_test.csv"

# Check if today is Monday
is_monday = datetime.today().weekday() == 0
print(f"Today is Monday? {is_monday}")  # DEBUG

# Prepare data for CSV
csv_data = []

for client, exchanges in required_files.items():
    csv_data.append([client, "Daily"])
    csv_data.append(["", today_date])  # Today's date in second field

    # Clone the original exchanges to avoid modifying required_files directly
    current_exchanges = exchanges.copy()

    # Add additional files only on Mondays
    if is_monday and client == "DERIVITEC":
        current_exchanges.update({"XKFE": "KR", "MISX": "RU"})  

    for exchange, country in current_exchanges.items():
        base_filename = f"{country}_{yesterday}_{exchange}_ref_delta"
        file_path = os.path.join(base_paths[client], base_filename)
        zip_file_path = f"{file_path}.zip"

        # Check for exact match
        if os.path.isfile(zip_file_path):
            csv_data.append([base_filename + ".zip", "V"])
        else:
            # If not found, search for valid suffixed versions
            found = False
            for suffix in valid_suffixes:
                suffixed_filename = f"{base_filename}_{suffix}.zip"
                suffixed_path = os.path.join(base_paths[client], suffixed_filename)
                
                if os.path.isfile(suffixed_path):
                    csv_data.append([suffixed_filename, "V"])
                    found = True
                    break
            
            # If nothing was found, mark as missing
            if not found:
                csv_data.append([base_filename + ".zip", "X"])
    
    # If today is Monday, check for the contract master file (with correct date)
    if is_monday:
        master_filename = f"{yesterday}_contract_master_file.zip"
        master_file = os.path.join(master_paths[client], master_filename)
        
        print(f"Checking for contract master file: {master_filename}")  # DEBUG
        if os.path.isfile(master_file):
            csv_data.append([master_filename, "V"])
            print(f"Found: {master_filename}")  # DEBUG
        else:
            csv_data.append([master_filename, "X"])
            print(f"Not Found: {master_filename}")  # DEBUG
    
    csv_data.append([])  # Empty row for separation

# Write to CSV
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"CSV report generated: {output_file}")


