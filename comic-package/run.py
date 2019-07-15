# pip modules
import os, sys, glob, requests
from natsort  import natsorted

# package modules
from utils        import is_url_valid, get_url_domain
from WebScraper   import Scraper
from SiteInfo     import SiteInfo
from FileManager  import FileManager

site_info    =  SiteInfo()
scraper      =  Scraper()
file_manager =  FileManager()



def run():
  try:
    command, url, filetype = sys.argv
  except ValueError as e:
    print(f'error: {e}\nto run: python3 comic_request.py website')
    return

  # figure out which site settings to use
  domain          =  get_url_domain(url)
  domain_settings =  site_info.get_domain_settings(domain)

  # build comic name
  comic_name, issue_number, filename = site_info.get_comic_details(url, filetype, domain_settings)

  # bypass bot-protection
  response = scraper.scrape_comic(url, antibot=domain_settings['antibot'])

  # handoff to corresponding site-parser, returns array of image links
  session     =  requests.Session()
  image_links =  site_info.get_image_links(response, domain_settings, session)

  # download images
  scraper.download_images(comic_name, issue_number, image_links, session)

  # regroup images & sort to avoid a bad pagination
  unsorted_images =  [ image for image in glob.glob(f'{file_manager.full_temp_path}/*.jpg') ]
  images          =  natsorted(unsorted_images)

  # separate downloads into individual dirs
  series_dir        =  file_manager.create_and_get_series_dir(comic_name)
  download_location =  file_manager.get_download_location(series_dir, filename)

  # create pdf/cbz
  if filetype == 'pdf':
    file_manager.create_pdf(download_location, images)
  elif filetype == 'cbz':
    file_manager.create_cbz(download_location, images)

  # cleanup
  file_manager.remove_temp_dir()
  print('Comic successfully downloaded')


if __name__ == "__main__":
  run()
