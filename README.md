## Description
This a Python `click` script to add country codes to an existing contact list living in a `.vcf` file.

I was recently relocated to Germany, and I found out that all my contacts phone numbers were previously saved 
as local ones on my phone, meaning without the internation country code like (+49 Germany, +961 Lebanon, etc.).
However, for some social apps (like Whatsapp) it is required to have the international country codes to identify other 
users using that app. So, I made this script to transform my phone numbers to ones that are prefixed by
the country code, since doing it manually takes forever.

## Usage

You should have Python >= 3.7 installed.

**Prerequisite**: `pip install requirements.txt`

`python main.py -i path/to/input/.vcf/file -o path/to/output/.vcf/file -c YOUR_COUNTRY_CODE`

You can run `python main.py --help` to get more info.

## How to get the .vcf file?

On mac, you can open the Contacts app, select all contacts (w/ `cmd + A`), right click -> export vCard.
On gmail, follow [this](https://support.google.com/contacts/answer/7199294).

## Notes

Double check before importing the updated .vcf file. You can use online text-diff tools which highlight what 
was changed. 

This script does not handle numbers that are considered `hot lines` as they are strictly local and 
cannot be reached internationally, so upon inspection remove the country codes that were added by the script
for those numbers.

My implementation is based on vCard v3.0, backwards compatibility is not guaranteed.