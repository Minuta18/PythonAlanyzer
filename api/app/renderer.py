class Renderer:
    def render_dict(dct: dict):
        points = ''
        for key, value in dct.items():
            points += f'<li class="variable-int">{key}: '
            if type(value) == str:
                points += f'"{value}"'
            elif type(value) == bytes:
                points += f'b"{value}"'
            elif type(value) == dict:
                points += f'<span class="ellipsis">...</span>{Renderer.render_dict(value)}'
            else:
                points += f'{value}'
            points += '</li>'
        return f'<ul class="variables-list" style="display: none">{points}</ul>'

    def render(dct: dict):
        inner_html = '''<table class="results-table"><tbody><tr id="head"><td>Line</td><td>Variables' values</td></tr>'''
        for line in dct.keys():
            inner_html += f'''<tr><td>{ line }</td><td><span class="ellipsis">...</span>{ Renderer.render_dict(dct[line]) }</td></tr>'''
        return inner_html
