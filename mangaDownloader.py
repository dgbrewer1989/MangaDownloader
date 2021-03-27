import sys, os, json, subprocess
from os import system
from typing import NamedTuple

ADDITIONAL_OPTIONS = '-z -W --wait-after-page 5 --max-threads 1'
MANGA_LIST_FILE = './mangaList.json'
MANGA_DOWNLOAD_PATH = 'C:\\Users\\bette\\Desktop'

class MangaToDownload(NamedTuple):
        name: str
        url: str

def runScanner():
    if os.path.isfile(MANGA_LIST_FILE) and os.stat(MANGA_LIST_FILE).st_size != 0:
        with open(MANGA_LIST_FILE) as data_file:
            try:
                jsonObj = json.load(data_file)
            except Exception as e:
                print(f"Unable to load JSON file. Exception: {(e)}")
                return
            for i in jsonObj:
                try:
                    subprocess.run(f"manga-py {i['url']} --name \"{i['name']}\" -d {MANGA_DOWNLOAD_PATH} {ADDITIONAL_OPTIONS}", check = True)
                except AttributeError as f:
                    print(f"Unable to download url {i['url']} and name {i['name']} through manga-py. specific AttributeError occured {(f)}")
                except Exception as e:
                    print(f"Unable to download url {i['url']} and name {i['name']} through manga-py. exception: {(e)} ")
    else:
        print(f"Error: {(MANGA_LIST_FILE)} file does not exist or is empty")

def loadAndAppendManga(newMangaToSave):
    with open(MANGA_LIST_FILE) as data_file:
        data = json.load(data_file)
        temp = data
        temp.append(newMangaToSave._asdict())
    
    with open(MANGA_LIST_FILE, 'w') as f:
        json.dump(data, f)

def addmanga():
    print("Enter the manga URL: ")
    mangaUrl = input(" >> ")
    print("Enter the manga name (Optional) : ")
    mangaName = input(" >> ")
    newMangaToSave = MangaToDownload(mangaName, mangaUrl)
    loadAndAppendManga(newMangaToSave)

def main_menu(argv):
   
    if len(argv) == 2:
        exec_menu(argv[1])
    else:
        os.system('clear')
        
        print("Welcome,\n")
        print("Please choose the menu you want to start:")
        print("1. Add Manga")
        print("2. Run Check")
        print("\n0. Quit")
        choice = input(" >>  ")
        exec_menu(choice)

    return

def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']([])
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']([])
    return

def exit():
    sys.exit()

menu_actions = {
    'main_menu': main_menu,
    '1': addmanga,
    '2': runScanner,
    '0': exit,
}

if __name__ == "__main__":
    try:
        import manga_py
    except Exception as e:
        print("Please install manga-py")
        raise

    if not os.path.isfile(MANGA_LIST_FILE):
        file = open(MANGA_LIST_FILE,"a")
        json.dump([], file)
        file.close()

    main_menu(sys.argv)
    print("Exiting..")