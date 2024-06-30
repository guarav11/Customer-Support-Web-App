# agents/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from webchatapp import db
from webchatapp.models import Agent
from webchatapp.agents.forms import AddAgentForm, EditAgentForm


agents = Blueprint('agents', __name__) # and passing the buildin name variable __name__

@agents.route('/add_agent', methods=['GET','POST'])
def add_agent():
    form = AddAgentForm()

    if form.validate_on_submit():
        agent = Agent(name=form.name.data,
                      email=form.email.data,
                      password=form.password.data,
                      agent_type=form.agent_type.data)
        
        db.session.add(agent)
        db.session.commit()
        flash('Thanks for registering the Agent')
        return redirect(url_for('agents.view_agents'))
    return render_template('add_agent.html', form=form)


@agents.route('/edit_agent/<int:agent_id>', methods=['GET', 'POST'])
@login_required
def edit_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    form = EditAgentForm(agent_id=agent_id)

    if form.validate_on_submit():
        agent.name = form.name.data
        agent.email = form.email.data
        agent.agent_type = form.agent_type.data
        if form.password.data:
            agent.password = form.password.data
        db.session.commit()
        flash('Agent details have been updated!', 'success')
        return redirect(url_for('agents.view_agents'))

    elif request.method == 'GET':
        form.name.data = agent.name
        form.email.data = agent.email
        form.agent_type.data = agent.agent_type

    return render_template('edit_agent.html', form=form, agent=agent)


@agents.route('/view_agents')
def view_agents():
    agents = Agent.query.all()  # Query all agents from the database
    return render_template('view_agents.html', agents=agents)


@agents.route('/delete_agent/<int:agent_id>', methods=['POST'])
@login_required
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    flash('Agent has been deleted!', 'success')
    return redirect(url_for('agents.view_agents'))


#   this method will be used later to agent login purposes
        
# @agents.route('/', methods=['GET','POST'])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():

#         user = User.query.filter_by(email=form.email.data).first()
#         if user.check_password(form.password.data) and user is not None:
            
#             login_user(user)
#             flash('Login successful')

#             # next = request.args.get('next')  # if user click on other link for which login is necessary
#             # if next == None or not next[0]=='/':
#             #     next = url_for('users.base_dashboard')   # going back to th home page

#             return render_template('chats.html')
        
#     return render_template('login.html', form=form)