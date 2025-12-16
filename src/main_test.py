import unittest
from pathlib import Path

from src import main


class MediathekDownloaderTest(unittest.TestCase):
  def test_download_video(self) -> None:
    download_path = Path("src/test/test.mp4")
    main.download_video(
      "https://sportschau-dd.akamaized.net/weltweit/nfsk/2025/01/13/cfefa4c9-252d-403a-9743-1bb1f0b6e1d8/cfefa4c9-252d-403a-9743-1bb1f0b6e1d8_AVC-1080.mp4",
      download_path,
    )
    self.assertTrue(download_path.exists())

  def test_extract_urls_from_html(self) -> None:
    html_str = Path("src/test/MediathekViewWeb.html").read_text()
    url_dict = main.extract_urls_from_html(html_str)

    self.assertEqual(len(url_dict), 24)

  @unittest.skip
  def test_get_html(self) -> None:
    main.get_html(1)

  def test_post_process_filename(self) -> None:
    match = 'Enthüllungen (S01/E12) (Englisch)</div> <div class="mb-2 text-lg font-semibold">Beschreibung</div> <p class="text-neutral-900/80 dark:text-neutral-50/80">Harvey\n lässt ein alter Prozess nicht los. Er glaubt an einen Justizfehler und \nkämpft dafür, einen unschuldig Verurteilten aus dem Gefängnis zu \nbefreien.</p> <div class="mt-4 pt-4 border-t border-gray-500/50"><!----><!----> <div class="flex flex-wrap justify-between gap-x-12 gap-y-8"><div><h4 class="font-semibold mb-3">Qualität</h4> <div class="grid grid-cols-[repeat(2,auto)] gap-y-2 text-sm"><!----><span class="font-medium">HD</span> <span class="ml-1 font-normal">- ? MB</span><!----><span class="font-medium">SD</span> <span class="ml-1 font-normal">- ? MB</span><!----><span class="font-medium">LQ</span> <span class="ml-1 font-normal">- ? MB</span><!----> <!----></div></div> <div class="flex flex-wrap items-start gap-x-12 gap-y-8"><div><h4 class="flex items-center gap-4 font-semibold mb-3">Abspielen</h4> <div class="flex gap-x-2 font-bold"><!----><a class="action-btn svelte-1x3uipq" href="https://nrodlzdf-a.akamaihd.net/dach/zdf/25/10/251008_1755_sendung_sui/1/251008_1755_sendung_sui_a3a4_6660k_p37v17.mp4" '
    self.assertEqual(
      main.post_process_filename(match),
      "(S01-E12)_(Englisch)_Enthüllungen.mp4",
    )


if __name__ == "__main__":
  unittest.main()
