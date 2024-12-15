from models import Cliente, handler
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def list_clientes():
    clientes = handler.session.query(Cliente).all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/add-cliente/', methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        horario = request.form.get('horario')
        
        # Obtém os serviços selecionados como uma lista de valores
        servicos = request.form.getlist('servicos')

        # Valida se pelo menos um serviço foi selecionado
        if not servicos:
            error = "Por favor, selecione pelo menos um serviço."
            return render_template(
                'add-cliente.html', 
                error=error, 
                nome=nome, 
                email=email, 
                telefone=telefone, 
                horario=horario, 
                selected_servicos=servicos
            )
        
        # Converte a lista de serviços selecionados em uma string para armazenar no banco de dados
        servicos_str = ", ".join(servicos)
        
        cliente = Cliente(
            nome=nome,
            email=email,
            telefone=telefone,
            horario=horario,
            servicos=servicos_str
        )

        try:
            handler.session.add(cliente)
            handler.session.commit()
        except Exception as e:
            handler.session.rollback()
            print(f"Erro ao adicionar cliente: {e}")
            error = "Ocorreu um erro ao cadastrar o cliente."
            return render_template('add-cliente.html', error=error)

        return redirect(url_for('clientes'))
    
    return render_template('add-cliente.html')

@app.route('/deletar-cliente/<id>')
def deletar_cliente(id: int):
    cliente = handler.session.query(Cliente).filter(Cliente.id == id).one_or_none()
    handler.session.delete(cliente)
    handler.session.commit()
    return redirect(url_for('clientes'))


@app.route('/atualizar-cliente/<id>', methods=['GET', 'POST'])
def update_cliente(id: int):
    cliente = handler.session.query(Cliente).filter(Cliente.id == id).one_or_none()
    if not cliente:
        return redirect(url_for('clientes'))

    if request.method == 'POST':
        # Dados recebidos do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        horario = request.form.get('horario')
        
        # Obter lista de serviços selecionados
        servicos = request.form.getlist('servicos')

        # Validação: pelo menos um serviço deve ser selecionado
        if not servicos:
            error = "Por favor, selecione pelo menos um serviço."
            return render_template(
                'update-cliente.html', 
                cliente=cliente, 
                error=error, 
                selected_servicos=servicos
            )
        
        # Converte lista de serviços para string
        servicos_str = ", ".join(servicos)

        # Atualiza os campos do cliente
        cliente.nome = nome
        cliente.email = email
        cliente.telefone = telefone
        cliente.horario = horario
        cliente.servicos = servicos_str

        try:
            handler.session.commit()
        except Exception as e:
            handler.session.rollback()
            print(f"Erro ao atualizar cliente: {e}")
            error = "Ocorreu um erro ao atualizar o cliente."
            return render_template('update-cliente.html', cliente=cliente, error=error)

        return redirect(url_for('clientes'))
    
    # Formatação do template para exibir serviços já selecionados
    selected_servicos = cliente.servicos.split(", ") if cliente.servicos else []
    return render_template('update-cliente.html', cliente=cliente, selected_servicos=selected_servicos)


if __name__ == '__main__':
    app.run(debug=True)

