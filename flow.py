from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def conf(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        flows = []
        con = []
        message = []
        commands = ['retrieve', 'server_active']
        for i in range(len(commands)):
            flows.append(flow.connect(commands[i], auto_trigger=True))
            message.append(flows[i].connect('confirm_message'))
            con.append(message[i].connect('confirm'))
            con[i].connect('confirm')
            con[i].connect(FLOW_END)#, predicate=lambda ctx: ctx['tries'] == 0)
