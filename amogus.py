
def get_spaces_(line: str):
    space_cnt = 0
    for char in line:
        if char != ' ':
            break
        else:
            space_cnt += 1
    return space_cnt

get_spaces_('        print("!!!")')

a = 0
while True:
    a += 1