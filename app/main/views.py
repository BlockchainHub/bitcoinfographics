from . import main
from flask import render_template, session, redirect, request
from .. import db
from ..models import Infographic


@main.route('/')
def index():
    infographics = Infographic.query.order_by('timestamp')
    return render_template('index.html',
                            infographics=infographics,
                            lang=session.get('lang') or 'en')


@main.route('/infographic/<string:infographic_slug>')
def infographic(infographic_slug):
    infographics = Infographic.query.all()
    current_infographic = Infographic.query.filter_by(slug=infographic_slug).first_or_404()
    prev_infographic = Infographic.query.filter_by(id=current_infographic.id+1).first() or infographics[0]
    next_infographic = Infographic.query.filter_by(id=current_infographic.id-1).first() or infographics[-1]
    return render_template('infographic.html',
                               infographic=current_infographic,
                               prev_slug=prev_infographic.slug,
                               next_slug=next_infographic.slug,
                               lang=session.get('lang') or 'en')


@main.route('/donate/')
def donate():
    return render_template('donate.html')


@main.route('/about/')
def about():
    return render_template('about.html')


@main.route('/translate/')
def translate():
    lang = request.args.get('lang')
    referrer = request.referrer or '/'
    if '?' in referrer:
        print(referrer)
        referrer = referrer[:referrer.find('?')]
    if lang and lang in ('en', 'es', 'pt'):
        session['lang'] = lang
        return redirect(referrer + '?lang=' + session['lang'])
    session['lang'] = 'en'
    return redirect(referrer + '?lang=' + session['lang'])
