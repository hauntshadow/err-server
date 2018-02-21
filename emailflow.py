from errbot import botflow, FlowRoot, BotFlow, FLOW_END

commands = ['retrieve']#open("/var/lib/err/plugins/hauntshadow/err-server/concomm.txt", 'r').read().splitlines()
       
class ConfFlow(BotFlow):
       
    @botflow
    def conf(self, flow: FlowRoot):
        """ This flow sets up confirmation with the users."""
        # Lists of flows and confirm dialogues
        flows = []
        con = []
        for i in range(len(commands)):
            flows.append(flow.connect(commands[i], auto_trigger=True))
            #End if command doesn't need confirming
            flows[i].connect(FLOW_END, predicate=lambda ctx: ctx['commands'])
            con.append(flows[i].connect('confirm'))
            con[i].connect('confirm')
            #End if command confirmation has been attempted
            con[i].connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
