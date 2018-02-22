from errbot import BotPlugin, botcmd, botmatch
import subprocess, tempfile, re, time
import smtplib
from email.mime import multipart, text, base
from email import encoders
import emailflow
import tempfile

class Email(BotPlugin):
    """Email plugin for Errbot"""
    
    @botcmd
    def acceba(self, msg, args, attempts=1):
        """Add admin command"""
        self['command'] = "acceba"
        #Add command if approved or doesn't need approval
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            if args not in emailflow.commands:
                emailflow.commands.append(args)
                return "Command " + args + " added to list of confirm commands."
            else:
                return "Command already in list of confirm commands."
        #Get confirmation
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
    
    @botcmd
    def rcceba(self, msg, args, attempts=1):
        """Remove admin command"""
        self['command'] = "rcceba"
        #Remove command if approved or doesn't need approval
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            if args in emailflow.commands:
                emailflow.commands.remove(args)
                return "Command " + args + " removed from list of confirm commands."
            else:
                return "Command not in list of confirm commands."
        #Get confirmation
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt

    @botcmd
    def get_log(self, msg, args, attempts=1):
        """Add admin command"""
        self['command'] = "get_log"
        if "-email" in args and attempts == 1:
            args = args.split(" ")
            msg.ctx['useremail'] = args[args.index("-email") + 1]
            del args[args.index("-email") + 1]
            del args[args.index("-email")]
            args = " ".join(args)
        #Set email to a default
        elif attempts == 1:
            msg.ctx['useremail'] = "chr.smith@cgi.com"
        #Add command if approved or doesn't need approval
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            data = self.get_plugin('Utils').log_tail(msg, args)
            with tempfile.NamedTemporaryFile(prefix="log_", suffix=".txt") as temp:
                temp.write(str.encode(data))
                return self.retrieve(msg, temp.name, 0)
        #Get confirmation
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt    
        
    @botcmd
    def retrieve(self, msg, args, attempts=1):
        """Set up file transfer"""
        #Set email based on flag the first time in the function
        if "-email" in args and attempts == 1:
            self['command'] = "retrieve"
            args = args.split(" ")
            msg.ctx['useremail'] = args[args.index("-email") + 1]
            del args[args.index("-email") + 1]
            del args[args.index("-email")]
            args = " ".join(args)
        #Set email to a default
        elif attempts == 1:
            self['command'] = "retrieve"
            msg.ctx['useremail'] = "chr.smith@cgi.com"
        #Send email if approved or doesn't need approval
        if (self['command'] in emailflow.commands and attempts == 0 and self['permission'] == True) or self['command'] not in emailflow.commands:
            #User and Errbot's emails
            fromaddr = "errbotemail@gmail.com"
            toaddr = msg.ctx['useremail']
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
        #Get confirmation
        if self['command'] in emailflow.commands and attempts == 1:
            prompt = self.preconfirm(msg, args)
            return prompt
        
    def preconfirm(self, msg, args):
        """Set up the environment for confirmation"""
        self['permission'] = False
        user = str(msg.frm)
        self['args'] = args
        self['user'] = user
        msg.ctx['commands'] = self['command'] not in emailflow.commands
        msg.ctx['tries'] = 1
        return "OK to execute command " + msg.body + " [Y/N]?"
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        """Confirmation dialogue"""
        ans = match.string.lower()
        #Confirmation not needed
        if self['command'] not in emailflow.commands:
            return
        #Confirmed by another user
        if ans == 'y' and str(msg.frm) != self['user']:
            self['permission'] = True
            self.send(msg.frm, "Permission granted.")
            msg.ctx['tries'] = 0
            #Call the function whose name is the original command
            return getattr(self, self['command'])(msg, self['args'], 0)
        #User cannot confirm their own command
        elif str(msg.frm) == self['user']:
            msg.ctx['tries'] = 0
            return "Someone else must confirm the command. Permission denied."
        #Confirmation denied
        else:
            msg.ctx['tries'] = 0
            return "Permission denied."
   

# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
