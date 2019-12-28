import requests, re, humanize, click, time, random
from bs4 import BeautifulSoup as bs
from pathlib import Path
from urllib.parse import urljoin
from pydash import arrays as _arrays
from fake_useragent import UserAgent

# TODO: Functionality to specify filetypes to fetch
specific_filetypes = ["jpg", "png", "webm", "gif"]
ua = UserAgent()
s = requests.Session()
s.headers.update({
  'User-Agent': ua.random,
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Upgrade-Insecure-Requests': '1'})
s.verify = False
dl_ct, total_dld = 0, 0

@click.command()
@click.option('-o', '--output-dir', 'output_parent_dir',
              default='.',
              help='Specify the folder to create the output.')
@click.option('-w', '--wait', 'wait_time',
              default=None, nargs=2, type=int,
              help='Specify a range (in seconds) to wait between initiating each download.')
@click.argument('url')

def scrape_channel(url, output_parent_dir, wait_time):
  """
  :param url: [str] -

  :param wait_time: Optional[(A, B)] - A random time to wait in seconds between A and B.

  :param output_parent_dir: Optional[str] - Specified path in which to make the output.

  """
  global total_dld, dl_ct
  input_url = url
  output_dir_name = input_url.replace("://", "_").replace(".", "_").replace("/", "-")
  output_parent = Path(output_parent_dir)
  output_dir = output_parent / output_dir_name
  output_dir.mkdir(exist_ok=True)
  print(f"Downloading {specific_filetypes} from url: {input_url}")
  r = s.get(input_url)
  soup = bs(r.text, 'html5lib')
  links = get_links(input_url, soup)
  print(f"Attempting to download {len(links)} things!")
  try:
    dls = _arrays.compact(list(map(lambda x: download_file(x, path=output_dir, waiting_time=wait_time), links)))
  except:
    print("Stopping!")
  finally:
    print(f"Links found: {len(links)} Things Downloaded: {dl_ct} Amount Downloaded: "
          f"[{humanize.naturalsize(total_dld, binary=True)}]")

def get_links(url, soup):
  sf = "|".join(specific_filetypes)
  link_re = re.compile(f"\.({sf})$")
  findit = lambda x: x.find_all(attrs={"href": link_re})
  lns = []
  for x in findit(soup):
    href = x.get("href")
    if href:
      href = urljoin(url, href)
    if href and href not in lns: lns.append(href)
  return list(set(lns))

def download_file(url, waiting_time=None, path="."):
  global total_dld, dl_ct
  local_filename = url.split("/")[-1]
  ext = local_filename.split(".")[-1]
  if ext not in specific_filetypes:
    print(f"Filetype: {local_filename} not in listed extensions! url: {url}")
    return
  ext_path = Path(path) / ext
  ext_path.mkdir(exist_ok=True)
  local_path = ext_path / local_filename
  if not local_path.is_file():
    if waiting_time: time.sleep(random.uniform(*waiting_time))
    with s.get(url, stream=True) as resp:
      try:
        cl = int(resp.headers["content-length"])
      except:
        cl = None
      total_dld += cl
      # TODO: Get size if not supplied by headers
      print(f"Downloading {local_filename} [{humanize.naturalsize(cl, binary=True) if cl else 'N/A'}]")
      resp.raise_for_status()
      with open(local_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
          if chunk:
            f.write(chunk)
    dl_ct += 1
    return str(local_path)
  else:
    print(f"Already downloaded {local_filename}! Skipping.")

if __name__ == "__main__":
  scrape_channel()
