from CRUD_clientes import CrudCliente
from CRUD_produtos import CrudProduto
from CRUD_vendas import CrudVendas

def menu_principal():
    print("\n===== SISTEMA DO BAR =====")
    print("1. Gerenciar clientes")
    print("2. Gerenciar produtos")
    print("3. Gerenciar vendas")
    print("0. Sair")

def menu_clientes():
    crud = CrudCliente()
    while True:
        print("\n --CLIENTES-- ")
        print("1. Inserir cliente")
        print("2. Alterar cliente")
        print("3. Pesquisar cliente por nome")
        print("4. Remover cliente")
        print("5. Listar todos os clientes")
        print("6. Exibir um cliente pelo ID")
        print("7. Gerar relatório de clientes")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            idade = int(input("Idade: "))
            crud.inserir(nome, telefone, email, idade)
        elif opcao == "2":
            id_cliente = int(input("ID do cliente a alterar: "))
            nome = input("Novo nome: ")
            telefone = input("Novo telefone: ")
            email = input("Novo email: ")
            idade = int(input("Nova idade: "))
            crud.alterar(id_cliente, nome, telefone, email, idade)
        elif opcao == "3":
            nome = input("Nome do cliente a pesquisar: ")
            crud.pesquisar_por_nome(nome)
        elif opcao == "4":
            id_cliente = int(input("ID do cliente a remover: "))
            crud.remover(id_cliente)
        elif opcao == "5":
            crud.listar_todos()
        elif opcao == "6":
            id_cliente = int(input("ID do cliente a exibir: "))
            crud.exibir_um(id_cliente)
        elif opcao == "7":
            crud.relatorio()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_produtos():
    crud = CrudProduto()
    while True:
        print("\n --PRODUTOS-- ")
        print("1. Inserir produto")
        print("2. Alterar produto")
        print("3. Pesquisar produto por nome")
        print("4. Remover produto")
        print("5. Listar todos os produtos")
        print("6. Exibir um produto pelo ID")
        print("7. Gerar relatório de produtos")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))
            crud.inserir(nome, preco, quantidade)
        elif opcao == "2":
            id_produto = int(input("ID do produto a alterar: "))
            nome = input("Novo nome do produto: ")
            preco = float(input("Novo preço: "))
            quantidade = int(input("Nova quantidade: "))
            crud.alterar(id_produto, nome, preco, quantidade)
        elif opcao == "3":
            nome = input("Nome do produto a pesquisar: ")
            crud.pesquisar_por_nome(nome)
        elif opcao == "4":
            id_produto = int(input("ID do produto a remover: "))
            crud.remover(id_produto)
        elif opcao == "5":
            crud.listar_todos()
        elif opcao == "6":
            id_produto = int(input("ID do produto a exibir: "))
            crud.exibir_um(id_produto)
        elif opcao == "7":
            crud.relatorio()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_vendas():
    crud = CrudVendas()
    while True:
        print("\n --VENDAS-- ")
        print("1. Registrar venda")
        print("2. Alterar venda")
        print("3. Pesquisar vendas por cliente")
        print("4. Remover venda")
        print("5. Listar todas as vendas")
        print("6. Exibir uma venda pelo ID")
        print("7. Gerar relatório de vendas")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente_id = int(input("ID do cliente: "))
            produto_id = int(input("ID do produto: "))
            quantidade = int(input("Quantidade: "))
            crud.registrar_venda(cliente_id, produto_id, quantidade)
        elif opcao == "2":
            id_venda = int(input("ID da venda a alterar: "))
            cliente_id = int(input("Novo ID do cliente: "))
            produto_id = int(input("Novo ID do produto: "))
            quantidade = int(input("Nova quantidade: "))
            crud.alterar(id_venda, cliente_id, produto_id, quantidade)
        elif opcao == "3":
            cliente_id = int(input("ID do cliente: "))
            crud.pesquisar_por_cliente(cliente_id)
        elif opcao == "4":
            id_venda = int(input("ID da venda a remover: "))
            crud.remover(id_venda)
        elif opcao == "5":
            crud.listar_todos()
        elif opcao == "6":
            id_venda = int(input("ID da venda a exibir: "))
            crud.exibir_um(id_venda)
        elif opcao == "7":
            crud.relatorio()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_vendas()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
