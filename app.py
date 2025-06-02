from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


def conectar_db():
    return sqlite3.connect('lista.db')

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresa (
        idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        setor TEXT,
        prioridade TEXT NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL,
        empresa_idUsuario INTEGER NOT NULL,
        FOREIGN KEY (empresa_idUsuario) REFERENCES empresa(idUsuario)
    )
    ''')

    conectar.commit()
    conectar.close()

@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tarefas.id, tarefas.descricao, tarefas.setor, tarefas.prioridade, tarefas.data, tarefas.status,
               empresa.nome, empresa.email
        FROM tarefas
        JOIN empresa ON tarefas.empresa_idUsuario = empresa.idUsuario
    """)
    tarefas = cursor.fetchall()

    cursor.execute("SELECT idUsuario, nome, email FROM empresa")
    usuarios = cursor.fetchall()

    conn.close()

    return render_template('index.html', tarefas=tarefas, usuarios=usuarios)

@app.route('/registrar_tarefa', methods=['POST'])
def adicionar_tarefa():
    descricao = request.form.get('descricao')
    setor = request.form.get('setor')
    prioridade = request.form.get('prioridade')
    data = request.form.get('data')
    status = request.form.get('status')
    empresa_id = request.form.get('empresa_id')

    if descricao and setor and prioridade and data and status and empresa_id:
        try:
            conectar = conectar_db()
            cursor = conectar.cursor()
            cursor.execute("""
                INSERT INTO tarefas (descricao, setor, prioridade, data, status, empresa_idUsuario)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (descricao, setor, prioridade, data, status, empresa_id))
            conectar.commit()
            conectar.close()
            flash('Tarefa adicionada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao cadastrar tarefa: {e}', 'error')
    else:
        flash('Por favor, preencha todos os campos.', 'error')

    return redirect(url_for('index'))
    
def alterar_tarefa(id_tarefa, descricao, setor, prioridade, data, status):
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute(
            "UPDATE tarefas SET descricao = ?, nome = ?, prioridade = ?, data = ?, status = ? WHERE id = ?",
            (descricao, setor, prioridade, data, status, id_tarefa)
        )

        conectar.commit()
        conectar.close()

        return "Tarefa atualizada com sucesso!"

    except Exception as e:
        return f"Erro ao atualizar a tarefa: {e}"

@app.route('/deletar_tarefa', methods=['DELETE'])
def excluir_tarefa():
    dados = request.get_json()
    id_tarefa = dados.get('id')

    if not id_tarefa:
        return jsonify({'mensagem': 'Erro: ID da tarefa não fornecido'}), 400

    try:
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        conectar.commit()
        conectar.close()
        return jsonify({'mensagem': 'Tarefa deletada com sucesso!'})
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao deletar tarefa: {e}'}), 500
    

@app.route('/cadastro_usuario', methods=['GET'])
def cadastro_usuario():
    return render_template('cadastro_usuario.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nome = request.form.get('nome')
    email = request.form.get('email')

    if nome and email:
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO empresa (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
            conn.close()
            flash('Usuário cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}', 'error')
    else:
        flash('Por favor, preencha todos os campos.', 'error')

    return redirect(url_for('index'))




@app.route('/editar_tarefa/<int:id>')
def editar_tarefa(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
    tarefa = cursor.fetchone()
    conn.close()
    return render_template("editar.html", tarefa=tarefa)

@app.route('/atualizar_tarefa', methods=['POST'])
def atualizar_tarefa():
    try:
        id_tarefa = request.form.get('id')
        descricao = request.form.get('descricao')
        setor = request.form.get('setor')
        prioridade = request.form.get('prioridade')
        data = request.form.get('data')
        status = request.form.get('status')

        if not all([id_tarefa, descricao, setor, prioridade, data, status]):
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('index'))

        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute(
            """
            UPDATE tarefas
            SET descricao = ?, setor = ?, prioridade = ?, data = ?, status = ?
            WHERE id = ?
            """,
            (descricao, setor, prioridade, data, status, id_tarefa)
        )
        
        conectar.commit()
        conectar.close()

        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Erro ao atualizar a tarefa: {str(e)}', 'error')
        return redirect(url_for('index'))

    finally:
        if 'conectar' in locals():
            conectar.close()




if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
    
