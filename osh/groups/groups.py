from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from osh.groups.utility.groups_utility import (
    create_new_group,
    get_current_day,
    get_group_data,
    get_group_and_students,
    update_group_status_toggle,
    delete_group_by_id,
    clear_all_data_from_db,
    inject_groups_utility
)

groups_bp = Blueprint('groups', __name__,
                      static_folder='static',
                      template_folder='templates'
                      )


@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = create_new_group(request)
        if group_name:
            return redirect(url_for('groups.list_groups'))

    current_day = get_current_day()

    return render_template('group_create.html', current_day=current_day)


@groups_bp.route('/', methods=['GET'])
def list_groups():
    group_data = get_group_data(request)

    return render_template('group_list.html', **group_data)


@groups_bp.route('/<int:group_id>/', methods=['GET'])
def view_group(group_id):
    group, students = get_group_and_students(group_id)

    return render_template('group_view.html',
                           group=group,
                           students=students,
                           group_id=group_id)


@groups_bp.route('/<int:group_id>/update_status', methods=['POST'])
def update_group_status(group_id):
    update_group_status_toggle(group_id)

    return redirect(url_for('groups.view_group', group_id=group_id))


@groups_bp.route('/<int:group_id>/delete', methods=['POST'])
def delete_group(group_id):
    delete_group_by_id(group_id)

    return redirect(url_for('groups.list_groups'))


@groups_bp.route('/clear_database', methods=['POST'])
def clear_all_data():
    clear_all_data_from_db()

    return redirect(url_for('groups.list_groups'))


@groups_bp.context_processor
def inject_groups():
    return inject_groups_utility()
