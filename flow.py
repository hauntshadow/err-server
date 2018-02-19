from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):

    @botflow
    def conf(self, flow: FlowRoot):
        """ This flow sets up confirmation with the users."""
        # List of flows, confirm dialogues, and commands that need confirmation
        flows = []
        con = []
        commands = open("concomm.txt", 'r').read().splitlines()
        for i in range(len(commands)):
            commands[i] = commands[i].split(':')[1]
            flows.append(flow.connect(commands[i], auto_trigger=True))
            con.append(flows[i].connect('confirm'))
            con[i].connect('confirm')
            con[i].connect(FLOW_END)#, predicate=lambda ctx: ctx['tries'] == 0)
