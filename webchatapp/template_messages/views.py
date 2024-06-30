# template_messages/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from webchatapp import db
from webchatapp.models import Template
from webchatapp.template_messages.forms import AddTemplateForm


templates = Blueprint('templates', __name__) # and passing the buildin name variable __name__

@templates.route('/view_templates/add_template', methods=['GET','POST'])
def add_template():
    form = AddTemplateForm()

    if form.validate_on_submit():
        template = Template(template_name=form.template_name.data,
                      template_message=form.template_message.data,
                      )
        
        db.session.add(template)
        db.session.commit()
        flash('Template added successfully')
        return redirect(url_for('templates.view_templates'))
    return render_template('add_template.html', form=form)

# this code will be modified later to edit the templates

# @agents.route('/edit_agent/<int:agent_id>', methods=['GET', 'POST'])
# @login_required
# def edit_agent(agent_id):
#     agent = Agent.query.get_or_404(agent_id)
#     form = EditAgentForm(agent_id=agent_id)

#     if form.validate_on_submit():
#         agent.name = form.name.data
#         agent.email = form.email.data
#         agent.agent_type = form.agent_type.data
#         if form.password.data:
#             agent.password = form.password.data
#         db.session.commit()
#         flash('Agent details have been updated!', 'success')
#         return redirect(url_for('agents.view_agents'))

#     elif request.method == 'GET':
#         form.name.data = agent.name
#         form.email.data = agent.email
#         form.agent_type.data = agent.agent_type

#     return render_template('edit_agent.html', form=form, agent=agent)


# @templates.route('/view_templates')
# def view_templates():
#     templates = Template.query.all()  # Query all templates from the database
#     return render_template('template.html', templates=templates)

@templates.route('/view_templates')
@templates.route('/view_templates/<int:page>')
def view_templates(page=1):
    # page = request.args.get('page', 1, type=int)  # Get the page parameter from the query string, default to 1
    per_page = 7  # Number of items per page
    templates = Template.query.paginate(page=page, per_page=per_page, error_out=False)  # Paginate the query results
    return render_template('template.html', templates=templates)


@templates.route('/delete_template/<int:template_id>', methods=['POST'])
@login_required
def delete_template(template_id):
    template = Template.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    flash('Template has been deleted!', 'success')
    return redirect(url_for('templates.view_templates'))


