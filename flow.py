from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def conf(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        flows = []
        commands = ['retrieve']
        for i in len(commands):
            flows[i] = flow.connect(commands[i], auto_trigger=True)
            conf.append(flows[i].connect('confirm'))
            conf[i].connect('confirm')
            conf[i].connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
