def get_menu_format(menu_manager):
    return [
        {  # First tab: File
            'name': 'File',
            'data': {
                menu_manager.app.get_class('FileManager'): {
                    'save': {
                        'type': 'text',
                        'var_type': 'StringVar',
                        'description': 'Save As',
                    },
                    'open': {
                        'type': 'dropdown',
                        'var_type': 'StringVar',
                        'description': 'Open File',
                        'from': 'data_dir'
                    },
                }
            },
        },
        {  # Second tab: Options
            'name': 'Options',
            'data': {
                menu_manager.app.get_class('ScreenManager'): {
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
                menu_manager.app.get_class('BorderManager'): {
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
                menu_manager.app.get_class('ExcludedManager'): {
                    'screen': {
                        'type': 'canvas_screen',
                        'var_type': 'StringVar',
                        'description': 'Hidden Screens',
                        'monitors': menu_manager.app.monitors,
                        'storage': 'config',
                    }
                },
                menu_manager.app.get_class('DemoManager'): {
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
        }
    ]
