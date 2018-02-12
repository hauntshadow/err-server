from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def conf(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        dialogue = flow.connect('retrieve', auto_trigger=True)
        conf = dialogue.connect('confirm')
        conf.connect('confirm')
        conf.connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
