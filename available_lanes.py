#!/usr/bin/env python3

import requests
import bs4
import datetime
import pytz
import locale


def proccess_stats():
    days = []
    res = requests.get('https://www.kravihora-brno.cz/kryta-hala/rozpis', verify=False)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    today = datetime.datetime.now()
    for i in range(0, 7):
        tmp_date = today + datetime.timedelta(days=i)
        table_key = tmp_date.strftime('%Y%m%d')

        table = soup.find_all('table', class_='reservation-day-{0}'.format(table_key))

        lines = table[0].find_all('tr')

        # print(table)

        lanes = lines[1:7]
        whirlpool = lines[8]

        lanes_hours = {'06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0,
                       '17': 0, '18': 0, '19': 0, '20': 0, '21': 0}

        whirlpool_hours = {'06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0,
                           '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0}

        tmp_day = {'day': tmp_date, 'lanes_hours': lanes_hours, 'whirlpool_hours': whirlpool_hours}

        for lane in lanes:
            tds = lane.find_all('td', class_='reservable')
            for td in tds:
                if td.has_attr('class'):
                    hour = td['class'][0][4:6]
                    tmp_day['lanes_hours'][hour] += 1

        tds = whirlpool.find_all('td', class_='reservable')
        for td in tds:
            if td.has_attr('class'):
                hour = td['class'][0][4:6]
                tmp_day['whirlpool_hours'][hour] += 1

        days.append(tmp_day)

    return days


def generate_html(days, file_location):
    with open(file_location, 'w', encoding='utf-8') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<meta charset="UTF-8">\n')
        f.write(
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">')
        f.write(
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">')
        f.write(
            '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>')
        f.write('<title>Obsazenost</title>\n')
        f.write('</head>\n')
        f.write('<body>\n')

        f.write('<div style="text-align: center; align-self: center; margin: auto; align-content: center;">\n')
        f.write('<h2>Volné dráhy v krytém bazénu na Kraví hoře</h2>\n')
        f.write('<h4>Aktualizováno v {0} </h4>\n'.format(datetime.datetime.now().strftime('%A %d.%m.%Y %H:%M:%S')))
        f.write('<div class="panel panel-default" style="width: 90%; align-self: center;margin: auto;">\n')
        f.write('<table class="table table-hover table-responsive table-bordered" style="width: 100%; margin: auto">\n')
        f.write('<tbody>\n')
        f.write(
            '<tr class="info">'
            '<th style="vertical-align: middle; border: 2px solid">Datum</th>'
            '<th style="text-align: center; border: 2px solid">06:00<br>-<br>07:00</th>'
            '<th style="text-align: center; border: 2px solid">07:00<br>-<br>08:00</th>'
            '<th style="text-align: center; border: 2px solid">08:00<br>-<br>09:00</th>'
            '<th style="text-align: center; border: 2px solid">09:00<br>-<br>10:00</th>'
            '<th style="text-align: center; border: 2px solid">10:00<br>-<br>11:00</th>'
            '<th style="text-align: center; border: 2px solid">11:00<br>-<br>12:00</th>'
            '<th style="text-align: center; border: 2px solid">12:00<br>-<br>13:00</th>'
            '<th style="text-align: center; border: 2px solid">13:00<br>-<br>14:00</th>'
            '<th style="text-align: center; border: 2px solid">14:00<br>-<br>15:00</th>'
            '<th style="text-align: center; border: 2px solid">15:00<br>-<br>16:00</th>'
            '<th style="text-align: center; border: 2px solid">16:00<br>-<br>17:00</th>'
            '<th style="text-align: center; border: 2px solid">17:00<br>-<br>18:00</th>'
            '<th style="text-align: center; border: 2px solid">18:00<br>-<br>19:00</th>'
            '<th style="text-align: center; border: 2px solid">19:00<br>-<br>20:00</th>'
            '<th style="text-align: center; border: 2px solid">20:00<br>-<br>21:00</th>'
            '<th style="text-align: center; border: 2px solid">21:00<br>-<br>22:00</th></tr>')

        for day in days:
            f.write('<tr>\n')
            f.write('<td style="border: 2px solid">')
            f.write(day['day'].strftime('%A %d.%m.%Y'))
            f.write('</td>')
            for hour_value in day['lanes_hours'].values():
                if hour_value == 6:
                    background = '#9fffa5'
                elif hour_value == 0:
                    background = '#ff1a1a'
                else:
                    background = '#ffc14d'

                f.write('<td style="background: {0}; text-align: center; border: 2px solid; font-weight: bold">{1}</td>'.format(background, hour_value))
            f.write('</tr>\n')

        f.write('</tbody>\n')
        f.write('</table>\n')
        f.write('</div>\n')
        f.write('</div>\n')
        f.write('</body>\n')
        f.write('</html>\n')


def main():
    locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
    global local_tz
    local_tz = pytz.timezone('Europe/Prague')
    days = proccess_stats()

    prefix_path = '/var/www/my_web/pool_stats/'
    generate_html(days, prefix_path + 'available_lanes.html')


if __name__ == '__main__':
    main()