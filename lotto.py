#!/usr/bin/python

import os, urllib2, sys, re, datetime, smtplib

#########################################
####### PUT IN YOUR STUFF HERE ##########

SEND_EMAIL = False
FROMADDR = "fromaddress@gmail.com"
TOADDRS  = ["toaddress@gmail.com"]
gmail_user = 'useraddress@gmail.com'
gmail_pwd = 'password' # leave the quotes in, just like the username above

myNums = "01 02 03 04 05"
myPowerball = "99"

#########################################
#########################################

def between_i(string, start='', end=''):
    """
    Iteratively find all string wrapped by start and end within a string.
    """
    # Used to store the results
    result = []
    
    # Iterate until there's no string found
    while True:
        # If no start is specified, start at the begining
        if not start:
            s = 0
        # Else find the first occurence of start
        else:
            s = string.find(start)
        # If end is empty, end at the ending
        if not end:
            e = len(string)
        # Else find the first occurence of end
        else:
            e = string.find(end)
        # Base case, if can't find one of the element, stop the iteration
        if s < 0 or e < 0:
            break
        # Append the result
        result.append(string[s+len(start):e])
        # Cut the string
        string = string[e+len(end):]
    return result

def get_htm_content():
    """ return the lotto site """
    url = "http://www.mdlottery.com/games/powerball/winning-numbers/"
    try:
        resp = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print >> sys.stderr, 'Failed to fetch (%s)' % url
    else:
        try:
            content = resp.read()
        except:
            content = []
    
    return content

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)
    


if __name__ == "__main__":

    winning_numbers = [[]]
    path =  os.path.dirname(os.path.abspath(__file__))
    #print path
    html = get_htm_content()
    #print html
    clean_html = remove_extra_spaces(html)
    #print clean_html
    nums  = between_i(clean_html, "valign=\"middle\"><strong>", "</strong></td>")
    bonus = between_i(clean_html, "bonus\">", "</strong>")
    dates = between_i(clean_html, "<td align=\"left\" valign=\"middle\">", "</td>")

    # clean up arrays
    i = 0
    while i < len(nums):
       if nums[i] == "":
          nums.pop(i)
       else:
          i += 1
    i = 0
    while i < len(bonus):
       if bonus[i] == "":
          bonus.pop(i)
       else:
          i += 1
    i = 0
    while i < len(dates):
       if dates[i] == "":
          dates.pop(i)
       else:
          i += 1

    powerball = []
    myNums.split()
    if nums:
        for i in range(0,len(nums)):
            winToday  = []
            numString = nums[i].split()
	    #print numString
            for j in range(0, 5):
                if numString[j] in myNums:
                    winToday.append(numString[j])
            if bonus[i] == myPowerball:
                powerball.append(True)
            else:
                powerball.append(False)
	    winning_numbers.append(winToday)
    winning_numbers.pop(0)
    
    if winning_numbers:
        output = ''
	for i in range(0, len(winning_numbers)):
            if len(winning_numbers[i]) > 1:
                SEND_EMAIL = True
	    output += "Matched %d numbers on %s: \n" % (len(winning_numbers[i]) ,dates[i])
            for j in range(0, len(winning_numbers[i])):
                output += winning_numbers[i][j] + '\n'
            if powerball[i] == True:
                output += "And you won the powerball!\n"
        if SEND_EMAIL:
            now        = datetime.datetime.now().isoformat().split('T')[0]
            SUBJECT    = 'Winning lotto numbers for %s' % now
            BODY       = output
	    email_text = """\  
	    From: %s  
	    To: %s  
	    Subject: %s

	    %s
	    """ % (FROMADDR, ", ".join(TOADDRS), SUBJECT, BODY)
            
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
                server.sendmail(FROMADDR, TOADDRS, email_text)
                server.close()
            except:
                print >> sys.stderr, 'Email failed, what you dun did?'
            else:
                print >> sys.stderr, email_text
        else:
            print >> sys.stderr, winning_numbers