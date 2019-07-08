import validators
from urllib.parse import urlsplit



def is_url_valid(url):
  """
  :param string url: is a url

  check if the given url is valid and is not a gif
  """
  is_valid = not url.endswith('.gif') and validators.url(url)
  return is_valid

def get_url_domain(url):
  """
      parses url for the domain name
  """

  scheme, domain, path, query, fragment = urlsplit(url)

  # print('scheme: ', scheme)
  # print('domain: ', domain)
  # print('path: ', path)

  return domain