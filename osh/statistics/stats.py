from flask import (
    Blueprint,
    render_template
)

from osh.statistics.stats_utility import prepare_stats_data

stats_bp = Blueprint('stats', __name__,
                     static_folder='static',
                     template_folder='templates'
                     )


@stats_bp.route('/', methods=['GET'])
def stats():
    stats_data = prepare_stats_data()

    return render_template('stats.html', **stats_data)
