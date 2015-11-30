from . import main
from flask import render_template, url_for, redirect
from ..models import db
from ..models import Infographic


@main.route('/')
@main.route('/<lang>/')
def index(lang='en'):
    if lang not in ('en', 'pt', 'es'):
        return redirect(url_for('main.index', lang='en'))
    infographics = Infographic.query.order_by('timestamp')
    return render_template('index.html',
                            infographics=infographics,
                            lang=lang)


@main.route('/<string:infographic_slug>/')
@main.route('/<lang>/<string:infographic_slug>/')
def infographic(infographic_slug, lang='en'):
    if lang not in ('en', 'pt', 'es'):
        return redirect(url_for('main.infographic', infographic_slug=infographic_slug, lang='en'))
    infographics = Infographic.query.all()
    current_infographic = Infographic.query.filter_by(slug=infographic_slug).first_or_404()
    prev_infographic = Infographic.query.filter_by(id=current_infographic.id+1).first() or infographics[0]
    next_infographic = Infographic.query.filter_by(id=current_infographic.id-1).first() or infographics[-1]
    return render_template('infographic.html',
                               infographic=current_infographic,
                               prev_slug=prev_infographic.slug,
                               next_slug=next_infographic.slug,
                               lang=lang)


@main.route('/infographic/<string:infographic_slug>/')
@main.route('/<lang>/infographic/<string:infographic_slug>/')
def old_infographic(infographic_slug, lang='en'):
    return redirect(url_for('main.infographic', infographic_slug=infographic_slug,lang=lang))


@main.route('/donate/')
def donate():
    return render_template('donate.html')


@main.route('/about/')
def about():
    return render_template('about.html')

