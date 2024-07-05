def to_form(data: list):
    ''' Из полученного списка образуем словарь валидный для excel '''
    result = {}
    
    for i in data:
        if 'www.twitch.tv' in i[0]:
            result['A'] = i[0]
            result['B'] = i[1]

        if 'youtube' in i[0]:
            result['C'] = i[0]
            result['D'] = i[1]

        if 'vk.com' in i[0]:
            result['E'] = i[0]
            result['F'] = i[1]

        if 't.me' in i[0]:
            result['G'] = i[0]
            result['H'] = i[1]


        if 'tiktok' in i[0]:
            result['I'] = i[0]
            result['J'] = i[1]


    return result