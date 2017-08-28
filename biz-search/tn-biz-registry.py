import urllib
import urllib2
from cookielib import CookieJar

uri = 'https://tnbear.tn.gov/ECommerce/FilingSearch.aspx'
contrlnumbr = '000000002'

#the http headers are useful to simulate a particular browser (some sites deny
#access to non-browsers (bots, etc.)
#also needed to pass the content type.
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookies': {
        'ASP.NET_SessionId': 'hwilduqnpnun3nbtylmjwtcq',
        'NID': 'ZbvZWExhZF7SDXerZLJVLGwlphDg11I8EwOTXgoz2XqJXL8ppG1nzgGAw3U9Cl9Qhifjl6HMOB',
        '_ga': 'GA1.2.1645633929.1503691152'

    }
}

# we group the form fields and their values in a list (any
# iterable, actually) of name-value tuples.  This helps
# with clarity and also makes it easy to later encoding of them.

formFields = (
    # the viewstate is actualy 800+ characters in length! I truncated it
    # for this sample code.  It can be lifted from the first page
    # obtained from the site.  It may be ok to hardcode this value, or
    # it may have to be refreshed each time / each day, by essentially
    # running an extra page request and parse, for this specific value.
    #(r'__VSTATE', r'7TzretNIlrZiKb7EOB3AQE ... ...2qd6g5xD8CGXm5EftXtNPt+H8B'),

    # following are more of these ASP form fields
    (r'__EVENTTARGET', r''),
    (r'__EVENTARGUMENT', r''),
    #(r'__VIEWSTATE', r'/wEPDwULLTIwMTA3MzEzNDkPFgQeDVNlYXJjaFJlcXVlc3QypQcAAQAAAP////8BAAAAAAAAAAwCAAAAR0NPUkVfRGF0YU9iamVjdHMsIFZlcnNpb249Mi4zLjYuMSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAkQ09SRS5Nb2RlbC5EYXRhT2JqZWN0cy5TZWFyY2hSZXF1ZXN0AgAAAAR0eXBlCnBhcmFtZXRlcnMEBCFDT1JFLk1vZGVsLkRhdGFPYmplY3RzLlNlYXJjaFR5cGUCAAAAKUNPUkUuTW9kZWwuRGF0YU9iamVjdHMuTWV0YURhdGFDb2xsZWN0aW9uAgAAAAIAAAAJAwAAAAkEAAAABQMAAAAhQ09SRS5Nb2RlbC5EYXRhT2JqZWN0cy5TZWFyY2hUeXBlCwAAABw8RGlzcGxheU5hbWU+a19fQmFja2luZ0ZpZWxkHTxBc3NlbWJseU5hbWU+a19fQmFja2luZ0ZpZWxkGTxUeXBlTmFtZT5rX19CYWNraW5nRmllbGQlPFVzZXJIYXNSaWdodFRvU2VhcmNoPmtfX0JhY2tpbmdGaWVsZBM8SUQ+a19fQmFja2luZ0ZpZWxkJjxTZWFyY2hSZXF1ZXN0VHlwZV9LZXk+a19fQmFja2luZ0ZpZWxkGzxEQl9TUF9OYW1lPmtfX0JhY2tpbmdGaWVsZCQ8Q2xvc2VPblNpbmdsZVJlc3VsdD5rX19CYWNraW5nRmllbGQXPFBhcmVudD5rX19CYWNraW5nRmllbGQkPEhpZGVVbmxlc3NSZXF1ZXN0ZWQ+a19fQmFja2luZ0ZpZWxkHjxNYXhTZWFyY2hSb3dzPmtfX0JhY2tpbmdGaWVsZAEBAQAAAQEAAgAAAQgBAQgCAAAABgUAAAAHRmlsaW5ncwYGAAAAFkFNX0JFQVJfU2VhcmNoQ29udHJvbHMGBwAAACpBTV9CRUFSLlZpZXcuU2VhcmNoQ29udHJvbHMuU0VBUkNIX0ZJTElOR1MBDAAAAAYIAAAAElNFQVJDSF9GSUxJTkdTX1dFQgYJAAAAFnVzcF9YbWxTZWFyY2hGaWxpbmdXZWIBCgAAAAAABQQAAAApQ09SRS5Nb2RlbC5EYXRhT2JqZWN0cy5NZXRhRGF0YUNvbGxlY3Rpb24DAAAACkZJTElOR19OVU0LRklMSU5HX05BTUULQUNUSVZFX09OTFkBAQECAAAABgoAAAAJMDAwMDAwMDAyBgsAAAAABgwAAAABTgseB1BhZ2VOdW0CARYCZg9kFgZmD2QWBAITDxUJFi9pbmNsdWRlcy9tb2Rlcm5penIuanMdL2luY2x1ZGVzL2pxdWVyeS0xLjMuMi5taW4uanMnL2luY2x1ZGVzL2pxdWVyeS11aS0xLjcuMy5jdXN0b20ubWluLmpzGy9pbmNsdWRlcy9qcXVlcnkudG9vbHRpcC5qcx0vaW5jbHVkZXMvanF1ZXJ5LXRleHRyYW5nZS5qcx0vaW5jbHVkZXMvYnJvd3NlckZ1bmN0aW9ucy5qcx4vaW5jbHVkZXMvdWkuZGF0ZXBpY2tlci5taW4uanMdL2luY2x1ZGVzL0N1c3RvbUF0dHJpYnV0ZXMuanMXL2luY2x1ZGVzL1ZhbGlkYXRpb24uanNkAhQPFQwbL0NvbW1vbi9Db250cm9sTnVtSW5mby5hc3B4JS9Db21tb24vQ29udHJvbE51bUluZm8uYXNweD9vcGVuTmV3PVkfL0NvbW1vbi9Db252ZW5pZW5jZUZlZUluZm8uYXNweBgvQ29tbW9uL0NhcHRjaGFJbmZvLmFzcHggL1dDL1dlYlBhcnRzL0NvbnRyb2xOdW1JbmZvLmFzcHgqL1dDL1dlYlBhcnRzL0NvbnRyb2xOdW1JbmZvLmFzcHg/b3Blbk5ldz1ZHi9XQy9XZWJQYXJ0cy9TdGF0ZUxpY0luZm8uYXNweBIvVE0vVE1XYXJuaW5nLmFzcHgaL1dDL1dlYlBhcnRzL0ZFSU5JbmZvLmFzcHgZL0NvbW1vbi9EaXNzb2x2ZUluZm8uYXNweBsvQ29tbW9uL1BheW1lbnRNZXRob2RzLmFzcHgkL0NvbW1vbi9EZXRhaWxzRm9yZWlnbkV4aXN0YW5jZS5hc3B4ZAIDD2QWAgIBD2QWIAIBD2QWAgIBDw8WAh4EVGV4dAW1AUFzIG9mIEF1Z3VzdCAyNSwgMjAxNyB3ZSBoYXZlIHByb2Nlc3NlZCBhbGwgY29ycG9yYXRlIGZpbGluZ3MgcmVjZWl2ZWQgaW4gb3VyIG9mZmljZSB0aHJvdWdoIEF1Z3VzdCAyMywgMjAxNyBhbmQgYWxsIGFubnVhbCByZXBvcnRzIHJlY2VpdmVkIGluIG91ciBvZmZpY2UgdGhyb3VnaCBBdWd1c3QgMjQsIDIwMTcuICBkZAIDDxYCHgdWaXNpYmxlaGQCBQ8WAh8DZ2QCBw8PFgIfA2hkZAIJDw8WAh8DaGRkAgsPDxYEHwIFCDEtMSBvZiAxHwNnZGQCDQ8PFgIfA2hkZAIPDw8WAh8DaGRkAhsPFgIfA2hkAh8PFgIfA2gWBAIBDxYCHglpbm5lcmh0bWwFlwE8Zm9udCBjb2xvcj0ncmVkJz5Zb3VyIHF1ZXJ5IGZvdW5kIG1vcmUgdGhhbiA1MDAgcmVzdWx0cy4gIE9ubHkgdGhlIGZpcnN0IDUwMCBhcmUgZGlzcGxheWVkLiBSZWZpbmUgeW91ciBzZWFyY2ggdG8gb2J0YWluIG1vcmUgc3BlY2lmaWMgcmVzdWx0cy48L2ZvbnQ+ZAICDxYCHwNoZAIhDxYCHwQF7gQ8dGFibGUgY2VsbHBhZGRpbmc9JzMnIGNlbGxzcGFjaW5nPScxJyB3aWR0aD0nMTAwJSc+PHRyIGNsYXNzPSdyb3dIZWFkZXInPjx0aD5Db250cm9sICM8L3RoPjx0aD5FbnRpdHkgVHlwZTwvdGg+PHRoIHN0eWxlPSd0ZXh0LWFsaWduOmxlZnQ7Jz5OYW1lPC90aD48dGg+TmFtZSBUeXBlPC90aD48dGg+TmFtZSBTdGF0dXM8L3RoPjx0aD5FbnRpdHkgRmlsaW5nIERhdGU8L3RoPjx0aD5FbnRpdHkgU3RhdHVzPC90aD48L3RyPjx0ciBjbGFzcz0ncm93UmVndWxhcic+PHRkPjxhIGhyZWY9J0ZpbGluZ0RldGFpbC5hc3B4P0NOPTI0OTE3ODI0NjIzNjI0MjE4OTA2NTA0MjAyNTE2MjA5MjA0MzIwMzA2MzAzNzE0MicgY2xhc3M9J01lbnVOYXYnIHRpdGxlPSdWaWV3IEVudGl0eSBEZXRhaWwnPjAwMDAwMDAwMjwvYT48L3RkPiA8dGQ+Q09SUDwvdGQ+PHRkIHN0eWxlPSd0ZXh0LWFsaWduOmxlZnQ7Jz5BQUEgQU1FUklDQU4gRkVOQ0UgQ09NUEFOWSwgSU5DLjxiciAvPjxpPlRFTk5FU1NFRTwvaT48L3RkPjx0ZD5FbnRpdHk8L3RkPjx0ZD5JbmFjdGl2ZTwvdGQ+PHRkPjA2LzAxLzE5NzA8L3RkPjx0ZD5JbmFjdGl2ZSAtIERpc3NvbHZlZCAoQWRtaW5pc3RyYXRpdmUpPC90ZD48L3RyPjwvdGFibGU+ZAIjDw8WAh8DaGRkAiUPDxYCHwNoZGQCJw8PFgQfAgUIMS0xIG9mIDEfA2dkZAIpDw8WAh8DaGRkAisPDxYCHwNoZGQCBA8WAh8DaGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFJGN0bDAwJE1haW5Db250ZW50JGNoa1NlYXJjaFN0YXJ0V2l0aAUjY3RsMDAkTWFpbkNvbnRlbnQkY2hrU2VhcmNoSW5jbHVkZXMFI2N0bDAwJE1haW5Db250ZW50JGNoa1NlYXJjaEluY2x1ZGVzBR9jdGwwMCRNYWluQ29udGVudCRjaGtBY3RpdmVPbmx5a+VYzPakkSi2nK95sZS7bCsMBBFSA4XmoEZ1zssFIjg='),
    (r'__VIEWSTATE', r''),
    (r'__VIEWSTATEGENERATOR', r'19191ED7'),
    (r'__EVENTVALIDATION', r'/wEdAAfR3aECIlo4M6b1pNjBbOc36Dpupl2em6ySkIOjOaxkKGSgr32JpB2QYUHUhEkKkuGLy7BGpDsgWC1KmTuieLqvxPbEAiwSkKdl9I33ZPQKH/XDJxEi8paW+8MUVgVBOy1p2c1+qhnI3Ql2GJvAKPRDTU54Uxzaz26PY5Ue5rQJXD7J35G9Fad16dRvFv9L+Z0='),

    # Search criteria
    (r'ctl00$MainContent$txtSearchValue', ''),
    (r'ctl00$MainContent$txtFilingId', contrlnumbr),
    # Radio button (values are chkSearchStartsWith|chkSearchIncludes)
    (r'ctl00$MainContent$searchOpt', 'chkSearchStartWith'),
    # Check box
    (r'ctl00$MainContent$chkActiveOnly', 'on'),

    # Search button
    (r'ctl00$MainContent$SearchButton', 'Search')
)

# Setting the cookies and adding the headers
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# these have to be encoded
encodedFields = urllib.urlencode(formFields)

req = urllib2.Request(uri, encodedFields, headers)
f = urllib2.urlopen(req)     #that's the actual call to the http site.

# *** here would normally be the in-memory parsing of f
#     contents, but instead I store this to file
#     this is useful during design, allowing to have a
#     sample of what is to be parsed in a text editor, for analysis.

print f

# try:
#     fout = open('tmp.htm', 'w')
# except:
#     print('Could not open output file\n')
#
# fout.writelines(f.readlines())
# fout.close()