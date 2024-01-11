from flask import (
    Blueprint,
    render_template,
    # request,
    # redirect,
    # url_for,
    # abort
)

stats_bp = Blueprint('stats', __name__,
                     static_folder='static',
                     template_folder='templates'
                     )


@stats_bp.route('/', methods=['GET'])
def view_stats():
    return render_template('stats.html')
