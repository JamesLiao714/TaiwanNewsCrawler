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

Three crawler in `model.py` for different news company website:
- chinatimes_crawler 
- ltn_crawler 
- udn_crawler 

Use `search(keywords, pages_num, CSV)` to retrieve the dataframe conatining news info within page_num. If CSV is set to True (default=False), the searching result will be save automatically as CSV file in the folder called `search_result`.

For example,

```python
## Build news crawler
crawler = udn_crawler()
## search keywords: covid
## search first 100 results
## save the result as udn_covid_100.csv in search_result folder.
crawler.search('covid', 100, CSV=True)
## search keywords: covid
## search first 100 results
## Do not save the result as .csv file
crawler.search('covid', 100, CSV=False)
```
## Result Example
Please refer to `Demo.ipynb`

TITLE|TIME	|CATEGORY|DESCRIPTION|CONTENT|KEYWORDS|	FROM|	LINK|
:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
北市房仲傳染給新北客戶Ct值19.4 急匡列40人足跡公布|2022-01-25 15:23:00|	udn|國內疫情持續延燒，北市日前出現不明感染源，北市男房仲（案18375）曾帶一名客戶（案1851...|國內疫情持續延燒，北市日前出現不明感染源，北市男房仲（案18375）曾帶一名客戶（案1851...	|新冠肺炎,COVID-19|聯合新聞網|https://udn.com/news/story/120940/6059544
