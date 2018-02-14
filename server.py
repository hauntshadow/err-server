from errbot import BotPlugin, botcmd, botmatch
import subprocess, tempfile, re, time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class AutoSysServer(BotPlugin):
    """AutoSys server plugin for Errbot"""

    @botcmd
    def server_target(self, msg, args):
        """Target server for jobs"""
        self['target_server'] = args
        self.target_server = args
        #with open('/var/errbot/target_server', 'w+') as file:
        #    proc = subprocess.Popen(['echo',args], stdout=file)
        #    proc.wait()
        #    file.seek(0)
        #    target_server = str(target_server) + str(file.read())
        return "Targeted server: " + self['target_server']
    
    @botcmd
    def server_active(self, msg, args):
        """Retrieve targeted server"""
        self['command'] = "server_active"
        self.preconfirm(msg, args)
        #target_server = ""
        #with open('/var/errbot/target_server', 'r') as file:
        #    target_server = str(file.read())
        return "Currently targeted server: " + self['target_server']

    @botcmd
    def retrieve(self, msg, args):
        """Set up file transfer"""
        self.preconfirm(msg, args)
        self['command'] = "retrieve"
        
    def preconfirm(self, msg, args):
        """Set up the environment for confirmation"""
        self['permission'] = False
        self['args'] = args
        self['user'] = msg.frm
        self.send(msg.frm, "OK to execute command " + msg.body + " [Y/N]?")
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        """Confirmation dialogue"""
        guess = match.string.lower()
        if guess == 'y' and msg.frm != self.user:
            self['permission'] = True
            self.send(msg.frm, "Permission granted.")
            #Call the function whose name is the original command with a '2' appended to the end of it
            return getattr(self, self['command'] + "2")(msg, self['args'])
        elif msg.frm == self.user:
            return "Someone else must confirm the command. Permission denied."
        else:
            return "Permission denied."

    def retrieve2(self, msg, args):
        """Get the log file from errbot"""
        if self['permission']:
            fromaddr = msg.to
            toaddr = self.user
     
            mess = MIMEMultipart()
     
            mess['From'] = fromaddr
            mess['To'] = toaddr
            mess['Subject'] = "File from Errbot"
     
            body = "The file you requested is attached."
     
            mess.attach(MIMEText(body, 'plain'))
     
            filename = "log.txt"
            attachment = open(self.args, "rb")
     
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
            mess.attach(part)
     
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "YOUR PASSWORD")
            text = mess.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
    
    def server_active2(self, msg, args):
        """Test function"""
        if self['permission']:
            self.send(msg.frm, "You did the thing again!")

# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
