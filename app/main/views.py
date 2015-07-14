from . import main
from flask import render_template, abort
import json


@main.route('/')
def index():
    with open('app/static/resources/infographics_index.json') as jsonFile:
        infographicsJson = json.load(jsonFile)
        return render_template('index.html',
                               infographics_json=infographicsJson)


@main.route('/infographic/<infographic_slug>')
def infographic(infographic_slug):
    with open('app/static/resources/infographics.json') as jsonFile, open('app/static/resources/infographics_index.json') as indexedFile:
        infographicsJson = json.load(jsonFile)
        indexedJson = json.load(indexedFile)
        index = None
        if infographicsJson.get(infographic_slug) is not None:
            index = infographicsJson.get(infographic_slug)['index']
        else:
            abort(404)
        next_index = None
        prev_index = None
        if index == 0:
            prev_index = len(infographicsJson)-1
            next_index = 1
        elif index == len(infographicsJson)-1:
            prev_index = len(infographicsJson)-2
            next_index = 0
        else:
            prev_index = index - 1
            next_index = index + 1
        prev_slug = indexedJson[str(prev_index)]['slug']
        next_slug = indexedJson[str(next_index)]['slug']
        return render_template('infographic.html',
                               infographic=infographic_slug,
                               infographics_json=infographicsJson,
                               next_slug=next_slug,
                               prev_slug=prev_slug)


@main.route('/donate/')
def donate():
    return render_template('donate.html')
