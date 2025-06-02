from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'


def conectar_db():
    return sqlite3.connect('crud.db')

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS carro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            vaga_id INTEGER,
            FOREIGN KEY (vaga_id) REFERENCES vaga(id)
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS vaga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'disponível',
            carro_id INTEGER,
            FOREIGN KEY (carro_id) REFERENCES carro(id)
        )
        '''
     )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carro_id INTEGER NOT NULL,
            vaga_id INTEGER NOT NULL,
            entrada DATETIME NOT NULL,
            saida DATETIME,
            FOREIGN KEY (carro_id) REFERENCES carro(id),
            FOREIGN KEY (vaga_id) REFERENCES vaga(id)
        )
        '''
    
    )
    conectar.commit()
    conectar.close()

@app.route('/')
def index():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM carro")
    carros = cursor.fetchall()
    conectar.close()
    return render_template('index.html', carros=carros, datetime=datetime)

@app.route('/registrar_carro', methods=['POST'])
def adicionar_carro():
    placa = request.form.get('placa')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = request.form.get('ano')

    if placa and marca and modelo and ano:
        try:
            ano = int(ano)
            ano_atual = datetime.now().year
            if not (1900 <= ano <= ano_atual):
                flash('Ano inválido! Digite um ano entre 1900 e o ano atual.', 'error')
                return redirect(url_for('index')) 

            conectar = conectar_db()
            cursor = conectar.cursor()
            cursor.execute("INSERT INTO carro (placa, marca, modelo, ano) VALUES (?, ?, ?, ?)",
                           (placa, marca, modelo, ano))
            conectar.commit()
            
            cursor.execute("SELECT * FROM carro")
            carros = cursor.fetchall()
            conectar.close()
            
            flash('Carro adicionado com sucesso!', 'success')
            return render_template('index.html', carros=carros, datetime=datetime)  
            
        except sqlite3.IntegrityError:
            flash('Erro: Placa já cadastrada!', 'error')
        except Exception as e:
            flash(f'Erro ao adicionar carro: {str(e)}', 'error')
    else:
        flash('Preencha todos os campos!', 'error')
        
    return redirect(url_for('index'))

@app.route('/exibir_carro', methods=['GET'])
def exibir_carro():
    conectar = conectar_db()
    cursor = conectar.cursor()

    cursor.execute("SELECT * FROM carro")
    carros = cursor.fetchall()  

    conectar.close()

    return render_template('index.html', carros=carros)

def deletar_carro(id_carro):
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute("DELETE FROM carro WHERE id = ?", (id_carro,))
        conectar.commit()  

        conectar.close()

        return "Carro excluído com sucesso!"

    except Exception as e:
        return f"Erro ao excluir carro: {e}"
    
def alterar_carro(id_carro, placa, marca, modelo, ano):

    try:
        conectar = conectar_db()
        cursor = conectar.cursor()

        cursor.execute(
            "UPDATE carro SET placa = ?, marca = ?, modelo = ?, ano = ? WHERE id = ?",
            (placa, marca, modelo, ano, id_carro)
        )

        conectar.commit()  

        conectar.close()

        return "Carro alterado com sucesso!"

    except Exception as e:
        return f"Erro ao alterar o carro: {e}"


@app.route('/deletar_carro', methods=['DELETE'])
def excluir():
    dados = request.get_json()
    id_carro = dados.get('id')  

    if not id_carro:
        return jsonify({'mensagem': 'Erro: ID do carro não fornecido'}), 400

    mensagem = deletar_carro(id_carro)
    return jsonify({'mensagem': mensagem})

@app.route('/atualizar_carro', methods=['POST'])
def atualizar_carro():
    try:
        id_carro = request.form.get('id')
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        ano = request.form.get('ano')

        if not all([id_carro, placa, marca, modelo, ano]):
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('index'))

        try:
            ano = int(ano)
            if ano < 1900 or ano > datetime.now().year:
                flash('Ano inválido!', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Ano deve ser um número válido!', 'error')
            return redirect(url_for('index'))

        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM carro WHERE placa = ? AND id != ?", (placa, id_carro))
        if cursor.fetchone():
            flash('Esta placa já está cadastrada em outro veículo!', 'error')
            return redirect(url_for('index'))

        cursor.execute(
            "UPDATE carro SET placa=?, marca=?, modelo=?, ano=? WHERE id=?",
            (placa, marca, modelo, ano, id_carro)
        )
        
        conn.commit()
        flash('Carro atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Erro durante atualização: {str(e)}")
        flash('Erro ao atualizar carro!', 'error')
        return redirect(url_for('index'))
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/gerenciar_vagas')
def gerenciar_vagas():
    conectar = conectar_db()
    cursor = conectar.cursor()
    
    cursor.execute("SELECT * FROM vaga")
    vagas = cursor.fetchall()
    
    cursor.execute("SELECT * FROM carro WHERE vaga_id IS NULL")
    carros_disponiveis = cursor.fetchall()
    cursor.execute("SELECT * FROM carro ")
    todos_carros = cursor.fetchall()
    
    conectar.close()
    
    return render_template('gerenciar_vagas.html', 
                         vagas=vagas, 
                         todos_carros=todos_carros,
                         carros_disponiveis= carros_disponiveis, 
                         datetime=datetime)


@app.route('/criar_vagas', methods=['POST'])
def criar_vagas():
    quantidade = request.form.get('quantidade', type=int)
    
    if quantidade and quantidade > 0:
        try:
            conectar = conectar_db()
            cursor = conectar.cursor()
            
            cursor.execute("SELECT MAX(numero) FROM vaga")
            max_numero = cursor.fetchone()[0] or 0
            
            for i in range(1, quantidade + 1):
                cursor.execute(
                    "INSERT INTO vaga (numero, status) VALUES (?, ?)",
                    (max_numero + i, 'disponível')
                )
            
            conectar.commit()
            flash(f'{quantidade} vagas criadas com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao criar vagas: {str(e)}', 'error')
        finally:
            conectar.close()
    else:
        flash('Quantidade inválida!', 'error')
    
    return redirect(url_for('gerenciar_vagas'))

@app.route('/reservar_vaga', methods=['POST'])
def reservar_vaga():
    vaga_id = request.form.get('vaga_id')
    carro_id = request.form.get('carro_id')
    
    if vaga_id and carro_id:
        try:
            conectar = conectar_db()
            cursor = conectar.cursor()
            
            cursor.execute("SELECT status FROM vaga WHERE id = ?", (vaga_id,))
            status = cursor.fetchone()[0]
            
            if status != 'disponível':
                flash('Vaga não está disponível para reserva!', 'error')
                return redirect(url_for('gerenciar_vagas'))
            
            cursor.execute(
                "UPDATE vaga SET status = 'reservada', carro_id = ? WHERE id = ?",
                (carro_id, vaga_id)
            )
            
            cursor.execute(
                "UPDATE carro SET vaga_id = ? WHERE id = ?",
                (vaga_id, carro_id)
            )
            
            conectar.commit()
            flash('Vaga reservada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao reservar vaga: {str(e)}', 'error')
        finally:
            conectar.close()
    else:
        flash('Dados incompletos para reserva!', 'error')
    
    return redirect(url_for('gerenciar_vagas'))

@app.route('/registrar_entrada', methods=['POST'])
def registrar_entrada():
    placa = request.form.get('placa')
    
    if placa:
        try:
            conectar = conectar_db()
            cursor = conectar.cursor()
            
            cursor.execute("SELECT id, vaga_id FROM carro WHERE placa = ?", (placa,))
            carro = cursor.fetchone()
            
            if not carro:
                flash('Carro não encontrado!', 'error')
                return redirect(url_for('gerenciar_vagas'))
            
            carro_id, vaga_id = carro
            
            if vaga_id:
                cursor.execute("SELECT status FROM vaga WHERE id = ?", (vaga_id,))
                status = cursor.fetchone()[0]
                
                if status == 'ocupada':
                    flash('Carro já está estacionado!', 'error')
                    return redirect(url_for('gerenciar_vagas'))
            
                cursor.execute(
                    "UPDATE vaga SET status = 'ocupada' WHERE id = ?",
                    (vaga_id,)
                )
            else:
                cursor.execute(
                    "SELECT id FROM vaga WHERE status = 'disponível' LIMIT 1"
                )
                vaga = cursor.fetchone()
                
                if not vaga:
                    flash('Não há vagas disponíveis!', 'error')
                    return redirect(url_for('gerenciar_vagas'))
                
                vaga_id = vaga[0]
                
                cursor.execute(
                    "UPDATE vaga SET status = 'ocupada', carro_id = ? WHERE id = ?",
                    (carro_id, vaga_id)
                )
                cursor.execute(
                    "UPDATE carro SET vaga_id = ? WHERE id = ?",
                    (vaga_id, carro_id)
                )
            
            cursor.execute(
                "INSERT INTO historico (carro_id, vaga_id, entrada) VALUES (?, ?, ?)",
                (carro_id, vaga_id, datetime.now())
            )
            
            conectar.commit()
            flash('Entrada registrada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao registrar entrada: {str(e)}', 'error')
        finally:
            conectar.close()
    else:
        flash('Placa não informada!', 'error')
    
    return redirect(url_for('gerenciar_vagas'))

@app.route('/registrar_saida', methods=['POST'])
def registrar_saida():
    placa = request.form.get('placa')
    
    if not placa:
        flash('Placa não informada!', 'error')
        return redirect(url_for('gerenciar_vagas'))

    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT carro.id, carro.vaga_id 
            FROM carro 
            WHERE placa = ? AND vaga_id IS NOT NULL
        """, (placa,))
        carro = cursor.fetchone()
        
        if not carro:
            flash('Carro não encontrado ou não está estacionado!', 'error')
            return redirect(url_for('gerenciar_vagas'))
        
        carro_id, vaga_id = carro
        
        cursor.execute("""
            UPDATE vaga 
            SET status = 'disponível', carro_id = NULL 
            WHERE id = ? AND carro_id = ?
        """, (vaga_id, carro_id))
        
        cursor.execute("""
            UPDATE carro 
            SET vaga_id = NULL 
            WHERE id = ?
        """, (carro_id,))
        
        cursor.execute("""
            UPDATE historico 
            SET saida = datetime('now') 
            WHERE carro_id = ? AND vaga_id = ? AND saida IS NULL
        """, (carro_id, vaga_id))
        
        conn.commit()
        flash('Saída registrada com sucesso!', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Erro ao registrar saída: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('gerenciar_vagas'))

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/relatorio_entradas_saidas')
def relatorio_entradas_saidas():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()
        
        query = """
            SELECT h.entrada, h.saida, c.placa, c.marca, c.modelo, v.numero
            FROM historico h
            JOIN carro c ON h.carro_id = c.id
            JOIN vaga v ON h.vaga_id = v.id
        """
        
        params = []
        
        if data_inicio and data_fim:
            query += " WHERE h.entrada BETWEEN ? AND ?"
            params.extend([data_inicio, data_fim])
        
        query += " ORDER BY h.entrada DESC"
        
        cursor.execute(query, params)
        registros = cursor.fetchall()
        
        return render_template('relatorio_entradas_saidas.html', 
                            registros=registros,
                            data_inicio=data_inicio,
                            data_fim=data_fim)
    
    except Exception as e:
        flash(f'Erro ao gerar relatório: {str(e)}', 'error')
        return redirect(url_for('relatorios'))
    finally:
        conectar.close()

@app.route('/relatorio_ocupacao')
def relatorio_ocupacao():
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM vaga")
        total_vagas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vaga WHERE status = 'ocupada'")
        ocupadas = cursor.fetchone()[0]
       
        cursor.execute("SELECT COUNT(*) FROM vaga WHERE status = 'reservada'")
        reservadas = cursor.fetchone()[0]
        
        disponiveis = total_vagas - ocupadas - reservadas
        
        cursor.execute("""
            SELECT AVG(JULIANDAY(saida) - JULIANDAY(entrada)) * 24 
            FROM historico 
            WHERE saida IS NOT NULL
        """)
        tempo_medio_horas = cursor.fetchone()[0] or 0
        
        return render_template('relatorio_ocupacao.html',
                            total_vagas=total_vagas,
                            ocupadas=ocupadas,
                            reservadas=reservadas,
                            disponiveis=disponiveis,
                            tempo_medio_horas=round(tempo_medio_horas, 2))
    
    except Exception as e:
        flash(f'Erro ao gerar relatório: {str(e)}', 'error')
        return redirect(url_for('relatorios'))
    finally:
        conectar.close()


if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
    
