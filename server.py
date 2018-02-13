from errbot import BotPlugin, botcmd, botmatch
import subprocess, tempfile, re, time

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
        #target_server = ""
        #with open('/var/errbot/target_server', 'r') as file:
        #    target_server = str(file.read())
        return "Currently targeted server: " + self['target_server']

    @botcmd
    def retrieve(self, msg, args):
        """Ask for the log file from errbot"""
        msg.ctx['tries'] = 2
        msg.ctx['permission'] = False
        msg.ctx['command'] = "retrieve"
        msg.ctx['args'] = args
        self.send(msg.frm, "OK to execute command " + msg.body + " [Y/N]?")
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        msg.ctx['tries'] -= 1
        guess = match.string.lower()
        if guess == 'y':
            msg.ctx['tries'] = 0
            msg.ctx['permission'] = True
            self.send(msg.frm, "Permission granted.")
            return getattr(self, msg.ctx['command'] + "2")(msg, args)
        msg.ctx['permission'] = False
        if guess == 'n' or msg.ctx['tries'] == 0:
            return "Permission denied."
        return "Invalid. Please try again."

    @botcmd(flow_only=True)
    def retrieve2(self, msg, args):
        """Get the log file from errbot"""
        if msg.ctx['permission']:
            self.send(msg.frm, "You did the thing!")

# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
