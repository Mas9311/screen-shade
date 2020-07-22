import sys

# from src.gui.managers.border import BorderManager
# from src.gui.toplevels.menu import MenuConfig
# from src.gui.managers.demo import DemoManager
# from src.gui.managers.screen import ScreenManager
from src.helpers.path_helper import get_config_path, make_sure_data_dir_exists, config_file_exists


def import_configurations(app):
    if config_file_exists():
        print('\nPrevious configurations file found.')
        config_dict = import_from_file(app)
        # TODO: verify config file is valid
        # if is_valid_config_file(config_dict):
        print('Successfully loaded configurations file.\n')
        return config_dict
        # else:
        #     print('Errors found in previous configuration. Merging with default configurations')
        #     return merge_configurations(config_dict)
    print('Loading default configurations')
    from src.defaults import DEFAULT_CONFIGURATIONS
    return DEFAULT_CONFIGURATIONS


def import_from_file(app):
    verbose = app.arg('verbose')
    if verbose:
        print(f'\n\n{"*" * 40}\nSTART: Import configurations from file\n{"*" * 40}')
    with open(get_config_path(), 'r') as import_f:
        lines = import_f.read().splitlines()
        import_f.close()

    output_dict = {}
    for line_number, line in enumerate(lines):
        if verbose:
            print(f'[before] conversion:  input_line `{line}`')
        key, value = convert_str_dict_to_dict(line, verbose)
        key_class = app.get_class(key)
        if verbose:
            break_line = ('-' * 10 + ' ') * 5 + '\n'
            print(f'[after]  conversion:  output_dict[{key_class.__name__}]: {value}')
            if line_number < len(lines) - 1:
                # prints a ----- line to separate lines of input file.
                print(f'{break_line * int(verbose)}', end='')
        output_dict[key_class] = value
    if verbose:
        print(f'{"*" * 40}\nFINISH: Import configurations from file\n{"*" * 40}\n\n')
    return output_dict


def export_to_file(dict_, verbose):
    """Writes App.config_dict dict to the file as key{tab}value"""
    if verbose > 1:
        print(f'{"*" * 37}\nSTART: Export configurations to file\n{"*" * 37}')
    make_sure_data_dir_exists()
    lines = convert_dict_to_str(dict_, verbose)
    if verbose > 3:
        print(f' * Before conversion: {dict_}')
    if verbose > 1:
        print(f' * After conversion: ', end='\n\t')
        print(f'\n\t'.join(lines))

    with open(get_config_path(), 'w') as export_f:
        for line in lines:
            export_f.write(f'{line}\n')
        export_f.close()

    if verbose > 1:
        print(f'{"*" * 38}\nFINISH: Export configurations to file\n{"*" * 38}\n\n')


def convert_dict_to_str(dict_, verbose):
    if verbose > 1:
        print('  - converting dict to str:', dict_)
    lines = []
    for key, value in dict_.items():
        from src.gui.managers.border import BorderManager
        from src.gui.managers.demo import DemoManager
        from src.gui.managers.excluded import ExcludedManager
        from src.gui.toplevels.menu import MenuConfig
        from src.gui.managers.screen import ScreenManager
        if key in [BorderManager, DemoManager, ExcludedManager, MenuConfig, ScreenManager]:
            # convert class to str
            key = key.__name__
            if verbose > 1:
                print(f'  > parsing class key: {key}:')
        # else:
        #     # key is a string
        #     pass

        if isinstance(value, dict):
            # converts dict to str using custom `//` format
            value = f'{{{"//".join(convert_dict_to_str(value, verbose))}}}'
        elif isinstance(value, list):
            # converts list to str using custom format
            value = convert_list_to_str(value, verbose)
        elif isinstance(value, set):
            # converts set to str using custom format
            if bool(value):
                value = convert_set_to_str(value, verbose)
            else:
                value = '{}'

        lines.append(f'{key}:{value}')
    return lines


def convert_set_to_str(set_, verbose):
    if verbose > 1:
        print('    - now converting set to str:', set_)

    output = ('{}', str(set_).replace(', ', '//'))[bool(set_)]

    if verbose > 2:
        print(f'     > [After] converting set to str: \'{output}\'')
    return output


def convert_list_to_str(list_, verbose):
    output = []
    for element in list_:
        if isinstance(element, list):
            element = convert_list_to_str(element, verbose)
        elif isinstance(element, tuple):
            temp = ''
            for index, sub_element in enumerate(element):
                temp += repr(sub_element)
                if index is not len(element) - 1:
                    # no trailing commas after last element
                    temp += ','
            element = f'({temp})'
        elif isinstance(element, str):
            element = repr(element)  # Adds ' quotation marks around strings
        output.append(element)
    output = f'[{",".join(output)}]'
    if verbose > 1:
        print(f'    - converting list: {list_} => str: \'{output}\'')
    return output


def convert_set_str_to_set(line, verbose):
    if verbose > 2:
        print(f'* Now converting set_str to type set() with input_str of: `{line}`')
    index_of_open_set = line.find(':{')
    key = line[:index_of_open_set]
    val = line[index_of_open_set+2:]
    if val.rfind('}') is len(val) - 1:
        val = val[:-1]
    if verbose > 1:
        print(f' > key: `{key}`')
        print(f' > val: `{val}`')

    if val:
        data = val.split('//')
        if verbose > 1:
            print(f'  * After splitting on delimiter `//`: {data}')
        set_ = set([element.strip('\'') for element in data])
        return key, set_
    else:
        # empty set
        return key, set()


def convert_str_dict_to_dict(line, verbose):
    if verbose > 2:
        print(f'* Now converting dict_str to type dict() with input_str of: `{line}`')
    index_of_open_dict = line.find(':{')
    key = line[:index_of_open_dict]
    val = line[index_of_open_dict+2:]
    if val.rfind('}') is len(val) - 1:
        val = val[:-1]
    if verbose > 1:
        print(f' > key: `{key}`')
        print(f' > val: `{val}`')

    dict_ = convert_inner_str_dict_to_dict(val, verbose)
    return key, dict_


def convert_inner_str_dict_to_dict(input_str, verbose):
    dict_ = {}
    while input_str.find(':{') != -1:
        start_index = input_str.find(':{')
        end_index = input_str[start_index:].find('}') + len(input_str[:start_index]) + 1
        if input_str[:start_index].rfind('//') == -1:
            key_start = 0
        else:
            key_start = input_str[:start_index].rfind('//') + 2

        inner_key = input_str[key_start:start_index]
        inner_dict = input_str[key_start:end_index]
        if verbose > 2:
            print(f'  * Indexing inner dict from index range [{start_index}:{end_index}].\n'
                  f'   > inner dict: `{inner_dict}`\n'
                  f'    * inner key: `{inner_key}`\n'
                  f'    * inner val: `{input_str[start_index + 2:end_index - 1]}`')

        if inner_dict.count(':') == 1:
            key, value = convert_set_str_to_set(inner_dict, verbose)
        else:
            key, value = convert_str_dict_to_dict(inner_dict, verbose)

        dict_[key] = value
        if verbose > 1:
            print(f' > [\'{key}\']: {dict_[key]}')
        input_str = input_str[:key_start] + input_str[end_index + 2:]
        if verbose > 1:
            print(f'  * input_str after removing inner_dict: `{input_str}`')

    for curr_index, curr_item in enumerate(input_str.split('//')):
        if verbose > 2:
            print(f'  * converting item #{curr_index}: `{curr_item}`')
        if not curr_item:
            continue
        if ':' in curr_item:
            # item is dict type
            key, value = curr_item.split(':')
            if verbose > 1:
                print(f'   > [\'{key}\']: {value}')
            if not key or not value:
                continue
            if value[0] != '#':
                import ast
                value = ast.literal_eval(value)
            else:
                value = str(value)
            dict_[key] = value
        else:
            print('\n\n\nAn error has occurred in file_helper.convert_inner_str_dict_to_dict')
            print(f'Input: {input_str}')
            print(f'Item \'{curr_item}\' does not contain a colon character, `:`.')
            sys.exit()
    return dict_


# if __name__ == '__main__':
#     config_dict = import_from_file()
#     print(config_dict)
#     # sys.exit()
#
#     config_dict = {
#         Area: {
#             'alpha': 0.40,
#             'background_color': '#000000',
#             'px_radius': PX_RADIUS,
#         },
#         MenuConfig: {
#             'alpha': 0.50,
#             'background_color': {
#                 'border': '#6900db',
#                 'inner': '#303030',
#             },
#             'px_radius': 10,
#             'w': 200,
#             'h': 300,
#             'x': 0,
#             'y': 0,
#         },
#         BorderMonitor: {
#             'alpha': 0.50,
#             'background_color': '#4B8BBE',
#             'px_radius': PX_RADIUS // 2,
#             'excluded': [('HDMI-0', 'Top')]
#         },
#     }
#     print(config_dict)
#     # export_to_file(config_dict)
#     sys.exit()
