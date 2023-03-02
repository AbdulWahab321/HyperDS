
from undeadupdater import Updater
import zipfile,os,logging,sys
 
def update(version):
    print(f"Configuring hyperDS@{version}...")
    updater = Updater("hyperDS",version,is_module=True)

    file,version = updater.get_update_file()
    if file:
        with zipfile.ZipFile(file) as f:
            f.extractall("./")
        print("Cleaning up...")
        os.remove(file)
        print("Please restart the program!")
