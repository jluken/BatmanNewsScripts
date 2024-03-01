import xlsxwriter
import requests
from bs4 import BeautifulSoup

months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

class Post:
    def __init__(self, title, author, date):
        self.title = title
        self.author = author
        self.date = date

    def __str__(self):
        return f'(Title: {self.title}, Author: {self.author}, Date: {self.date})'

    def __repr__(self):
        return f'(Title: {self.title}, Author: {self.author}, Date: {self.date})'


def collect_posts(month, html):
    posts = []
    articles = html.find_all('article')
    for article in articles:
        author = next(span.contents[0].strip() for span in article.findAll('span', attrs={'class':'author-name'}))
        date = next(span.contents[0].strip() for span in article.findAll('span', attrs={'class': 'published'}))
        title = next(h2.find('a').contents[0].strip() for h2 in article.findAll('h2', attrs={'itemprop': 'headline'}))
        if month.lower() in date.lower():
            posts.append(Post(title, author, date))
    return posts


def write_sheets(month, posts):
    authors = set([post.author for post in posts])
    author_sets = {author: [post for post in posts if post.author == author] for author in authors}
    workbook = xlsxwriter.Workbook(month + '.xlsx')
    totals = workbook.add_worksheet('Totals')
    row = 0
    totals.write_row(row, 0, ['', 'Pageviews', 'Ext', 'Writer\'s Pay'])
    for author, posts in author_sets.items():
        row += 1
        sheet_name = '\'' + author + '\''
        sum_row = len(posts) + 2
        totals.write_row(row, 0,
                         [author, '=' + sheet_name + f'!C{sum_row}', '=' + sheet_name + f'!E{sum_row}',
                          '=' + sheet_name + f'!F{sum_row}'])
    totals.write_row(len(authors)+1, 0, ['', f'=SUM(B2:B{len(authors)+1})', f'=SUM(C2:C{len(authors)+1})',
                                         f'=SUM(D2:D{len(authors)+1})'])

    for author, author_posts in author_sets.items():
        author_sheet = workbook.add_worksheet(author)
        row = 0
        author_sheet.write_row(row, 0,
                               ['Review', 'Original Date', 'Week 1', 'Ext', 'Old Pay', 'New Pay', '% to Writer'])
        for author_post in author_posts[::-1]:
            row += 1
            author_sheet.write_row(row, 0, [author_post.title, author_post.date, '',
                                            f'=SUM((C{row + 1}/1000)*3.4)', f'=SUM(D{row + 1}*0.4)',
                                            f'=MAX(E{row + 1}, 3)',
                                            f'=F{row + 1}/D{row + 1}'])
        sum_row = len(author_posts) + 1
        author_sheet.write_row(sum_row, 0, ['Sums', '', f'=SUM(C2:C{sum_row})', f'=SUM(D2:D{sum_row})',
                                            f'=SUM(E2:E{sum_row})', f'=SUM(F2:F{sum_row})'])
    workbook.close()


def create_sheets(month):
    posts = []
    new_posts = []
    page_num = 0
    max_pages = 10
    while not posts or new_posts:
        page_num += 1
        url = f'https://batman-news.com/page/{page_num}/'
        req = requests.get(url)
        html = BeautifulSoup(req.content, features="html.parser")

        new_posts = collect_posts(month, html)
        posts += new_posts
        if page_num >= max_pages and not posts:
            cont = input(f"Found no posts for month '{month}' within first {max_pages} pages. Continue searching? Y/N ")
            while cont.lower() not in ['y', 'n']:
                cont = input(f"'{cont}' is an invalid input. Please enter 'Y' or 'N' ")
            if cont.lower() == 'n':
                raise Exception('No posts found')
            max_pages += 10

    write_sheets(month, posts)


if __name__ == '__main__':
    month_to_grab = input('What month would you like to collect data for? ')
    while month_to_grab.lower() not in months:
        month_to_grab = input(f"'{month_to_grab}' is not considered a valid month. Please try again. ")
    create_sheets(month_to_grab)

