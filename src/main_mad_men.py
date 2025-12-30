import logging
import re
from pathlib import Path

import enlighten
import requests

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)
LOG = logging.getLogger(__name__)
OUTPUT_DIR = Path("/mnt/hdd/Bilder-Videos/Filme/mad_men")
LOG.setLevel(logging.INFO)


def post_process_filename(text: str) -> str:
  filename = text.split("</div>")[0]
  filename = filename.rstrip()

  return filename.replace(" ", "_").replace("/", "-").replace("&", "--") + ".mp4"


def extract_urls_from_html(html: str) -> dict[str, str]:
  result = {}
  for match in re.findall(
    r'<div class="mb-4 text-lg font-bold">(.*?)title="HD abspielen',
    string=html,
    flags=re.MULTILINE | re.DOTALL,
  ):
    name = post_process_filename(match)
    urls = re.findall(r'href="https://arteptweb-a.akamaihd.net/.*"', match)

    if len(urls) != 1:
      raise RuntimeError
    url = urls[0].split("href=")[1].replace('"', "")
    if name in result and result[name] != url:
      raise RuntimeError

    result[name] = url

  return result


def download_video(url: str, local_file: Path) -> None:
  LOG.info("Downloading %s to %s \n", url, local_file)
  if not local_file.parent.exists():
    msg = "The parent directory does not exist: "
    raise FileNotFoundError(msg, local_file.parent.absolute())
  local_file.touch()
  # 1. Open the connection with streaming enabled
  with requests.get(url, stream=True, timeout=10) as response:
    content_length = response.headers["Content-Length"]

    manager = enlighten.get_manager()

    pbar = manager.counter(
      total=int(content_length) // 8192,
      desc="Downloading",
      unit="8MB",
    )

    response.raise_for_status()  # Check for errors (404, 500, etc.)

    with open(local_file, "wb") as f:  # noqa: PTH123
      for chunk in response.iter_content(chunk_size=8192):
        pbar.update()
        if chunk:  # Filter out keep-alive new chunks
          f.write(chunk)
  LOG.info("Download complete: %s", local_file)


def main_mad_men() -> None:
  for html in ("src/test/mad_men2.html", "src/test/mad_men1.html"):
    urls = extract_urls_from_html(Path(html).read_text())
    print(urls)
    for filename, url in urls.items():
      video_path = OUTPUT_DIR / filename
      if video_path.exists():
        LOG.info("Skipping %s", filename)
        continue

      download_video(url, video_path)


if __name__ == "__main__":
  main_mad_men()
