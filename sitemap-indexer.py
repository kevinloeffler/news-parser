import csv
from usp.tree import sitemap_tree_for_homepage


def index_pages(domains: list[str], names: list[str]):
    for i in range(len(domains)):
        index_page(domains[i], names[i])


def index_page(domain: str, name: str):
    pages = get_pages_from_sitemap(domain)
    for i in range(0, 100):
        try:
            new_name = name if (i == 0) else f'{name}_1'
            write_csv(pages, new_name)
            break
        except FileExistsError:
            continue


def get_pages_from_sitemap(domain: str) -> list[str]:
    tree = sitemap_tree_for_homepage(domain)
    pages = []
    for page in tree.all_pages():
        pages.append(page.url)

    return pages


def write_csv(list_of_pages: list[str], name: str):
    with open(f'sitemaps/{name.replace(" ", "_")}.csv', 'x', newline='') as file:
        fields = ['link']
        writer = csv.writer(file)

        for page in list_of_pages:
            writer.writerow([page])


# index_pages(domains, names)


domains = []
names = []

index_pages(domains, names)
