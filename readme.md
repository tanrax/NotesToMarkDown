# Notes to MarkDown 

Exports the notes of the application Notes for MacOS, Fastmail... in Markdown.

## Requeriments

You will need to have installed python3. Then you will have to install dependencies.

``` bash
pip install -r requeriments.txt
```
## Use

Compatible with any account. You only need to know what the SMTP address of your email account. The following example would be using Gmail.

``` bash
python3 notes.py --imap imap.gmail.com --user my@gmail.com --password 123456
```
