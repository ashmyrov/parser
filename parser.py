import csv
import urllib.request
from bs4 import BeautifulSoup


BASE_URL = 'http://www.weblancer.net/jobs/'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_page(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('ul', class_='pagination')
    count = paggination.find_all('a')[-1]
    count_page = count['href'][-3:]
    return int(count_page)


def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_ ='container-fluid cols_table show_visited')
    rows = table.find_all('div', class_='row')

    projects = []

    for row in rows:
        cols = row.find_all('div')

        projects.append({
            'title': cols[0].a.text,
            'categories': [category.text for category in cols[0].find_all('a', class_='text-muted')],
            'price': cols[2].text.strip(),
            'application': cols[3].text.strip()
        })

    return projects


def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))

        writer.writerows(
            (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
        )


def main():

    total_pages = get_page(get_html(BASE_URL))
    projects = []

    for page in range(1,total_pages):
        print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        projects.extend(parse(get_html(BASE_URL + "?page={}".format(page))))

    print("Saving...")
    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()