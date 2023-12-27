class Renderer:
    def render_dict(dct: dict):
        points = ''
        for key, value in dct.items():
            points += f'<li>{key}: '
            if type(value) == str:
                points += f'"{value}"'
            elif type(value) == bytes:
                points += f'b"{value}"'
            elif type(value) == dict:
                points += f'<button class="opening-btn">show</button>{Renderer.render_dict(value)}'
            else:
                points += f'{value}'
            points += '</li>'
        return f'<ul class="ul" style="display: none">{points}</ul>'

    def render(dct: dict):
        inner_html = '''<table class="res-table"><tbody><tr><td><b>Строка</b></td><td><b>Переменные</b></td></tr>'''
        for line in dct.keys():
            inner_html += f'''<tr><td>{ line }</td><td><button class="opening-btn">show</button>{ Renderer.render_dict(dct[line]) }</td></tr>'''
        return inner_html
