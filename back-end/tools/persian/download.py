from ftplib import FTP
import gzip
import shutil
import os
from visualize import persian_convert

ftp_host = "persiann.eng.uci.edu"
ftp_dir = "/CHRSdata/PDIRNow/PDIRNowdaily" 

ftp = FTP(ftp_host)
ftp.login()
ftp.cwd(ftp_dir)

files = ftp.nlst()

if not files:
    print("No PDIR-NOW files found.")
    ftp.quit()
    exit()

latest_file = files[-1]
print(f"Latest file found: {latest_file}")

local_gz = latest_file
local_bin = latest_file.replace(".gz", "")

with open(local_gz, "wb") as f:
    ftp.retrbinary(f"RETR {latest_file}", f.write)

ftp.quit()
print(f"Downloaded: {local_gz}")

with gzip.open(local_gz, 'rb') as f_in, open(local_bin, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)

print(f" Extracted: {local_bin}")

os.remove(local_gz)
print(f"Deleted compressed file: {local_gz}")

persian_convert(local_bin)

# files = [f for f in os.listdir('./') if os.path.isfile(os.path.join('./', f)) and f.endswith('.bin')]

# for file in files:
    # persian_convert(file)