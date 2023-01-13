# тут будут функции, обрабатывающие запросы

import aiohttp_jinja2


# создаем функцию, которая будет отдавать html-файл
@aiohttp_jinja2.template("index.html")
async def index(request):
    return {'title': 'Пишем первое приложение на aiohttp'}
