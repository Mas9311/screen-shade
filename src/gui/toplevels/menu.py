from tkinter import *
# from tkinter import font

from src.gui.frames.titlebar import Titlebar


class MenuConfig(Toplevel):
    def __init__(self, creator):
        super().__init__()
        self.app = creator

        self.__configure()
        self.__create_widgets()

    def __configure(self):
        self.root = self.app.root
        self.manager = self

        self.overrideredirect(True)
        self.geometry(
            # f'{self.app.config("w", w=self.__class__)}x'
            # f'{self.app.config("h", w=self.__class__)}+'
            f'+{self.app.config("x", w=self.__class__)}+'
            f'{self.app.config("y", w=self.__class__)}')
        # self.bind('<Enter>', self.mouse_hover_enter)
        # self.bind('<Leave>', self.mouse_hover_leave)

        self.widgets_create_dict = {
            self.app.get_class('ScreenManager'): {
                'alpha': {
                    'type': 'scale',
                    'var_type': 'DoubleVar',
                    'description': 'Screen Transparency',
                    'from': 0,
                    'to': 0.975,
                    'resolution': 0.001,
                    'storage': 'config',
                },
                'color': {
                    'type': 'radiobutton',
                    'var_type': 'StringVar',
                    'description': 'Screen Color',
                    'options': [
                        ('White', '#FFFFFF'),
                        ('Gray4', '#404040'),
                        ('Black', '#000000'),
                        ('Sepia', '#704214'),
                        ('Brown', '#643B0F'),
                        # ('', '#'),
                        # ('', '#'),
                        # ('', '#'),
                        ('DBlue', '#00172E'),
                    ],
                    'per_row': 3,
                    'storage': 'config',
                },
                'px_radius': {
                    'type': 'scale',
                    'var_type': 'IntVar',
                    'description': 'Mouse Radius',
                    'from': 1,
                    'to': 100,
                    'resolution': 1,
                    'storage': 'config',
                }
            },
            self.app.get_class('BorderManager'): {
                'px_radius': {
                    'type': 'scale',
                    'var_type': 'IntVar',
                    'description': 'Border Radius',
                    'from': 1,
                    'to': 50,
                    'resolution': 1,
                    'storage': 'config',
                }
            },
            self.app.get_class('ExcludedManager'): {
                'screen': {
                    'type': 'canvas_screen',
                    'var_type': 'StringVar',
                    'description': 'Hidden Screens',
                    'monitors': self.app.monitors,
                    'storage': 'config',
                }
            },
            self.app.get_class('DemoManager'): {
                'demo': {
                    'type': 'radiobutton',
                    'var_type': 'BooleanVar',
                    'description': 'Demo',
                    'options': [
                        ('On ', True),
                        ('Off', False)
                    ],
                    'per_row': 2,
                    'storage': 'arg',  # stored in ``self.app._arg_dict`` accessible with self.app.arg() method
                }
            },
        }
        self.internal_observer_names = []

    def __create_widgets(self):
        if self.app.arg('verbose'):
            print(f'\n{"*" * 42}\nSTART: Creating nested MenuConfig widgets\n{"*" * 42}')
        self.widgets = dict()
        self.variables = dict()  # holds types: {BooleanVar, DoubleVar, IntVar, StringVar}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._create_titlebar()  # creates the top-most border containing the window manager buttons {−, +, ×}
        self._create_main_frame()  # creates the Frame to hold the bulk of the MenuConfig, i.e. Scales, Buttons, etc.

        self.row_index = 0
        for curr_class, curr_class_dict in self.widgets_create_dict.items():
            self.widgets[curr_class] = dict()
            self.variables[curr_class] = dict()
            for sub_key, curr_dict in curr_class_dict.items():
                self.widgets[curr_class][sub_key] = dict()
                self._create_widget_description(curr_class, curr_dict)
                getattr(self, f'_create_widget_{curr_dict["type"]}')(curr_class, sub_key, curr_dict)

        self.main_frame.rowconfigure(self.row_index, weight=1)
        if self.app.arg('verbose'):
            print(f'{" " * 5}> row {self.row_index}: vertically centered.')
            print(f'{"*" * 43}\nFINISH: Creating nested MenuConfig widgets\n{"*" * 43}\n\n')

    def _create_titlebar(self):
        if self.app.arg('verbose'):
            print(f'{" " * 3}- row 0: TitleBar allows click+drag to move MenuConfig')
        self.titlebar = Titlebar(master=self)
        self.titlebar.grid(row=0, column=0, sticky=W + N + E)  # .pack(fill=X, expand=True)
        # self.titlebar.update_idletasks()

    def _create_main_frame(self):
        if self.app.arg('verbose'):
            print(f'{" " * 3}- row 1: Frame contains configuration modifier widgets')
        self.main_frame = Frame(master=self, bg=self.app.config('color', 'inner', w=self.__class__))
        self.main_frame.grid(row=1, column=0, sticky='wnes')
        self.main_frame.columnconfigure(0, weight=1)

    def _create_variable_type(self, curr_class, sub_key, curr_dict):
        """Assigns the dict entry (for self.variables) with the instance as the value.
        self.variables dict is navigable:
            first dict: class
            second dict: which field are we modifying? {color, alpha, px_radius, ...}
            value: variable instance {DoubleVar, StringVar}
        eg: self.variables[ScreenManager][px_radius] = StringVar(name='StringManager px_radius')

        This allows us to use self.variables[class][sub] like the instance itself and use the ``Var`` methods:
            - self.variables[class][sub].get()
            - self.variables[class][sub].set('New Value')
        """
        var_name = f'{curr_class.__name__} {sub_key}'

        if 'var_type' in curr_dict.keys():
            var_type = curr_dict['var_type']
        else:
            # default to StringVar if not specified in self.widgets_create_dict
            var_type = 'StringVar'
        self.variables[curr_class][sub_key] = getattr(sys.modules[__name__], f'{var_type}')(name=var_name)

        return var_name

    def _create_widget_description(self, curr_class, curr_dict):
        self.main_frame.rowconfigure(self.row_index, weight=1)
        self.row_index += 1

        self.widgets[curr_class]['description'] = Label(master=self.main_frame, text=f'{curr_dict["description"]}:')
        self.widgets[curr_class]['description'].grid(row=self.row_index, column=0)
        if self.app.arg('verbose'):
            print(f'{" " * 5}- row {self.row_index}: Label widget \'description\': \'{curr_dict["description"]}\'')
        self.row_index += 1

    def _create_widget_generic_frame(self, curr_class, sub_key):
        """Create a frame to nest 2 widgets in: Label (value) and the actual widget {Scale, Text}
        Column 0: grid-equivalent of: fill=None, expand=False
        Column 1: grid-equivalent of: fill=X,    expand=True
        """
        generic_frame = Frame(master=self.main_frame, bg=self.app.config('color', 'inner', w=self.__class__))
        generic_frame.grid(row=self.row_index, column=0, sticky='nsew')
        if self.app.arg('verbose'):
            print(f'{" " * 5}- row {self.row_index}: (nested) Frame widget {curr_class.__name__}[\'{sub_key}\']')
        self.row_index += 1

        generic_frame.columnconfigure(0, weight=0)
        generic_frame.columnconfigure(1, weight=1)

        return generic_frame

    def _create_widget_scale(self, curr_class, sub_key, curr_dict):
        self._create_variable_type(curr_class, sub_key, curr_dict)
        temp_frame = self._create_widget_generic_frame(curr_class, sub_key)

        self.widgets[curr_class][sub_key]['value'] = Label(master=temp_frame, text='*****')
        self.widgets[curr_class][sub_key]['value'].pack(side=LEFT, expand=False)
        if self.app.arg('verbose'):
            print(f'{" " * 7}- column 0: Label widget \'value\' {curr_class.__name__}[\'{sub_key}\']')

        self.widgets[curr_class]['scale'] = Scale(master=temp_frame, showvalue=0, orient=HORIZONTAL,
                                                  from_=curr_dict['from'], to=curr_dict['to'],
                                                  resolution=curr_dict['resolution'],
                                                  variable=self.variables[curr_class][sub_key],
                                                  command=getattr(self.app.widget(curr_class.__name__), f'adjust_{sub_key}'))
        self.widgets[curr_class]['scale'].pack(side=LEFT, fill=X, expand=True)
        if self.app.arg('verbose'):
            print(f'{" " * 7}- column 1: Scale widget {curr_class.__name__}[\'{sub_key}\']')

        trace_id = self.variables[curr_class][sub_key].trace('w', self.update_value_label)
        self.variables[curr_class][sub_key].trace_id = trace_id

        self.variables[curr_class][sub_key].set(self.app.config(sub_key, w=curr_class))  # Updates Var (and Label).
        # self.update_value_label(name=var_name)  # Not needed, because of trace_id variable bind

    def _create_widget_radiobutton(self, curr_class, sub_key, curr_dict):
        self._create_variable_type(curr_class, sub_key, curr_dict)
        trace_id = self.variables[curr_class][sub_key].trace('w', self.update_value_label)
        self.variables[curr_class][sub_key].trace_id = trace_id

        temp_frame = self._create_widget_generic_frame(curr_class, sub_key)
        # font_ = font.Font(family='Courier', size='-12', weight='bold')
        self.widgets[curr_class][sub_key]['value'] = Label(master=temp_frame, font='Courier -11 bold',
                                                           text=getattr(self.app, f'{curr_dict["storage"]}')
                                                           (sub_key, w=curr_class))
        # self.widgets[curr_class][sub_key]['value'].pack(side=LEFT, fill=None, expand=True)
        self.widgets[curr_class][sub_key]['value'].grid(row=0, column=0, sticky='nsew')
        if self.app.arg('verbose'):
            print(f'{" " * 7}- column 0: Label widget \'value\' {curr_class.__name__}[\'{sub_key}\']')

        nested_frame = Frame(master=temp_frame, bg='blue')  # self.app.config('color', 'inner', w=self.__class__))
        # nested_frame.columnconfigure(index=0, weight=1)
        nested_frame.grid(row=0, column=1, sticky='nsew')
        if self.app.arg('verbose'):
            print(f'{" " * 7}- column 1: (nested) Frame widget {curr_class.__name__}[\'{sub_key}\']')

        row_index, col_index = 0, 0
        per_row = curr_dict['per_row']
        for curr_index, (name, value) in enumerate(curr_dict['options'], start=1):
            if row_index == 0:
                nested_frame.columnconfigure(index=col_index, weight=1)
            curr_button = Radiobutton(master=nested_frame, text=name, indicatoron=0, value=value, padx=0, pady=0,
                                      variable=self.variables[curr_class][sub_key],
                                      command=lambda v=value:
                                      getattr(self.app.widget(curr_class.__name__), f'adjust_{sub_key}')(v))
            curr_button.grid(row=row_index, column=col_index, sticky='nsew')
            if self.app.arg('verbose'):
                print(f'{" " * 9}- {row_index, col_index}: Radiobutton {name}, {value}')

            # increment {row, col}_index for next loop
            if col_index == per_row - 1:
                row_index += 1
            col_index = curr_index % per_row

        # Updates Label.
        self.variables[curr_class][sub_key].set(getattr(self.app, f'{curr_dict["storage"]}')(sub_key, w=curr_class))
        # self.widgets[curr_class][sub_key]['value'].configure(text=self.app.config(sub_key, w=curr_class))

    def _create_widget_canvas_screen(self, curr_class, sub_key, curr_dict):
        screen_w, screen_h = self.app.get_max_screen_dimensions()
        ratio = screen_w / self.winfo_reqwidth()
        canvas = Canvas(master=self.main_frame, width=self.winfo_reqwidth(), height=screen_h / ratio)
        canvas.grid(row=self.row_index, column=0, sticky='nsew')
        self.configure(width=self.winfo_reqwidth())
        if self.app.arg('verbose'):
            print(f'{" " * 5}- row {self.row_index}: Canvas widget {curr_class.__name__}[\'{sub_key}\']')
        self.row_index += 1

        for curr_index, curr_option in enumerate(curr_dict['monitors']):
            color = ('Green', 'Red')[curr_option['hidden']]
            curr = Canvas(master=canvas, width=curr_option['w'] // ratio, height=curr_option['h'] // ratio, bg=color)
            curr.place(x=curr_option['min_x'] // ratio, y=curr_option['min_y'] // ratio)
            # Misc.lift(curr)
            curr.monitor = curr_option
            curr.bind('<Button-1>', lambda _, curr_canvas=curr: self.click_canvas_screen(curr_canvas))

        self.main_frame.configure(width=self.main_frame.winfo_reqwidth())

    def get_titlebar_wh(self):
        self.titlebar.update_idletasks()
        return self.titlebar.winfo_width(), self.titlebar.winfo_height()

    # def mouse_hover_enter(self, event):
    #     event_name = event.widget.__class__.__name__
    #     target_name = self.__class__.__name__
    #     if self.app.arg('verbose') > 2:
    #         print(f'Does widget \'{event_name}\' == \'{target_name}\'? {event_name == target_name}')
    #     if event_name == target_name:
    #         print('\n> Mouse is hovering over MenuConfig. Grabbing OS focus.')
    #         self.grab_set_global()
    #
    # def mouse_hover_leave(self, event):
    #     if self.__class__.__name__.lower() not in str(event.widget).split('.!')[-1]:
    #         # mouse hovered over some other nested widget within self.widgets
    #         if self.app.arg('verbose') > 2:
    #             print(f'  - Mouse is hovering over the {str(event.widget)} widget.')
    #         return
    #     print('> Mouse is not hovering over MenuConfig anymore. Releasing focus.\n')
    #
    #     self.destroy_()

    def destroy_(self):
        if self.app.arg('verbose') > 1:
            print(f'{" " * 1}> Destroying MenuConfig.widgets')
        self.grab_release()
        for curr_class, curr_class_dict in self.widgets_create_dict.items():
            for sub_key, curr_dict in curr_class_dict.items():
                # if curr_dict['type'] == 'scale':
                try:
                    curr_var = self.variables[curr_class][sub_key]
                    try:
                        curr_var.trace_vdelete('w', curr_var.trace_id)
                    except TclError as err:
                        print(f'{"@" * 3}- Could not trace_vdelete {curr_var}.\n'
                              f'{"@" * 3}  No trace_id: {err}.')
                except KeyError as err:
                    if self.app.arg('verbose') > 2:
                        print(err)
        for widget in self.winfo_children():
            widget.forget()
            widget.destroy()

        self.app.menuconfig_close(destroyed=True)

    def update_value_label(self, name, *_):
        keys = name.split(sep=' ')
        curr_class = self.app.get_class(keys[0])  # converts str to <class>
        sub_key = keys[1]
        variable_type = self.variables[curr_class][sub_key].__class__

        label_text = str(self.variables[curr_class][sub_key].get())
        if variable_type is BooleanVar:
            while len(label_text) < 5:
                label_text += ' '
        elif variable_type is DoubleVar:
            while len(label_text) < 5:
                label_text += '0'
        elif variable_type is IntVar:
            if '.' not in label_text and int(label_text) == float(label_text):
                label_text += '.'
            while len(label_text) < 5:
                label_text += '0'

        if self.app.arg('verbose') > 1:
            print(f'{" " * 6}> updating value of {curr_class.__name__}[\'{sub_key}\'] to \'{label_text}\'')

        try:
            self.widgets[curr_class][sub_key]['value'].configure(text=label_text)
        except TclError as err:
            print(f'{"@" * 3}- Could not update {name} to {label_text}: {err}')

    def click_canvas_screen(self, curr_canvas):
        self.app.widget('ExcludedManager').adjust_screen(curr_canvas)
        color = ('Green', 'Red')[curr_canvas.monitor['hidden']]
        curr_canvas.configure(bg=color)
        pass
