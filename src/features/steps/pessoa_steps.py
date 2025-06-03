from behave import given, when, then
from contextlib import contextmanager

from app import app
from flask import template_rendered, appcontext_pushed
from database import db
from models.pessoa import Pessoa

@given('I have a client and a CPF "{cpf}"')
def step_impl(context, cpf):
    context.client = app.test_client()
    context.cpf = cpf

@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@when('I try to register this CPF')
def step_impl(context):
    with captured_templates(app) as templates:
        response = context.client.post('/cadastrar', data={
            'nome': 'Test',
            'sobrenome': 'User',
            'cpf': context.cpf,
            'data_nascimento': '2000-10-10'
        }, follow_redirects=True)
        context.response = response
        context.templates = templates

@then('I should receive a success message')
def step_impl(context):
    template, template_context = context.templates[-1]
    assert 'Pessoa cadastrada com sucesso!' in template_context.get('message', '') or 'Pessoa cadastrada com sucesso!' in context.response.get_data(as_text=True)

@then('I should receive an error message')
def step_impl(context):
    text = context.response.get_data(as_text=True)
    print(text)  # veja o conteúdo para ajustar o assert
    assert 'Erro ao cadastrar' in text or 'já existe' in text or 'já cadastrado' in text

@given('I have a registered person with CPF "{cpf}"')
def step_impl(context, cpf):
    context.client = app.test_client()
    with app.app_context():
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()
        if not pessoa:
            pessoa = Pessoa(
                nome='Test',
                sobrenome='User',
                cpf=cpf,
                data_de_nascimento='2000-01-01'
            )
            db.session.add(pessoa)
            db.session.commit()
        context.pessoa_id = pessoa.id
        context.cpf = cpf

@when('I visit the list page')
def step_impl(context):
    context.response = context.client.get('/listar')

@then('I should see the person with CPF "{cpf}"')
def step_impl(context, cpf):
    assert cpf in context.response.get_data(as_text=True)

@when('I edit the person\'s name to "{new_name}"')
def step_impl(context, new_name):
    context.response = context.client.post(f'/editar/{context.pessoa_id}', data={
        'nome': new_name,
        'sobrenome': 'Edited',
        'cpf': context.cpf,
        'data_nascimento': '1999-12-31'
    }, follow_redirects=True)

@then('I should see the person with name "{name}"')
def step_impl(context, name):
    text = context.response.get_data(as_text=True)
    assert name in text

@when('I remove the person')
def step_impl(context):
    context.response = context.client.get(f'/remover/{context.pessoa_id}', follow_redirects=True)

@then('I should not see the person with CPF "{cpf}"')
def step_impl(context, cpf):
    assert cpf not in context.response.get_data(as_text=True)
