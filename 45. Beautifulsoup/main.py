from bs4 import BeautifulSoup
import requests

response = requests.get("https://appbrewery.github.io/news.ycombinator.com/")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")
articles = soup.find_all(name="a", class_="storylink")
article_texts = []
article_links = []
for article_tag in articles:
    article_texts.append(article_tag.getText())
    article_links.append(article_tag.get("href"))

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

# print(article_texts)
# print(article_links)
# print(article_upvotes)

max_upvote = max(article_upvotes)
max_index = article_upvotes.index(max_upvote)
print(f"Most upvoted article: {article_texts[max_index]} with {max_upvote} upvotes and link: {article_links[max_index]}")

# with open(r"C:\Code\100DaysCourse\45. Beautifulsoup\website.html", "r") as f:
#     content = f.read()

# soup = BeautifulSoup(content, "html.parser")

# soup.title
# soup.title.name
# print(soup.title.string)

# print(soup.a)  # first anchor tag
# print(soup.find_all(name="a"))  # all anchor tags
# for tag in soup.find_all(name="a"):
#     print(tag.getText())
#     print(tag.get("href"))

# heading = soup.find(name="h1", id="name")
# print(heading.string)

# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.get("class"))

# company_url = soup.select_one(selector="p a")
# print(company_url.get("href"))

# name = soup.select_one(selector="#name")
# print(name.getText())