import json
import random
from datetime import datetime
from collections import defaultdict
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse, HttpResponseNotFound
from hypernews import settings


class LohView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class HomeView(View):

    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q')
        if q:
            with open(settings.NEWS_JSON_PATH, 'r') as f:
                news_file = json.load(f)
            if news_file is None:
                return render(request, 'main.html', context={'new_dict': {''}})
            else:
                sorted_news = sorted(news_file, key=lambda i: i['created'], reverse=True)
                for item in news_file:
                    item['created'] = item['created'].split()[0]
                new_dict = {}
                for item in sorted_news:
                    if item['created'] not in new_dict:
                        if str(q) in item['title']:
                            new_dict[item['created']] = [item]
                    else:
                        if item:
                            if str(q) in item['title']:
                                new_dict[item['created']].append(item)
                return render(request, 'main.html', context={'new_dict': new_dict})
        else:
            with open(settings.NEWS_JSON_PATH, 'r') as f:
                news_file = json.load(f)
            if news_file is None:
                return render(request, 'main.html', context={'new_dict': {''}})
            else:
                sorted_news = sorted(news_file, key=lambda i: i['created'], reverse=True)
                for item in news_file:
                    item['created'] = item['created'].split()[0]
                new_dict = {}
                for item in sorted_news:
                    if item['created'] not in new_dict:
                        new_dict[item['created']] = [item]
                    else:
                        new_dict[item['created']].append(item)
                return render(request, 'main.html', context={'new_dict': new_dict})  # HttpResponse('Coming soon')

    #def get_queryset(self):
    #    return .filter(
    #        Q(name__icontains='Boston') | Q(state__icontains='NY')
    #    )



class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
        article = list(filter(lambda x: x['link'] == int(article_id), data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'article.html', context={'article': article[0]})
# {% extends "base.html" %}


class CreateView(View):
    title = ''
    text = ''

    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')  # , context={}   redirect('/')


    def post(self, request, *args, **kwargs):
        self.title = request.POST.get('title')
        self.text = request.POST.get('text')
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            old_news = json.load(f)
            if not old_news:
                new_link = random.randint(0, 1000000)
                new_news = [{'created': datetime.now(tz=None), 'text': self.text, 'title': self.title, 'link': new_link}]
                with open(settings.NEWS_JSON_PATH, 'w') as g:
                    json.dump(new_news, g)
                return redirect('/')
            while True:
                new_link = random.randint(0, 1000000)
                for i in range(len(old_news)):
                    # for z, link, x, c in enumerate(old_news[i]['link']):
                    if old_news[i]['link'] == new_link:
                        continue
                break
        old_news.append({'created': str(datetime.now(tz=None)).split('.')[0], 'text': str(self.text), 'title': str(self.title), 'link': new_link})
        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(old_news, f)
        return redirect('/news/')  # render(request, 'create.html'), context={}


"""
class SearchView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('sasi)))')
        
        with open(settings.NEWS_JSON_PATH, 'r') as f:
            news_file = json.load(f)
        if news_file is None:
            return render(request, 'main.html', context={'new_dict': {''}})
        else:
            sorted_news = sorted(news_file, key=lambda i: i['created'], reverse=True)
            for item in news_file:
                item['created'] = item['created'].split()[0]
            new_dict = {}
            for item in sorted_news:
                # new_dict.append(item)
                if item['created'] not in new_dict:
                    new_dict[item['created']] = [item]
                else:
                    new_dict[item['created']].append(item)
            return render(request, 'main.html', context={'new_dict': new_dict})  # HttpResponse('Coming soon')"""




