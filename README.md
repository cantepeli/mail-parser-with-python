mail-parser-with-python
=======================

mail (elm) parser with python 


The goal of this project will parse the email body and finds URLs in email
copy to remote server  with  sftp or ftp 

That's working with Python 2.7.6

Requirements

1 - Python 2.7.6 or go there http://www.python.org
2 - Pycrypto 2.1 or go there https://www.dlitz.net/software/pycrypto
3 - Ecdsa 0.9 or there  https://pypi.python.org/pypi/ecdsa
4 - Tld 0.7.2 or there https://pypi.python.org/pypi/tld   
5 - Paramiko library  http://paramiko-www.readthedocs.org/en/latest/installing.html
    If you have setup tools, you can build and install paramiko 


How to configure it.

Only fill out in the information in the config.cfg file.

[Remote_Server_Setting]
    HOSTNAME:175.44.45.37
    USERNAME:username
    PASSWORD:123456
    COPYDIRECTORY:/home/
    ssh:false             # If these parameter is true  it is going to use sftp  otherwise ftp  uses,

[Stmp_Mail_Server_Setting]
    MailHost:175.56.46.1
    MailUser:cantepeli@me.com
    MailPass:passsword!
    FromMail:cantepeli@me.com
    ToMail:cantepeli@me.com
    Sender: false           # If this parameter is true, as mail sent to parse results

[Local_Server_File_Setting]
    ParseDirectory:/home/root/Desktop/file/
    ResultDirectory:/home/root/Desktop/result/
    ResultFile:/home/root/Desktop/result/result.txt
    LogginFile:/home/root/Desktop/result/process.log

lastly, for the remote server, you must create a fingerprint.

If you do not want a domain or URL to be processed, you should write it in exclusions.txt.


NOte :  That's source has not been optimized yet 

Can Tepeli
