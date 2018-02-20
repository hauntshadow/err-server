from errbot import BotPlugin, botcmd, botmatch, BotFlow
import subprocess, tempfile, re, time
import smtplib
from email.mime import multipart, text, base
from email import encoders
import emailflow

class Email(BotPlugin):
    """Email plugin for Errbot"""

    
    #flowmod = ConfFlow(BotFlow(BotPlugin))
    
    @botcmd
    def acceba(self, msg, args):
        """Add admin command"""
        self['command'] = "acceba"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            emailflow.commands.append(self['args'])
            return "Command " + self['args'] + " added to admin commands."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
        return prompt
    
    @botcmd
    def rcceba(self, msg, args):
        """Remove admin command"""
        self['command'] = "rcceba"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            emailflow.commands.remove(self['args'])
            return "Command " + self['args'] + " removed to admin commands."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
    
    @botcmd
    def retrieve(self, msg, args, attempts=1):
        """Set up file transfer"""
        self['command'] = "retrieve"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            #User and Errbot's emails
            fromaddr = "errbotemail@gmail.com"#str(msg.to).split('/')[0]
            toaddr = "chr.smith@cgi.com"#str(self.user).split('/')[0]
            #Make the message and it's from, to, and subject lines
            mess = multipart.MIMEMultipart()
            mess['From'] = fromaddr
            mess['To'] = toaddr
            mess['Subject'] = "File from Errbot"
            
            body = "The file you requested is attached."
            #Connect the body to the email
            mess.attach(text.MIMEText(body, 'plain'))
            #Get the file, rename it log.txt, and attach it
            filename = "log.txt"
            attachment = open(self['args'], "rb")
            part = base.MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            mess.attach(part)
            #Send the email to the user
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "errbot123")
            sent_email = mess.as_string()
            server.sendmail(fromaddr, toaddr, sent_email)
            server.quit()
            return "Email sent."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
        
    def preconfirm(self, msg, args):
        """Set up the environment for confirmation"""
        self['permission'] = False
        self['args'] = args
        user = str(msg.frm)
        self['user'] = user
        msg.ctx['tries'] = 1
        return "OK to execute command " + msg.body + " [Y/N]?"
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        """Confirmation dialogue"""
        ans = match.string.lower()
        
        if ans == 'y' and str(msg.frm) != self['user']:
            self['permission'] = True
            self.send(msg.frm, "Permission granted.")
            msg.ctx['tries'] = 0
            #Call the function whose name is the original command with a '2' appended to the end of it
            return getattr(self, self['command'])(msg, self['args'], 0)
        elif str(msg.frm) == self['user']:
            return "Someone else must confirm the command. Permission denied."
        else:
            return "Permission denied."
   
    def acceba2(self, msg, args):
        """Add to list of admin commands"""
        if self['permission']:
            commfile = open("/var/lib/err/plugins/hauntshadow/err-server/concomm.txt", 'w')
            commands = commfile.read().splitlines()
            commands.append(self['args'])
            for comm in commands:
                commfile.write(":%s:\n" % comm)
            return "Command added to admin commands."
        
    def rcceba2(self, msg, args):
        """Add to list of admin commands"""
        if self['permission']:
            commfile = open("/var/lib/err/plugins/hauntshadow/err-server/concomm.txt", 'w')
            commands = commfile.read().splitlines()
            commands.remove(self['args'])
            for comm in commands:
                commfile.write(":%s:\n" % comm)
            return "Command added to admin commands."


# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
