# coding: utf-8

import urllib2
import BeautifulSoup
import os
import subprocess
# Requires installed wkhtmltopdf

url = 'http://www.deeplearningbook.org/'
download_location = '~/Downloads/dl_book'

urls_to_download = list()

# Create download folder
if not os.path.exists(download_location):
    os.mkdir(download_location)

# Change directory to download location
os.chdir(download_location)

html = urllib2.urlopen(url).read()
soup = BeautifulSoup.BeautifulSoup(html)
links = soup.findAll('ul li a')

links = [i.find('a') for i in soup.find('ul').findAll('li')]

urls_to_download = list()
for index, link in enumerate(links):
    download_url = link.get('href')
    urls_to_download.append((index, download_url))

soup.close()

# Final Urls to download
urls_to_download

files_downloaded = list()


def download_link(link_tuple, force=False):
    index, link = link_tuple
    file_name = link.rsplit('contents/')[-1]
    out_file_name = file_name.replace('html', 'pdf')
    out_file_name_with_index = str(index) + '_' + out_file_name
    download_link = 'http://www.deeplearningbook.org/' + link
    global files_downloaded
    # print index, link, file_name, out_file_name,
    # print out_file_name_with_index, download_link

    if 'html' in link:
        print '------- DOWNLOADING STARTED -------'
        print 'File --> %s' % file_name

        # wget the file
        download_proc = subprocess.call(['wget', '-v', download_link, '-O', file_name], shell=False)

        if download_proc == 0 and os.path.exists(file_name):
            print '%s Html Downloaded.\nNow converting it to PDF' % file_name
            subprocess.call(['wkhtmltopdf', '--print-media-type', file_name, out_file_name_with_index], shell=False)
            print 'PDF Generated.\nDeleting Html version'
            os.remove(file_name)
            files_downloaded.append(out_file_name_with_index)
    print '------- DOWNLOADING COMPLETED -------\n'

for url in urls_to_download:
    download_link(url)

print '-------$$$ DOWNLOAD COMPLETED $$$-------'
