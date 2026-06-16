# 1 - [ESTRUTURA DE DADOS]

Clientes = []
Proximo_id_Cliente = 1

# 2 - [FUNÇÕES AUXILIARES DE VALIDAÇÃO]

def obter_string(prompt):
  while True:
    entrada = input(prompt).strip()
    if entrada:
      return entrada.title()
    print("\033[1;31mErro: O campo não pode ser vazio.\033[0m")

def obter_float(prompt):
    while True:
      entrada = input(prompt).strip().replace(',','.')
      if not entrada:
        print('\033[1;31mErro: O Campo não pode ser vazio.\033[0m')
        continue
      try:
        valor = float(entrada)
        if valor >= 0:
          return valor
        print("\033[1;31mErro: O valor deve ser positivo.\033[0m")
      except ValueError:
        print("\033[1;31mErro:Digite um número decimal válido (ex: 75.50).\033[0m")

def obter_cpf(prompt):
  while True:
    cpf = input(prompt).strip()
    if not cpf:
      print("\033[1;31mErro: O campo não pode ser vazio.\033[0m")
      continue

    cpf_limpo = cpf.replace('.','').replace('-','')

    if len(cpf_limpo) == 11 and cpf_limpo.isdigit():
      return cpf_limpo

    print("\033[1;31mErro: CPF inválido. Certifique-se de que tem 11 dígitos.\033[0m")

def encontrar_cliente(identificador):
  if isinstance(identificador, int):
    for cliente in Clientes:
      if cliente['id'] == identificador:
        return cliente

  elif isinstance(identificador, str):
    for cliente in Clientes:
      if cliente['cpf'] == identificador:
        return cliente
  return None

#3 - [FUNÇÕES PRINCIPAIS DO SISTEMA]

def menu():
  print("\n" + "\033[35m=\033[0m"*23)
  print("\033[35;44m Menu Salão de Beleza\033[0m")
  print("\033[35m=\033[0m"*23)
  print("\033[34m1 - Cadastrar Cliente")
  print("2 - Listar Clientes")
  print("3 - Buscar Clientes")
  print("4 - Registrar Agendamento (Atualizar)")
  print("5 - Remover Cliente")
  print("6 - Estatísticas e Relatórios")
  print("0 - Sair\033[0m")
  print("\033[35m-\033[0m" * 23)

  while True:
        escolha = input(" Escolha uma opção: ").strip()
        if escolha.isdigit():
            opcao = int(escolha)
            if 0 <= opcao <= 6:
                return opcao
            else:
                print("\033[31m Opção inválida. Escolha um número entre 0 e 6.\033[0m")
        else:
            print("\033[31m Entrada inválida. Digite o número da opção.\033[0m")

def cadastrar():
    global Proximo_id_Cliente, Clientes
    print("\n--- CADASTRO DE NOVO CLIENTE ---")

    nome = obter_string("Nome do Cliente: ")

    cpf = obter_cpf("CPF (somente números): ")

    if encontrar_cliente(cpf):
        print(f"\033[1.31m Erro: Um cliente com o CPF '{cpf}' já está cadastrado.\033[0m")
        return

    novo_cliente = {
        "id": Proximo_id_Cliente,
        "nome": nome,
        "cpf": cpf,
        "telefone": input("Telefone (opcional): ").strip(),
        "agendamentos": []
    }

    Clientes.append(novo_cliente)
    Proximo_id_Cliente += 1
    print(f"\n \033[34mSucesso! Cliente '{nome}' cadastrado com o ID {novo_cliente['id']}.\033[0m")

def listar():
    if not Clientes:
        print("\n A lista de clientes está vazia.")
        return

    print("\033[7;34m\n---  LISTA DE CLIENTES E HISTÓRICO ---\033[0m")
    clientes_ordenados = sorted(Clientes, key=lambda c: c['nome'])
    print("\033[34mID | NOME (Cliente)      | CPF           | TEL   | TOTAL GASTO | Qtd. AGENDAMENTOS\033[0m")
    print("-" * 80)
    or clientef in clientes_ordenados:
        total_gasto = sum(a['valor'] for a in cliente['agendamentos'])
        qtd_agendamentos = len(cliente['agendamentos'])

        print(f"{cliente['id']:<2} | {cliente['nome']:<18} | {cliente['cpf']:<11} | {cliente['telefone'][:8]:<5} | R$ {total_gasto:<10.2f} | {qtd_agendamentos}")
    print("-" * 80)
    print(f"\033[34mTotal de Clientes: {len(Clientes)}\033[0m")

def buscar():
    if not Clientes:
        print("\n A lista de clientes está vazia.")
        return

    termo = obter_string("\n Digite o Nome ou CPF para buscar:").lower()

    resultados = []
    for c in Clientes:
        if termo in c['nome'].lower() or termo in c['cpf']:
            resultados.append(c)

    if resultados:
        print(f"\n {len(resultados)} cliente(s) encontrado(s) para '{termo}':")
        for cliente in resultados:
            print("\n" + "~" * 40)
            print(f"\033[34mID: {cliente['id']} | Nome: {cliente['nome']} | CPF: {cliente['cpf']}\033[0m")
            print(f"\033[34mTelefone: {cliente['telefone']}\033[0m")
            print("-" * 40)
            print(f"\033[34mHISTÓRICO DE AGENDAMENTOS ({len(cliente['agendamentos'])}):\033[0m")
            if cliente['agendamentos']:
                for i, agendamento in enumerate(cliente['agendamentos'], 1):
                    print(f"  {i}. {agendamento['data']} às {agendamento['hora']} - {agendamento['servico']} | R$ {agendamento['valor']:.2f}")
            else:
                print("  Nenhum agendamento registrado.")
        print("~" * 40)
    else:
        print(f"\nNenhum cliente encontrado com o termo '{termo}'.")

def atualizar():
    if not Clientes:
        print("\nA lista de clientes está vazia. Cadastre um cliente primeiro.")
        return

    print("\n--- REGISTRAR NOVO AGENDAMENTO ---")

    id_busca = obter_inteiro("Digite o ID do cliente para agendar: ")

    cliente = encontrar_cliente(id_busca)

    if not cliente:
        print(f"\033[31m Erro: Cliente com ID {id_busca} não encontrado.\033[0m")
        return

    print(f"\n Cliente Selecionado:\033[34m ID {cliente['id']} - {cliente['nome']}\033[0m")

    data = input("Data do Serviço (DD/MM/AAAA):").strip()
    hora = input("Hora do Serviço (HH:MM):").strip()
    servico = obter_string("Tipo de Serviço (Ex: Corte, Manicure, Coloração):")
    valor = obter_float("Valor do Serviço: R$ ")

    novo_agendamento = {
        "data": data,
        "hora": hora,
        "servico": servico,
        "valor": valor
    }

    cliente['agendamentos'].append(novo_agendamento)

    print(f"\n\033[32m Sucesso! Novo agendamento de '{servico}' registrado para {cliente['nome']}.\033[0m")

def remover():
    global Clientes
    if not Clientes:
        print("\nA lista de clientes está vazia. Nada para remover.")
        return

    print("\n--- REMOVER CLIENTE ---")

    id_remover = obter_inteiro("Digite o ID do cliente para remover: ")

    cliente_a_remover = encontrar_cliente(id_remover)

    if cliente_a_remover:
        confirmacao = input(f"ATENÇÃO: Confirma a remoção de {cliente_a_remover['nome']} e todo seu histórico? (S/N): ").lower()
        if confirmacao == 's':
            Clientes = [c for c in Clientes if c['id'] != id_remover]
            print(f"\033[32m\nSucesso! Cliente ID {id_remover} removido.\033[0m")
        else:
            print("\nRemoção cancelada pelo usuário.")
    else:
        print(f"\033[31m\n Erro: Cliente com ID {id_remover} não encontrado.\033[0m")

def estatisticas():
    if not Clientes:
        print("\nA lista de clientes está vazia. Nenhuma estatística para exibir.")
        return

    print("\n--- ESTATÍSTICAS DO SALÃO ---")

    total_clientes = len(Clientes)
    total_agendamentos = sum(len(c['agendamentos']) for c in Clientes)

    todos_valores = []
    for c in Clientes:
        for a in c['agendamentos']:
            todos_valores.append(a['valor'])

    clientes_gastos = [
        {"nome": c['nome'], "gasto": sum(a['valor'] for a in c['agendamentos']), "qtd": len(c['agendamentos'])}
        for c in Clientes
    ]

    print(f"Total de Clientes Cadastrados: {total_clientes}")
    print(f"Total de Agendamentos Registrados: {total_agendamentos}")

    if total_agendamentos > 0:
        total_faturamento = sum(todos_valores)
        media_servico = sum(todos_valores) / total_agendamentos

        cliente_mais_gastou = max(clientes_gastos, key=lambda x: x['gasto'])
        cliente_mais_agendou = max(clientes_gastos, key=lambda x: x['qtd'])

        print("\n--- DESTAQUES DOS CLIENTES ---")
        print(f"Cliente que mais Gastou: {cliente_mais_gastou['nome']} (R$ {cliente_mais_gastou['gasto']:,.2f})")
        print(f"Cliente que mais Agendou: {cliente_mais_agendou['nome']} ({cliente_mais_agendou['qtd']} serviços)")
    else:
        print("\n Nenhum agendamento foi registrado ainda.")

def obter_inteiro(prompt):
    while True:
        entrada = input(prompt).strip()
        if not entrada:
            print("\033[31m Erro: O campo não pode ser vazio.\033[0m")
            continue
        try:
            valor = int(entrada)
            if valor >= 0:
                return valor
            print("\033[31m Erro: O valor deve ser um número inteiro não negativo.\033[0m")
        except ValueError:
            print("\033[31m Erro: Digite um número inteiro válido.\033[0m")

#4 - [FUNÇÃO PRINCIPAL]

def main():
    print("\033[34m Iniciando Sistema Salão de Beleza (Cadastro e Agendamento)\033[0m")

    global Clientes, Proximo_id_Cliente
    Clientes.append({
        "id": 1,
        "nome": "Carla Oliveira",
        "cpf": "11122233344",
        "telefone": "987654321",
        "agendamentos": [
            {"data": "01/11/2025", "hora": "10:00", "servico": "Corte Feminino", "valor": 80.00},
            {"data": "05/11/2025", "hora": "14:30", "servico": "Manicure e Pedicure", "valor": 55.00}
        ]
    })
    Clientes.append({
        "id": 2,
        "nome": "Bruna Lima",
        "cpf": "55566677788",
        "telefone": "912345678",
        "agendamentos": [
            {"data": "02/11/2025", "hora": "16:00", "servico": "Coloração", "valor": 250.00}
        ]
    })
    Proximo_id_Cliente = 3

    while True:
        opcao = menu()

        if opcao == 1:
            cadastrar()
        elif opcao == 2:
            listar()
        elif opcao == 3:
            buscar()
        elif opcao == 4:
            atualizar()
        elif opcao == 5:
            remover()
        elif opcao == 6:
            estatisticas()
        elif opcao == 0:
            print("\n Encerrando o sistema do Salão de Beleza. Volte sempre!")
            break
        else:
            print("\033[31m Erro de execução: Opção desconhecida.\033[0m")

if __name__ == "__main__":
    main()
