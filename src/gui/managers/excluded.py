class ExcludedManager:
    def __init__(self, creator):
        self.app = creator

        self.__configure()

    def __configure(self):
        pass

    def adjust_screen(self, canvas):
        print("Attempted to hide the monitor:", repr(canvas.monitor['name']))

        self.hidden_update_variables_screen(canvas.monitor)
        self.app.widget('ScreenManager').update_hidden(index=canvas.monitor['index'])

    def alter_config_dict(self, sub_key, add, name):
        set_ = self.app.config(sub_key, w=self.__class__)
        print('Alter config dict type of config:', type(set_))
        if add:
            set_.add(name)
        else:
            set_.discard(name)
        self.app.config('screen', w=self.__class__, set=set_)

    def hidden_update_variables_screen(self, monitor):
        print(f'[{self.__class__.__name__}]: Updating Screen hidden variables')
        print(f'[Before]: SM\'s hidden_monitors: {self.app.widget("ScreenManager").hidden_monitors}')
        print(f'[Before]: {monitor["name"]} hidden: {monitor["hidden"]}')

        monitor['hidden'] = not monitor['hidden']
        curr_screen = self.app.widget('ScreenManager').widgets[monitor['index']]
        curr_screen.hidden = monitor['hidden']
        if monitor['hidden']:
            print("Seen => Unseen")
            self.app.widget('ScreenManager').hidden_monitors.add(monitor['index'])
            self.alter_config_dict(sub_key='screen', add=True, name=monitor['name'])
        else:
            print("Unseen => Seen")
            # set().remove throws errors, set().discard doesn't throw errors
            self.app.widget('ScreenManager').hidden_monitors.discard(monitor['index'])
            self.alter_config_dict(sub_key='screen', add=False, name=monitor['name'])

        print(f'[After]: SM\'s hidden_monitors: {self.app.widget("ScreenManager").hidden_monitors}')
        print(f'[After]: {monitor["name"]} hidden: {monitor["hidden"]}')
