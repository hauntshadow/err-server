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
        """Get the log file from errbot"""
        self.send(msg.frm, "OK to execute command " + msg.body + " [Y/N]?")
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        guess = match.string.lower()
        if guess == 'y':
            self.send_stream_request(user=msg.frm, fsource=open(args, 'rb'), name='log.txt')
            return "File found!"
        return "Permission denied!"

from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class GuessFlows(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def guess(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        game_created = flow.connect('tryme', auto_trigger=True)
        one_guess = game_created.connect('confirm')
        one_guess.connect(FLOW_END)
# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
