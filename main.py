import os
import sys
import mimetypes
import io
import regex_mail
import sftp_copy
import send_mail
import ConfigParser
import time
import shutil
import logging

from regex_mail import findUrlAtMail
from sftp_copy import CopyFTpSFTP
from send_mail import sendMail
from os import path
from tld import get_tld

COMMASPACE = ', '

class main(CopyFTpSFTP):
    def __init__(self):
        req_version = (2,7,6)
        cur_version = sys.version_info
        if cur_version < req_version:
            print "Must use python 2.7.6 or greater.....!!!!!"
            
        config = ConfigParser.RawConfigParser()
        global script_dir , makeProcessFileDOMAIN , makeProcessFileURL
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config.read(script_dir+'/config.cfg')
        logging.basicConfig(
            filename=config.get('Local_Server_File_Setting','LogginFile'),
            level=logging.INFO)
        directory = config.get('Local_Server_File_Setting','ParseDirectory')
        ResConf = config.get('Local_Server_File_Setting','ResultFile')
        msg = ''
        TIMERS = time.strftime("%Y%m%d-%H%M%S")
        makeProcessFileURL ="URL_"+TIMERS+".txt"
        makeProcessFileDOMAIN ="DOMAIN_"+TIMERS+".txt"
        logging.info('Starting process for '+makeProcessFileURL)
        if not directory:
            directory = '.'
        self.checkFile(os.listdir(directory))
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if not os.path.isfile(path):
                continue
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'application' or 'text' or 'message':
                with open(path) as fp:
                    msg = fp.read()
                    regexResult = findUrlAtMail(msg)
                    fp.close()
            self.writeToFileBylineBy(ResConf,regexResult)
            os.remove(path) 
            logging.info('timely processing of these are done->'+path)
        logging.info('this process was processing on the total domain -> %s ' % self.getFileCount(makeProcessFileDOMAIN))
        logging.info('this process was processing on the total url -> %s' % self.getFileCount(makeProcessFileURL))
        
        CopyFile = sftp_copy.CopyFTpSFTP()

        if (config.get('Remote_Server_Setting','ssh') == 'true'):    
            CopyFile.SFTPCopy(
                config.get('Remote_Server_Setting','HOSTNAME'),
                config.get('Remote_Server_Setting','USERNAME'),
                config.get('Remote_Server_Setting','PASSWORD'),
                script_dir+"/"+makeProcessFileURL,
                config.get('Remote_Server_Setting','COPYDIRECTORY')+makeProcessFileURL)
            
            CopyFile.SFTPCopy(
                config.get('Remote_Server_Setting','HOSTNAME'),
                config.get('Remote_Server_Setting','USERNAME'),
                config.get('Remote_Server_Setting','PASSWORD'),
                script_dir+"/"+makeProcessFileDOMAIN,
                config.get('Remote_Server_Setting','COPYDIRECTORY')+makeProcessFileDOMAIN)
        else:
            CopyFile.FTPCopy(
                config.get('Remote_Server_Setting','HOSTNAME'),
                config.get('Remote_Server_Setting','USERNAME'),
                config.get('Remote_Server_Setting','PASSWORD'),
                config.get('Remote_Server_Setting','COPYDIRECTORY'),
                makeProcessFileURL)
            
            CopyFile.FTPCopy(
                config.get('Remote_Server_Setting','HOSTNAME'),
                config.get('Remote_Server_Setting','USERNAME'),
                config.get('Remote_Server_Setting','PASSWORD'),
                config.get('Remote_Server_Setting','COPYDIRECTORY'),
                makeProcessFileDOMAIN)
        
        if (config.get('Stmp_Mail_Server_Setting','Sender') == 'true'):
            sendMail(
                config.get('Stmp_Mail_Server_Setting','MailHost'),
                config.get('Stmp_Mail_Server_Setting','MailUser'),
                config.get('Stmp_Mail_Server_Setting','MailPass'),
                config.get('Stmp_Mail_Server_Setting','ToMail'),
                config.get('Stmp_Mail_Server_Setting','FromMail'),self.getFileContent(ResConf))
            
        os.remove(ResConf)
        os.remove(script_dir+"/ERASE.txt")
        os.remove(script_dir+"/FULLURLSORT.txt")
        os.remove(script_dir+"/"+makeProcessFileURL)
        os.remove(script_dir+"/"+makeProcessFileDOMAIN)
        logging.info('It ended on the transcations '+makeProcessFileURL)
        
    def getFileContent(self,conf):
        resFile = open(conf, 'r')
        MailContent = resFile.read()    
        resFile.close()
        return MailContent
    
    def makeSplit(self,conf):
        retult = conf.split("/")[len(conf.split('/'))-1][:len(conf.split('/'))+16]
        return retult
    
    def checkFile(self,structure):
        if not structure:
            print('File is empty.')
            exit()
    
    def replaceFile(self,ResConf):
        URLdomain = script_dir+"/DOMAIN.txt"
        DOMAIN = open(URLdomain, "wb")
        ERASE = open(script_dir+"/ERASE.txt", "wb")
        fullURL = open(script_dir+"/FULLURL.txt", "wb")
        lines = [line.strip('\n=')
                 .rstrip('"\n')
                 .rstrip('~\n')
                 .rstrip('=\n')
                 .rstrip('\n/')
                 .rstrip('=\n')
                 .rstrip('\n=')
                 .rstrip('"\n=')
                 .rstrip('\n/"')
                 .rstrip('~\n')
                 .rstrip('"\n=')
                 .rstrip(']\n')
                 .rstrip('[\n')
                 .rstrip('/\n')
                 .rstrip('\\n')
                 .rstrip('*\n')
                 .rstrip(';\n')
                 .rstrip(',\n')
                 .rstrip('.\n')
                 .rstrip('}\n')
                 for line in open(ResConf)]
        fullURL.writelines(("%s\n" % l for l in lines  ))
        for l in lines : 
           res = get_tld(("%s" % l), fail_silently=True)
           if res is None:
                ERASE.writelines(("%s\n" %  l))
           else:
                DOMAIN.writelines(("%s\n" %  res))
        DOMAIN.close()
        ERASE.close()
        fullURL.close()
        
        cmdDomain = "sort -n "+URLdomain+" | uniq > "+script_dir+"/domainURLSORT.txt"
        os.system(cmdDomain)
        FULLSRT = "sort -n "+script_dir+"/FULLURL.txt"+" | uniq > "+script_dir+"/FULLURLSORT.txt"
        os.system(FULLSRT)
        os.remove(URLdomain)
        os.remove(script_dir+"/FULLURL.txt")
        os.rename(script_dir+"/domainURLSORT.txt", makeProcessFileDOMAIN)
        self.garbage_collector(script_dir+"/FULLURLSORT.txt",script_dir+"/"+makeProcessFileURL,"/ERASE.txt") 
    
    def writeToFileBylineBy(self,ResConf,regexResult):
        excludeTmp = script_dir+"/extTmp.txt"
        myfile = open(ResConf, 'a')
        myfile.writelines(("%s\n" % l for l in regexResult))
        myfile.close()
        self.garbage_collector(ResConf,excludeTmp,"/exclusions.txt") 
        self.replaceFile(excludeTmp)
        os.remove(excludeTmp)
     
    def getFileCount(self,path):
        return sum(1 for line in open(script_dir+"/"+path))
    
    def garbage_collector (self,ResConf,ResConfTmp,rpt):
        fp = open(ResConfTmp,"w+")
        with open(ResConf, "r") as text, open(script_dir+rpt, "r") as exc:
            exclusions = [line.rstrip('\n') for line in exc]
            for line in text:
                if not any(exclusion in line for exclusion in exclusions):
                    fp.writelines(line)
        fp.close()
        
if __name__ == '__main__':
    main()        
