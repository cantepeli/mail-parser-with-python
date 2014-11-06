import paramiko
import ftplib
import os

class CopyFTpSFTP(object):

    def SFTPCopy(self,server,username,password,localpath,remotepath):
        
        ssh = paramiko.SSHClient() 
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
        ssh.close()
        
    def FTPCopy(self,host,username,password,path,filename):
        
        ftp = ftplib.FTP(host)
        ftp.login(username, password)
        print ftp.getwelcome()
        print "-----------------------------------------------------------------------------------------------"
        ftp.cwd(path)
        print "Currently in : ", ftp.pwd()
        print "Uploading.................",
        fp = open(filename, 'r')
        ftp.storlines("STOR " + filename, fp)
        fp.close()
        print "OK"
        print "Files:"+filename
        #print ftp.retrlines('LIST')
        #ftp.quit() 