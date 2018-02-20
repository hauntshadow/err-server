from errbot import botflow, FlowRoot, BotFlow, FLOW_END

commands = ['retrieve']#open("/var/lib/err/plugins/hauntshadow/err-server/concomm.txt", 'r').read().splitlines()
       
class ConfFlow(BotFlow):
       
    @botflow
    def conf(self, flow: FlowRoot):
        """ This flow sets up confirmation with the users."""
        # List of flows, confirm dialogues, and commands that need confirmation
        flows = []
        con = []
        for i in range(len(commands)):
            #commands[i] = commands[i].split(':')[1]
            flows.append(flow.connect(commands[i], auto_trigger=True))
            con.append(flows[i].connect('confirm', predicate=lambda ctx: body.split(" ")[0][1:] not in ctx['commands']))
            #con[i].connect('confirm')
            con[i].connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
