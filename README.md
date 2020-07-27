# Literature_survey

A Python code to automate literature survey.

We all know that doing a literature survey is a daunting task, often taking a lot of time. This code aims to speed up this process. It searches Google Scholar for a given query, download .pdf files and organize them. With this code you can do your initial literature search in seconds!

## Prerequisites

Python : `selenium`

Browser: `chromedriver` is using Google Chrome. If you need support for other browsers, feel free to contact me.

## How to install

`git clone https://github.com/mgierada/literature_survey.git`

## How to run

Run the following python script:

```python
#!/usr/bin/env python3
query = 'research chemistry physics'
ls = LiteratureSurvey(query)
ls.run()
```
