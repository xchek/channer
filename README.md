# Channer
A media scraper for imageboards.

### Usage:
```
python channer.py https://website.com/path/to/board
```

### Output file structure:
```
$ python channer.py https://website.com/path/to/board
(test) testuser@the_host:~/test/channer$ python channer.py https://website.com/path/to/board
Downloading ['jpg', 'png', 'webm', 'gif'] from url: https://website.com/path/to/board
Attempting to download 14 things!
Downloading 1577456465452.jpg [1.3 MiB]
Downloading 4565542402661.png [199.7 KiB]
Downloading 9865461264911.gif [508.2 KiB]
Downloading 7326544608245.webm [712.0 KiB]
Downloading 1268506456482.gif [2.1 MiB]
Downloading 6546542253663.jpg [276.6 KiB]
Downloading 9879873216405.jpg [196.7 KiB]
Downloading 4654652119597.png [291.0 KiB]
Downloading 4578454598292.webm [2.4 MiB]
Downloading 5464623219879.png [357.3 KiB]
Downloading 4987987510028.webm [5.0 MiB]
Downloading 1577514654645.png [266.1 KiB]
Downloading 5467506456482.gif [503.5 KiB]
Downloading 4555524874446.webm [501.3 KiB]
Links found: 14 Things Downloaded: 14 Amount Downloaded: [13.3 MiB]
$ tree https_website_com-path-to-board/
https_website_com-path-to-board/
├── gif
│   ├── 1268506456482.gif
│   ├── 9865461264911.gif
│   └── 5467506456482.gif
├── jpg
│   ├── 1577456465452.jpg
│   ├── 6546542253663.jpg
│   └── 9879873216405.jpg
├── png
│   ├── 4654652119597.png
│   ├── 5464623219879.png
│   ├── 4565542402661.png
│   └── 1577514654645.png
└── webm
    ├── 4987987510028.webm
    ├── 4578454598292.webm
    ├── 7326544608245.webm
    └── 4555524874446.webm
```

### Install

`pip install -r requirements.txt`
