# LottoScript
The script will check winning numbers every Monday, Wednesday, and Friday at 9:00pm, and send an email to the account of
your choosing should you have a match of two or more numbers for any given draw.

## Use launchd to automate in Linux and MacOS

### lotto.py
Add your gmail account info and lotto numbers in the comment block at the top.

Save the file without a file extension.

### lottolist.plist
Change USERNAME to your username (or "home" folder name).

### To automate:
```
launchctl load ~/filepath
```
```
launchctl start lottolist
```
