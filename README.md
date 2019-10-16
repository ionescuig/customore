# customore

- scraper website
    - Lazada.vn and Shopee.vn
    - for a given search
    - only for brands
- show results in a graph

Technologies: python, django, beautifulsoup4, django-crispy-forms, django-debug-toolbar, djangorestframework

---

##### Good:
- Lazada.vn: works fine 
- search for 100 products

##### Bad:
- Shopee.vn: don't thing information is correct
- search only for 100 products (model is prepared but not accessible in form)
- the search model not connected to scraper: same results for any search

##### Maybe:
- create models for search results and give results through api
- update results every second (I don't know if is possible with django)