import requests, re, sys
from bs4 import BeautifulSoup as bs
from pathlib import Path
from urllib.parse import urljoin
from pydash import arrays as _arrays
import humanize
import argparse

# config = {
#   'version': '1.0.0',
#   'description': 'Download media content from a given website.',
#   'prog': 'channer',
# }
# parser = argparse.ArgumentParser(**config)
# w = 3

def get_links(sup):
  global specific_filetypes
  sf = "|".join(specific_filetypes)
  link_re = re.compile(f"\.({sf})$")
  findit = lambda x: x.find_all(attrs={"href": link_re})
  lns = []
  for x in findit(sup):
    href = x.get("href")
    src = x.get("src")
    if href:
      href = urljoin(input_url, href)
    if src:
      src = urljoin(input_url, src)
    if href and href not in lns: lns.append(href)
    if src and src not in lns: lns.append(src)
  return list(set(lns))


def get_media_sources(url):
  r = s.get(url)
  soup = bs(r.text, 'html5lib')


def download_file(url, path="."):
  global total_dld
  local_filename = url.split("/")[-1]
  ext = local_filename.split(".")[-1]
  if ext not in specific_filetypes:
    print(f"Filetype: {local_filename} not in listed extensions! url: {url}")
    return
  ext_path = Path(path) / ext
  ext_path.mkdir(exist_ok=True)
  local_path = ext_path / local_filename
  if not local_path.is_file():
    with s.get(url, stream=True) as resp:
      cl = int(resp.headers["content-length"])
      total_dld += cl
      bsize = f'[{humanize.naturalsize(cl, binary=True)}]'
      print(f"Downloading {local_filename} {bsize}")
      resp.raise_for_status()
      with open(local_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
          if chunk:
            f.write(chunk)
    return local_filename
  else:
    print(f"Already downloaded {local_filename}! Skipping.")

if __name__ == "__main__":
  specific_filetypes = ["jpg", "png", "webm", "gif"]
  total_dld = 0
  input_url = sys.argv[-1]
  output_dir_name = input_url.replace("://", "_").replace(".", "_").replace("/", "-")
  output_dir = Path(output_dir_name)
  output_dir.mkdir(exist_ok=True)
  print(f"Downloading {specific_filetypes} from url: {input_url}")
  s = requests.Session()
  s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1'})
  s.verify = False
  r = s.get(input_url)
  soup = bs(r.text, 'html5lib')
  links = get_links(soup)
  print(f"Attempting to download {len(links)} things!")
  dls = _arrays.compact(list(map(lambda x: download_file(x, path=output_dir), links)))
  tsize = f'[{humanize.naturalsize(total_dld, binary=True)}]'
  print(f"Links found: {len(links)} Things Downloaded: {len(dls)} Amount Downloaded: {tsize}")



