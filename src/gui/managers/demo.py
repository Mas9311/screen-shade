class DemoManager:
    def __init__(self, creator):
        self.app = creator

        self.__configure()

    def __configure(self):
        pass

    def adjust_demo(self, value):
        self.app.arg('demo', set=value)
        self.app.widget('ScreenManager').update_demo()
