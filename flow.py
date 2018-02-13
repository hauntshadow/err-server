from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def conf(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        flows = []
        con = []
        commands = ['retrieve']
        for i in range(len(commands)):
            flows.append(flow.connect(commands[i], auto_trigger=True))
            con.append(flows[i].connect('confirm'))
            con[i].connect('confirm')
            con[i].connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
