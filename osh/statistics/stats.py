from flask import (
    Blueprint,
    render_template
)

from osh.statistics.utility.stats_utility import get_stats_per_month, get_total_stats

stats_bp = Blueprint('stats', __name__,
                     static_folder='static',
                     template_folder='templates'
                     )


@stats_bp.route('/', methods=['GET'])
def stats():
    stats_data = get_stats_per_month()

    return render_template('stats.html', **stats_data)


@stats_bp.route('/total_stats', methods=['GET'])
def total_stats():
    total_stats_data = get_total_stats()
    return render_template('total_stats.html', total_stats_data=total_stats_data)
