from tkinter import *


class WindowManager(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='red')
        self.parent = master

        self.__configure()
        self.__create_widgets()

    def __configure(self):
        self.caller = self.parent.caller
        self.app = self.caller.app
        self.root = self.app.root

        self.widgets = dict()
        self.widgets_create_dict = {
            'minimize': {
                'character': '−',
                'color': 'Gold2'  # Yellow2 #FFD940 #FEBF2F
            },
            # 'maximize': {
            #     'character': '+',
            #     'color': 'SpringGreen3'  # SpringGreen2 Green3 #12D400 #28CB42
            # },
            'close': {
                'character': '×',
                'color': 'Brown2'  # OrangeRed FireBrick1 #E00000 #FE5F56
            }
        }

    def __create_widgets(self):
        if self.app.arg('verbose'):
            print(f'{" " * 5}- WindowManager Frame: contains {", ".join(self.widgets_create_dict.keys())} buttons')

        for col_index, (key, curr_dict) in enumerate(self.widgets_create_dict.items()):
            self.widgets[key] = Button(self, font='"Times" 9 bold',
                                       background=curr_dict['color'], activebackground=curr_dict['color'],
                                       foreground='#000000',
                                       highlightthickness=0, bd=0, padx=5, pady=2,  # relief=FLAT, overrelief=FLAT,
                                       command=getattr(self, f'_{key}'),
                                       text=curr_dict['character'])
            self.widgets[key].grid(row=0, column=col_index)

            if self.app.arg('verbose'):
                print(f'{" " * 7}- column {col_index}: {key[0].upper()}{key[1:]} Button')

    def _minimize(self):
        print(f'Minimize: Hiding the {self.caller.__class__.__name__}.')
        getattr(self.app, f'{self.caller.__class__.__name__.lower()}_close')()

    # def _maximize(self):
    #     print('WindowManager: maximize')

    def _close(self):
        print('Close: Exiting the application.')
        sys.exit()
