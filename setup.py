from distutils.core import setup
setup(
  name = 'apiary2postman',
  packages = ['apiary2postman'], # this must be the same as the name above
  version = '0.3',
  description = 'A tool for converting Blueman API markup from Apiary.io to Postman collection/dumps',
  author = 'Erik Jonsson Thoren',
  author_email = 'thecopy@gmail.com',
  url = 'https://github.com/thecopy/apiary2postman', # use the URL to the github repo
  download_url = 'https://github.com/thecopy/apiary2postman/tarball/0.3', # I'll explain this in a second
  keywords = ['apiary', 'blueman', 'postman'], # arbitrary keywords
  classifiers = [],
)