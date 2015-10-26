from . import main
from flask import render_template, abort, make_response, request, redirect
from .. import db
from ..models import Infographic


def check_lang():
  if 'lang' in request.cookies:
    return request.cookies['lang']
  else:
    return 'en'


@main.route('/')
def index():
    lang = check_lang()
    infographics = Infographic.query.order_by('timestamp')
    return render_template('index.html', infographics=infographics, lang=lang)


@main.route('/infographic/<string:infographic_slug>')
def infographic(infographic_slug):
    lang = check_lang()
    infographics = Infographic.query.all()
    current_infographic = Infographic.query.filter_by(slug=infographic_slug).first_or_404()
    prev_infographic = Infographic.query.filter_by(id=current_infographic.id+1).first() or infographics[0]
    next_infographic = Infographic.query.filter_by(id=current_infographic.id-1).first() or infographics[-1]
    return render_template('infographic.html',
                               infographic=current_infographic,
                               prev_slug=prev_infographic.slug,
                               next_slug=next_infographic.slug,
                               lang=lang)


@main.route('/donate/')
def donate():
    return render_template('donate.html')


@main.route('/about/')
def about():
    return render_template('about.html')


@main.route('/translate/')
def translate():
    referrer = request.referrer or '/'
    response = make_response(redirect(referrer))
    if request.args.get('lang') in ('en', 'es', 'pt'):
      response.set_cookie('lang', request.args.get('lang'))
    return response
