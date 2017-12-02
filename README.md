#############
# ScrapeBin #
#############

ScrapeBin is a standalone fire-and-forget tool to take advantage of Pastebin's scraping API to search for possible infosec leaks.  Currently the only criteria it takes into consideration is the number of e-mail addresses present in the paste.  It will then save only the e-mail addresses to a file.

Please Note: This software is highly tailored to my particular requirements.  You will need to review and modify the code in order to make it suit your needs!

##################
# Prerequisites  #
##################

First and foremost, you will need a PasteBin pro/lifetime pro account in order to use the scraping API.  Aside from that, the certifi and urllib3 libraries are both required in order to use this piece of software:

pip install certifi
pip install urllib3

##############
# Installing #
##############

Once the prerequisites are installed, just clone the repository:

git clone https://github.com/matt-sparrow/scrapebin.git

##############
# Deployment #
##############

This can be run within 'screen' or by itself.  The tool will create a copy of all the e-mails in files in the subdirectory 'pastes'.  The filename is that of the paste ID on PasteBin, but all other information is stripped out (everything but the e-mail addresses).  It works very well with sort/uniq to narrow down to unique e-mail addresses only.  I had issues with 'awk' hanging up on incredibly large files (> total system RAM).

$ sort -f *.txt | uniq -i > out

###########
# License #
###########

This project is licensed under the MIT License - see the LICENSE file for more info.
