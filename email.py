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
    def acceba(self, msg, args, attempts=1):
        """Add admin command"""
        self['command'] = "acceba"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            if args not in emailflow.commands:
                emailflow.commands.append(args)
                emailflow.addconf()
                return "Command " + args + " added to list of confirm commands."
            else:
                return "Command already in list of confirm commands."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
        return prompt
    
    @botcmd
    def rcceba(self, msg, args, attempts=1):
        """Remove admin command"""
        self['command'] = "rcceba"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            if args in emailflow.commands:
                emailflow.commands.remove(args)
                return "Command " + args + " removed from list of confirm commands."
            else:
                return "Command not in list of confirm commands."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
    
    @botcmd
    def retrieve(self, msg, args, attempts=1):
        """Set up file transfer"""
        self['command'] = "retrieve"
        if "-email" in args and attempts == 1:
            args = args.split(" ")
            useremail = args[args.index("-email") + 1]
            del args[args.index("-email") + 1]
            del args[args.index("-email")]
            args = " ".join(args)
        elif attempts == 1:
            useremail = "chr.smith@cgi.com"
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            #User and Errbot's emails
            fromaddr = "errbotemail@gmail.com"
            toaddr = useremail
            #Make the message and it's from, to, and subject lines
            mess = multipart.MIMEMultipart()
            mess['From'] = fromaddr
            mess['To'] = toaddr
            mess['Subject'] = "File from Errbot"
            
            body = "The file you requested is attached."
            #Connect the body to the email
            mess.attach(text.MIMEText(body, 'plain'))
            #Get the file and attach it
            attachment = open(args, "rb")
            part = base.MIMEBase('application', 'octet-stream')
            filename = str(args)
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
            return "Email sent with requested attachment."
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
        
    def preconfirm(self, msg, args):
        """Set up the environment for confirmation"""
        self['permission'] = False
        user = str(msg.frm)
        self['args'] = args
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
   

# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
