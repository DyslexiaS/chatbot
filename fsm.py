from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, bot, **machine_configs):
        self.bot = bot
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    
    def on_enter_state1(self, update):
        update.message.reply_text("Choose noodle")
        self.go_back(update)
    
    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("Choose rice")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
        
    def on_enter_state3(self, update):
        update.message.reply_text("Choose cookie")
        self.go_back(update)

    def on_exit_state3(self, update):
        print('Leaving state3')

    def on_enter_state4(self, update):
        update.message.reply_text("Choose cake")
        self.go_back(update)

    def on_exit_state4(self, update):
        print('Leaving state4')
