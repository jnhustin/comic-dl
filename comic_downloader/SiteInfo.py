import re
import requests
from bs4 import BeautifulSoup

from comic_downloader.Utils import Utils
utils = Utils()


class SiteInfo():

  def __init__(self):
    self.site_settings = {
      'comicextra' : {
        'domain'         :  'www.comicextra.com',
        'image_regex'    :  '<img[^>]+src="([^">]+)"',
        'antibot'        :  False,
        'name_position'  :  3,
        'issue_position' :  4,
      },
      'www.mangahere.cc' : {
        'domain'         :  'www.mangahere.cc',
        'base_url'       :  'http://www.mangahere.cc/',
        'image_regex'    :  r'<img[^>]+src="([^">]+)"',
        'antibot'        :  False,
        'name_position'  :  4,
        'issue_position' :  5,
      },
      'www.mangareader.net' : {
        'domain'         :  'www.mangareader.net',
        'base_url'       :  'https://www.mangareader.net',
        'image_regex'    :  '<img[^>]+src="([^">]+)"',
        'antibot'        :  False,
        'name_position'  :  3,
        'issue_position' :  4,
      },
      'read_comic_online' : {
        'domain'        :  'readcomiconline.to',
        'image_regex'   :  r'stImages.push\(\"(.*?)\"\)\;',
        'antibot'       :  True,
        'name_position' :  4,
        'issue_regex'   :  r'[(\d)]+',
      },
    }


  def get_comic_details(self, url, filetype, domain_settings):
    split_url    =  url.split('/')
    comic_name   =  split_url[domain_settings['name_position']]
    issue_number =  self.get_issue_number(split_url, domain_settings['domain'])
    filename     =  f'{comic_name}_{issue_number}.{filetype}'

    return [comic_name, issue_number, filename]


  def get_issue_number(self, split_url, domain):
    if domain == 'readcomiconline.to':
      regex        =  self.site_settings['read_comic_online']['issue_regex']
      issue_number =  re.findall(regex, split_url[5])[0]
    else:
      issue_number = split_url[self.site_settings[domain]['issue_position']]

    return issue_number


  def get_image_links(self, response, domain_settings, session):
    domain = domain_settings['domain']

    if domain == self.site_settings['www.mangahere.cc']['domain']:
      image_links =  self.mangahere_images_links(response)
    elif domain == self.site_settings['www.mangareader.net']['domain']:
      image_links = self.mangareader_images_links(response)
    else:
      html    =  BeautifulSoup(response.content, 'html.parser')

      image_html_links =  re.findall(domain_settings['image_regex'], str(html))
      image_links      =  [ link for link in image_html_links if utils.is_url_valid(link)]
    return image_links


  def get_domain_settings(self, domain):
    return [v for k,v in self.site_settings.items() if v['domain'] == domain][0]


  def mangahere_images_links(self, response):

    session =  requests.Session()
    soup    =  BeautifulSoup(response.content, 'html.parser')

    # retrieve the <options> in page
    options =  soup.findAll('option')
    links   =  [ f'http:{option.get("value")}' for option in options ]
    # grab all img links
    regex        =  self.site_settings['www.mangahere.cc']['image_regex']
    images_links =  []

    for link in links:
      response  =  session.get(link)
      image_url =  re.findall(regex, response.text)[1]

      if utils.is_url_valid(image_url):
        images_links.append(image_url)

    return images_links


  def mangareader_images_links(self, response):
    setting =  self.site_settings['www.mangareader.net']
    session =  requests.Session()
    soup    =  BeautifulSoup(response.content, 'html.parser')

    # retrieve the <options> in page
    options  =  soup.findAll('option')
    links    =  [ f"{setting['base_url']}{option['value']}" for option in options]

    images_links = []
    for link in links:
      response = session.get(link)

      # we'll find only 1 image
      image_url = re.findall(setting['image_regex'], response.text)[0]
      if utils.is_url_valid(image_url):
        images_links.append(image_url)

    return images_links
