from . import main
from flask import render_template, abort, request
from .. import db
from ..models import Infographic


@main.route('/')
def index():
    infographics = Infographic.query.order_by('timestamp')
    return render_template('index.html', infographics=infographics)


@main.route('/infographic/<string:infographic_slug>')
def infographic(infographic_slug):
    infographics = Infographic.query.all()
    current_infographic = Infographic.query.filter_by(slug=infographic_slug).first_or_404()
    prev_infographic = Infographic.query.filter_by(id=current_infographic.id-1).first() or infographics[-1]
    next_infographic = Infographic.query.filter_by(id=current_infographic.id+1).first() or infographics[0]
    return render_template('infographic.html',
                               infographic=current_infographic,
                               prev_slug=prev_infographic.slug,
                               next_slug=next_infographic.slug)


@main.route('/donate/')
def donate():
    return render_template('donate.html')


@main.route('/about/')
def about():
    return render_template('about.html')
