from ..models import User
from ..graphql import schema
import requests
from flask import (Blueprint, render_template, current_app, Response,
                   stream_with_context, jsonify, abort)

blueprint = Blueprint('views', __name__)


@blueprint.route('/')
def index():
    q = User.query.order_by(User.first_name, User.last_name)
    users = [{
        'userId': user.user_id,
        'fullName': '{} {}'.format(user.first_name, user.last_name),
        'avatarUrl': user.avatar_url,
    } for user in q.all()]
    return render_template('index.html', users=users)


@blueprint.route('/graphql/schema')
def schema_():
    if current_app.debug:
        return jsonify({
            'data': schema.introspect()
        })
    abort(404)


@blueprint.route('/lib/<path:filename>')
def lib(filename):
    """Proxy to frontend webpack server,
    else proxies `static/lib` in production."""
    if current_app.debug:
        url = '{endpoint}/lib/{filename}'.format(
            endpoint=current_app.config.get('DEV_FRONTEND_URI'),
            filename=filename)
        req = requests.get(url, stream=True)
        return Response(
            stream_with_context(req.iter_content(chunk_size=2048)),
            content_type=req.headers['content-type'])
    else:
        return current_app.send_static_file('lib/{}'.format(filename))
