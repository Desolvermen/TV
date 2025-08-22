import requests

# URL плейлиста
playlist_url = 'https://raw.githubusercontent.com/Dimonovich/TV/refs/heads/Dimonovich/FREE/TV'
# Имя файла для сохранения отфильтрованного плейлиста
output_file = 'IPTV.m3u8'

# Здесь указываем интересующие нас каналы
wanted_channels = [
    "Первый канал HD",
    "Россия 1 HD",
    "НТВ HD",
    "ТНТ HD",
    "ТНТ4 HD",
    "Пятница HD",
    "ТВ3 HD",
    "Звезда",
    "Мир",
    "Мир 24",
    "РБК",
    "Матч ТВ HD",
    "ТНТ Music",
    "МузТВ"
]

# Загружаем плейлист
response = requests.get(playlist_url)
if response.status_code == 200:
    playlist_content = response.text.splitlines()  # Преобразуем в список строк
else:
    print('Ошибка при загрузке плейлиста:', response.status_code)
    exit(1)

# Список отфильтрованных строк
filtered_lines = []

# Добавляем заголовок M3U
filtered_lines.append('#EXTM3U')

# Обработка строк плейлиста
for channel in wanted_channels:
    if channel == "Россия 1 HD":
        # Добавляем статичный канал Россия 1 HD после Первого канала
        filtered_lines.append('#EXTINF:-1,Россия 1 HD')
        filtered_lines.append('https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8')
    for index in range(len(playlist_content)):
        line = playlist_content[index]
        if "group-title=\"Rutube (VPN)\"" in line:
            channel_name = line.split(',')[1].strip() if len(line.split(',')) > 1 else ""
            if channel_name == channel:
                filtered_lines.append(f'#EXTINF:-1,{channel_name}')  # Добавляем только имя канала
                while index + 1 < len(playlist_content):
                    index += 1  # Перемещаемся к следующей строке
                    next_line = playlist_content[index]
                    if not next_line.startswith("#"):
                        filtered_lines.append(next_line)  # Добавляем URL-адрес потока
                    else:
                        break  # Прерываем цикл на комментарии
                if channel == "Звезда":
                    # Добавляем статичный канал Звезда Плюс HD после Звезда
                    filtered_lines.append('#EXTINF:-1,Звезда Плюс HD')
                    filtered_lines.append('http://tvzvezda.bonus-tv.ru/cdn/zvezdaplus/mono.ts.m3u8')
                break  # Выйти из внешнего цикла после добавления канала

# Запись отфильтрованного плейлиста в файл с учетом кодировки
with open(output_file, 'w', encoding='utf-8') as file:
    for line in filtered_lines:
        file.write(f"{line}\n")

print(f'Отфильтрованный плейлист сохранён в: {output_file}')