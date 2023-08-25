def remove_comments(code: str) -> str:
    lines = code.splitlines()
    no_comm = ''
    in_comment = False
    for line in lines:
        line = line.strip()
        if line.startswith('//'): continue
        mlcomm_start = line.find('/*')
        mlcomm_end = line.find('*/')
        if not in_comment:
            if mlcomm_end != -1:
                raise SyntaxError('*/ found but no /* found')
            if mlcomm_start == -1 and mlcomm_end == -1:
                no_comm += line
                continue
            if mlcomm_start != -1 and mlcomm_end == -1:
                no_comm += line[:mlcomm_start].strip()
                in_comment = True
                continue
            if mlcomm_start != -1 and mlcomm_end != -1:
                no_comm += line[:mlcomm_start].strip() + line[mlcomm_end + 2:].strip()
        else:
            if mlcomm_end != -1:
                no_comm += line[mlcomm_end + 2:].strip()
                in_comment = False
    
    return no_comm

def parse_chip_call(input_string):
    components = input_string.split(', ')
    result_dict = {}
    
    for component in components:
        key, value = component.split('=')
        result_dict[key.strip()] = value.strip()
    
    return result_dict

def extract_and_sort_values(d, s):
    selected_values = []

    for key, value in d.items():
        if key.startswith(s + '['):
            index = int(key[len(s) + 1:-1])
            selected_values.append((index, value))

    selected_values.sort(key=lambda x: x[0])
    sorted_values = [value for index, value in selected_values]

    return sorted_values