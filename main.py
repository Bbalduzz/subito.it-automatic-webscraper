import bs4, requests, webbrowser
import datetime
import time
from pprint import pprint


def tutto():
    LINK = 'https://www.subito.it/annunci-emilia-romagna/vendita/informatica/bologna/?q=macbook&from=top-bar' # ==> DA MODIFICARE <==
    PRE_LINK_ANNUNCIO = 'https://www.subito.it/informatica/' # ==> DA MODIFICARE <==

    res = requests.get(LINK) #invio una richiesta "get" alla pagina del link
    res.raise_for_status

    soup = bs4.BeautifulSoup(res.text, 'html.parser') #prendo il codice della pagina

    div_annunci = soup.find('div', class_='jsx-311129296 items visible')
    a_annunci = div_annunci.find_all('a')

    link_annunci = []
    for a_annuncio in a_annunci:
        link_annuncio = str(a_annuncio.get('href'))
        if PRE_LINK_ANNUNCIO in link_annuncio:
            link_annunci.append(link_annuncio)

    # pprint(link_annunci)

    f = open('risultati_salvati.txt', 'a')
    old_link_annunci = [riga.rstrip('\n') for riga in open('risultati_salvati.txt')]
    new_link_annunci = []
    for link_annuncio in link_annunci:
        if link_annuncio not in old_link_annunci:
            new_link_annunci.append(link_annuncio)
            f.write('%s\n' % link_annuncio)
    f.close()

    if new_link_annunci:
        print('Nuovi link trovati! Apertura in corso...')
        for new_link in new_link_annunci:
            webbrowser.open(new_link)
    else:
        print('Nessun nuovo annuncio')


# run lo script ogni giorno automaticamente (è accessiorio, può essere tolto)
next_start = datetime.datetime(2022, 5, 29, 11, 0, 0)
while True:
    dtn = datetime.datetime.now()

    if dtn >= next_start:
        next_start += datetime.timedelta(1)  # 1 day
        tutto()

    time.sleep(1)


