# from tkinter import *
from tkinter import ttk


class TabBar(ttk.Notebook):
    """Creates the Notebook's tabs located at the top-left corner.
    Allows the user to select different tabs.
    Creates all Tabs created, but hidden Tabs are not initially displayed."""
    def __init__(self, creator):
        self.manager = creator

        ttk.Notebook.__init__(self, self.manager)
        self.grid(row=0, column=0, sticky='W')
        # self.enable_traversal()

        self.__bind()
        self.__configure()
        self.__create_widgets()

    def __bind(self):
        self.bind('<<NotebookTabChanged>>', self.change_tab)

    def __configure(self):
        self.app = self.manager.app
        self.root = self.app.root

        self.style = ttk.Style()
        self.__initialize_tab_bar_style()

    def __initialize_tab_bar_style(self):
        """Creates the style used for the Notebook (TabBar) and the Tabs"""
        # print("TNotebook :".format(self.parent.style('TNotebook.Tab')))
        # customizes the TabBar widget (exists behind the tabs)
        self.style.configure("TNotebook",
                             background='#009954',  # bg color of entire TabBar row
                             borderwidth=0,
                             tabmargins=[3, 6, 3, 0])

        # customizes the active tab
        self.style.map("TNotebook.Tab",
                       background=[
                           ('selected', '#424242'),  # bg color of currently-selected tab
                           ('active', '#424242'),  # bg color when mouse hovers over
                       ],
                       expand=[
                           ('selected', [1, 3, 1, 0])
                       ],
                       # focuscolor=[
                       #     ('selected', '#4a009b'),
                       # ]
                       )

        # customizes the inactive tabs
        self.style.configure('TNotebook.Tab',
                             background='#606060',  # bg   color of tab_label when mouse is not hovering over
                             foreground='#bbbbbb',  # font color of tab_label when mouse is not hovering over
                             padding=[4, 3],
                             borderwidth=2)

    def __create_widgets(self):
        """Creates all tabs from parent, but only shows the non-hidden tabs"""
        self.widgets = []
        self.map_dict = {}

        for index, curr in enumerate(self.manager.tab_create_list):
            if self.app.arg('verbose'):
                print(f'{" " * 5}- column {index}: `{curr["name"]}` tab')
            self.map_dict[index] = curr['name']
            self.map_dict[curr['name']] = index
            curr_widget = ttk.Frame(self)
            self.widgets.append(curr_widget)
            self.add(curr_widget, text=curr['name'])
        self.select(0)

    def change_tab(self, event):
        tab_index = self.current_tab_index()
        print(f'Clicked Tab #{tab_index}, {self.map_dict[tab_index]}')

    def current_tab_index(self):
        """Returns the integer of the currently selected Tab"""
        return self.index(self.select())

    def forget(self, **kwargs):
        while self.widgets:
            tab = self.widgets.pop(0)
            if self.app.arg('verbose') > 2:
                print(f'{" " * 5}> tab {tab}')

            super().forget(tab)
            tab.destroy()

    # def override_select(self, tab_index=None):
    #     """Manipulates the selection to emulate <<NotebookTabChanged>> virtual event"""
    #     if self.current_tab_index() is not tab_index:
    #         print('Manually selecting tab #', tab_index)
    #         self.show_tab(tab_index)
    #         self.select(tab_index)
