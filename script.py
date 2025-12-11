import requests

# URL плейлиста
playlist_url = 'https://raw.githubusercontent.com/Dimonovich/TV/refs/heads/Dimonovich/FREE/TV'
# Имя файла для сохранения отфильтрованного плейлиста
output_file = 'IPTV.m3u8'

# Здесь указываем интересующие нас каналы
wanted_channels = [
    "Первый канал HD",
    "НТВ HD",
    "ТНТ HD",
    "ТНТ4 HD",
    "Пятница HD",
    "ТВ3 HD"
  ]

# Функция для получения HLS ссылки из API Rutube

def get_rutube_hls_url(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data['live_streams']['hls'][0]['url'] if 'live_streams' in data and 'hls' in data['live_streams'] else None
    else:
        print('Ошибка при запросе к API Rutube:', response.status_code)
        return None

# Получаем HLS ссылку для Соловьёв Live HD
soloviev_api_url = 'https://rutube.ru/api/play/options/c9b87c0b00cfff9b37f95b9c8e4eed42/'
soloviev_hls_url = get_rutube_hls_url(soloviev_api_url)

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

# Добавляем канал Соловьёв Live HD с динамической HLS ссылкой
if soloviev_hls_url:
    filtered_lines.append('#EXTINF:-1,Соловьёв Live HD')
    filtered_lines.append(soloviev_hls_url)
else:
    print('Не удалось получить HLS ссылку для Соловьёв Live HD')

# Обработка строк плейлиста
for channel in wanted_channels:
    for index in range(len(playlist_content)):
        line = playlist_content[index]
        if "group-title=\"Rutube (VPN)\"" in line:
            channel_name = line.split(',')[1].strip() if len(line.split(',')) > 1 else ""
            
            if channel_name == channel:
                # Изменяем название канала в зависимости от условий
                if channel_name == "ТНТ4 HD":
                    channel_name = "ТНТ-4 HD"
                elif channel_name == "Пятница HD":
                    channel_name = "Пятница! HD"
                elif channel_name == "ТВ3 HD":
                    channel_name = "ТВ-3 HD"  
              
                filtered_lines.append(f'#EXTINF:-1,{channel_name}')  # Добавляем название канала
                while index + 1 < len(playlist_content):
                    index += 1  # Перемещаемся к следующей строке
                    next_line = playlist_content[index]
                    if not next_line.startswith("#"):
                        filtered_lines.append(next_line)  # Добавляем URL-адрес потока
                    else:
                        break  # Прерываем цикл на комментарии

                # Добавляем статичные каналы
                if channel == "Первый канал HD":
                    filtered_lines.append('#EXTINF:-1,Россия 1 HD')
                    filtered_lines.append('https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8')  
                if channel == "ТНТ4 HD":
                    filtered_lines.append('#EXTINF:-1,СТС HD')
                    filtered_lines.append('http://03.stream.pg19.ru/tv/channel/110/index.m3u8?source=pgtv')
                if channel == "ТВ3 HD":
                    filtered_lines.append('#EXTINF:-1,Звезда HD')
                    filtered_lines.append('http://tvchannelstream1.tvzvezda.ru/cdn/tvzvezda/playlist_hdhigh.m3u8')
                    filtered_lines.append('#EXTINF:-1,Звезда Плюс HD')
                    filtered_lines.append('http://tvzvezda.bonus-tv.ru/cdn/zvezdaplus/mono.ts.m3u8')
                    filtered_lines.append('#EXTINF:-1,Мир HD')
                    filtered_lines.append('http://hls-mirtv.cdnvideo.ru/mirtv-parampublish/mirtv_2500/tracks-v1a1/mono.m3u8')
                    filtered_lines.append('#EXTINF:-1,Мир 24 HD')
                    filtered_lines.append('http://hls-mirtv.cdnvideo.ru/mirtv-parampublish/mir24_2500/tracks-v1a1/mono.m3u8')
                    filtered_lines.append('#EXTINF:-1 group-title="Украина",Iнтер HD')
                    filtered_lines.append('http://141.8.193.88:7034/110.m3u8')
                    filtered_lines.append('#EXTINF:-1,1+1 HD')
                    filtered_lines.append('http://141.8.193.88:7034/124.m3u8')
                    filtered_lines.append('#EXTINF:-1,Freedom HD')
                    filtered_lines.append('http://141.8.193.88:7034/91.m3u8')
                    filtered_lines.append('#EXTINF:-1,5 канал HD')
                    filtered_lines.append('http://api-tv.ipnet.ua/api/v1/manifest/2118742539.m3u8')
                    filtered_lines.append('#EXTINF:-1,24 канал HD')
                    filtered_lines.append('http://streamvideol1.luxnet.ua/news24/livenews_1080p/index.m3u8')
                    filtered_lines.append('#EXTINF:-1,Прямий HD')
                    filtered_lines.append('http://141.8.193.88:7034/3615.m3u8')
                    filtered_lines.append('#EXTINF:-1,Еспресо TV HD')
                    filtered_lines.append('http://api-tv.ipnet.ua/api/v1/manifest/2118742594.m3u8')
                    filtered_lines.append('#EXTINF:-1,Київ ТБ HD')
                    filtered_lines.append('http://api-tv.ipnet.ua/api/v1/manifest/1293296300.m3u8')

                
                break  # Выйти из внешнего цикла после добавления канала

# Запись отфильтрованного плейлиста в файл с учетом кодировки
with open(output_file, 'w', encoding='utf-8') as file:
    for line in filtered_lines:
        file.write(f"{line}\n")

print(f'Создан плейлист: {output_file}')




