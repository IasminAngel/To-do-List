# Gerenciamento de Estacionamento - Flask

## Descrição
Este projeto é um sistema de gerenciamento de estacionamento desenvolvido em Flask e SQLite. Ele permite cadastrar carros, criar e gerenciar vagas, registrar entradas e saídas de veículos e manter um histórico de movimentações.

## Tecnologias Utilizadas
- Python 3
- Flask
- SQLite3
- HTML/CSS (para templates)
- Bootstrap (para estilização)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script para criar o banco de dados:
   ```bash
   python -c "from app import criar_tabela; criar_tabela()"
   ```

## Como Usar

1. Inicie o servidor Flask:
   ```bash
   python app.py
   ```
2. Acesse no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Rotas Disponíveis

- `/` - Página inicial com a listagem de carros.
- `/registrar_carro` - Rota para adicionar um novo carro.
- `/exibir_carro` - Exibe os carros cadastrados.
- `/deletar_carro` - Exclui um carro pelo ID.
- `/atualizar_carro` - Atualiza os dados de um carro.
- `/gerenciar_vagas` - Permite visualizar as vagas do estacionamento.
- `/criar_vagas` - Adiciona novas vagas.
- `/reservar_vaga` - Reserva uma vaga para um carro.
- `/registrar_entrada` - Registra a entrada de um carro.
- `/registrar_saida` - Registra a saída de um carro e libera a vaga.
- `/historico_movimentacoes` - Exibe o histórico de movimentações do estacionamento.

## Estrutura do Banco de Dados

- **Carro**: id, placa, marca, modelo, ano, vaga_id.
- **Vaga**: id, número, status, carro_id.
- **Histórico**: id, carro_id, vaga_id, entrada, saída.
- **Usuário**: id, nome, email, senha (para autenticação futura).

## Melhorias Futuras
- Interface mais amigável com Bootstrap.
- Dashboard com gráficos de ocupação do estacionamento.
- Autenticação de usuários.
- Sistema de notificações para alertar sobre tempo de permanência excedido.

## Contribuição
Pull requests são bem-vindos! Para discussões maiores, abra uma issue primeiro para discutir as mudanças desejadas.

Copyright [2025] [Iasmin Angel]

Todos os direitos reservados. Este software é propriedade exclusiva do autor. Nenhuma parte deste código pode ser copiada, modificada, distribuída ou utilizada sem permissão expressa do autor.


