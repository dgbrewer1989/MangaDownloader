# MangaDownloader
 Small Python 3 script that utilizes [manga-py](https://github.com/manga-py/manga-py "manga-py") to download and maintain a list of manga series. As it is right now, this is soley used on a raspberry pi on my home network and runs via cron every few days.

## Usage ##
Currently from the main py file you can add a new entry to the JSON file used in this process, or run the checker to see if a new chapter exists for any series listed in the JSON file.

To run (and view a menu)
```
python3 mangaDownloader.py
```

To run with a predetermined selection (2 being the "Run Check" option)
```
python3 mangaDownloader.py 2
```

To add a manga to the list simply start the script, and select option 1. Follow the prompts from here. If no name is provided to the manga, it would use the default name that manga-py pulls from the provider.
```
Please choose the menu you want to start:
1. Add Manga
2. Run Check

0. Quit
Enter the manga URL:
 >> https://manganelo.com/manga/read_dragon_ball_manga_online_for_free2
Enter the manga name (Optional) :
 >> Dragon Ball
```

## Configuration ##
At the top of the mangaDownloader file is a series of configuration fields.

```
ADDITIONAL_OPTIONS = '--cbz --no-webp --wait-after-page 5 --max-threads 4'
MANGA_LIST_FILE = './mangaList.json'
MANGA_DOWNLOAD_PATH = 'C:\\Users\\bette\\Desktop'
```

ADDITIONAL_OPTIONS are specific manga-py parameters I've chosen, but they can be adjusted without any change to the process in this script. They're just used as a pass through to the manga-py call.

MANGA_LIST_FILE is the save location of the mangaList.json file which stores the name and URL of the manga being entered.

MANGA_DOWNLOAD_PATH just marks where the downloaded chapters should go. Note: this is a root path. All items from the JSON file will be saved under that path in named folders.

## Cron notes ##
The code in this repo is made to be ran outside of a cron but if you plan to use this on a cronjob, here are a few notes about my experiences with setting this script up to be ran using a cron.

#### My own crontab setup
```
0 */12 * * * /usr/bin/python3 /home/pi/MangaDownloader/mangaDownloader.py 2 2>&1 >> /home/pi/MangaDownloader/`date +\
%Y\%m\%d\%H\%M\%S`-cron.log
```
Ran once every 12 hours starting at 00:00, absolute path of python3 before calling the mangaDownloader file with "2" is the option at the menu so it will run through the mangaList.json file and check for updates. Beyond that `2>&1` redirects the error output to the same file as the info output (from my understanding) and just places that log file into a local directory with a timestamped cron log.


#### File paths and manga-py path need to be absolute

```
#file paths
MANGA_LIST_FILE = '/home/pi/MangaDownloader/mangaList.json'
MANGA_DOWNLOAD_PATH = "/media/pi/USB/share/manga"

#manga-py absolute path
call(f"/home/pi/.local/bin/manga-py {i['url']} --name \"{i['name']}\" -d {MANGA_DOWNLOAD_PATH} {ADDITIONAL_OPTIONS}", stderr=subprocess.STDOUT, shell=True)
```

In the `call` example above I also updated the `stderr` output to use `subprocess.STDOUT` so it would show up in the same log file as the rest of the output statements. 
