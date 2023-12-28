class Renderer:
    def render_dict(dct: dict):
        points = ''
        for key, val in dct.items():
            value = val['value']
            type_ = val['type']
            if type_ == 'str':
                points += f'<li class="variable-str">{key}: "{value}"'
            elif type_ == 'bytes':
                points += f'<li class="variable-str">{key}: b"{value}"'
            elif type_ == 'dict':
                points += f'<li class="variable-dict">{key}: <span class="ellipsis">...</span>{Renderer.render_dict(value)}'
            elif type_ == 'NoneType':
                points += f'<li class="variable-none">{key}: {value}'
            elif type_ == 'int':
                points += f'<li class="variable-int">{key}: {value}'
            elif type_ == 'module':
                points += f'<li class="variable-package">{key}: {value}'
            else:
                points += f'<li class="variable-class">{key}: {value}'
            points += '</li>'
        return f'<ul class="variables-list" style="display: none">{points}</ul>'

    def render(dct: dict):
        inner_html = '''<table class="results-table"><tbody><tr id="head"><td>Line</td><td>Variables' values</td></tr>'''
        for line in dct.keys():
            inner_html += f'''<tr><td>{ line }</td><td><span class="ellipsis">...</span>{ Renderer.render_dict(dct[line]) }</td></tr>'''
        return inner_html
