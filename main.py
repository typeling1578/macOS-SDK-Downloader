import requests
from tqdm import tqdm
import subprocess
import os
import shutil

print("Downloading Tools...")
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
result = requests.get("https://github.com/typeling1578/pbzx/releases/download/v1.0.2/pbzx", headers=headers, stream=True)
pbar = tqdm(total=int(result.headers["content-length"]), unit="B", unit_scale=True)
with open("./pbzx", "wb") as f:
    for chunk in result.iter_content(chunk_size=102400):
        f.write(chunk)
        pbar.update(len(chunk))
    f.close()
    pbar.close()
subprocess.call(["chmod", "+x", "./pbzx"])

print("Getting ADCDownloadAuth...")
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
result = requests.get(r"https://developerservices2.apple.com/services/download?path=%2FDeveloper_Tools%2FXcode_14%2FXcode_14.xip", headers=headers)
ADCDownloadAuth = result.cookies.get("ADCDownloadAuth")
print("ADCDownloadAuth: " + result.cookies.get("ADCDownloadAuth"))

print("Downloading Xcode Tool...")
headers = {
    "Referer": "https://developer.apple.com/download/all/",
    "Cookie": "ADCDownloadAuth=" + ADCDownloadAuth,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
result = requests.get("https://download.developer.apple.com/Developer_Tools/Command_Line_Tools_for_Xcode_14/Command_Line_Tools_for_Xcode_14.dmg", headers=headers, stream=True)
pbar = tqdm(total=int(result.headers["content-length"]), unit="B", unit_scale=True)
os.makedirs("./tmp", exist_ok=True)
with open("./tmp/tmp.dmg", "wb") as f:
    for chunk in result.iter_content(chunk_size=102400):
        f.write(chunk)
        pbar.update(len(chunk))
    f.close()
    pbar.close()

subprocess.call(["7z", "e", "-y", "tmp.dmg", "-i!Command Line Developer Tools/Command Line Tools.pkg"], cwd="./tmp")
subprocess.call(["7z", "e", "-y", "Command Line Tools.pkg", "-i!CLTools_macOSNMOS_SDK.pkg/Payload"], cwd="./tmp")

subprocess.call("../pbzx -n Payload | cpio -i", shell=True, cwd="./tmp")

shutil.move("./tmp/Library/Developer/CommandLineTools/SDKs/MacOSX12.3.sdk", "./MacOSX12.3.sdk")

shutil.rmtree("./tmp")
