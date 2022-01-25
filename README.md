# TaiwanNewsCrawler
#### Cooperating with [NTHU CTM (科技管理研究所)](http://www.ctm.nthu.edu.tw/) to collect news from top 3 news company in Taiwan
- 自由時報
- 中國時報
- 聯合新聞網

## Introduction
This is a news crawler for 3 Taiwanese mainstream media.
The crawlered media is listed below.

Media Type|Meida Name (CN)|Media Name (EN)|ID|Abbreviation
:---:|:---:|:---:|:---:|:---:
|Print Media|自由時報|Liberty News|0|ltn
|Print Media|聯合報|UDN News|1|udn
|Print Media|中國時報|China Times|2|chinatimes

## Usage

`model.py`
- chinatimes_crawler
- ltn_crawler
- udn_crawler

Use `search(keywords, pages_num)` to retrieve the dataframe conatining news info within page_num.

For example,

```python
## Build news crawler
crawler = ltn_crawler()
## search keywords: 帥哥
## search first 100 results
crawler.search('帥哥', 100)
```
## Result

TITLE	TIME	CATEGORY	DESCRIPTION	CONTENT	KEYWORDS	FROM	LINK
TITLE|TIME	|CATEGORY|DESCRIPTION|CONTENT|KEYWORDS|	FROM|	LINK|
:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
北市房仲傳染給新北客戶Ct值19.4 急匡列40人足跡公布|2022-01-25 15:23:00|	udn|國內疫情持續延燒，北市日前出現不明感染源，北市男房仲（案18375）曾帶一名客戶（案1851...|國內疫情持續延燒，北市日前出現不明感染源，北市男房仲（案18375）曾帶一名客戶（案1851...	|新冠肺炎,COVID-19|聯合新聞網|https://udn.com/news/story/120940/6059544
