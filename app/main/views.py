from . import main
from flask import render_template
import json


@main.route('/')
def index():
    jsonFile = open('app/static/resources/infographics.json')
    infographicsJson = json.load(jsonFile)
    return render_template('index.html', infographics_json=infographicsJson)


@main.route('/infographic/<infographic_slug>')
def infographic(infographic_slug):
    jsonFile = open('app/static/resources/infographics.json')
    infographicsJson = json.load(jsonFile)
    return render_template('infographic.html',
                           infographic=infographic_slug,
                           infographics_json=infographicsJson)


@main.route('/donate/')
def donate():
    return render_template('donate.html')


@main.route('/contact/')
def contact():
    return render_template('contact.html')
