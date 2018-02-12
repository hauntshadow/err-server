from errbot import BotPlugin, botcmd
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
        """Get the log file from errbot"""
        if self.confirm(msg):
            self.send_stream_request(user=msg.frm, fsource=open(args, 'rb'), name='log.txt')
            return "File found!"
        else:
            return "Permission denied!"
        
    @botcmd
    def confirm(self, msg):
        """Ask user to enter Y or N (case-insensitive).
        :return: True if the answer is Y.
        :rtype: bool"""
        answer = ""
        while answer not in ["y", "n"]:
            answer = input("OK to execute command " + msg.body + " [Y/N]? ").lower()
        return answer == "y" 
# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
