from CRUD_clientes import CrudCliente
from CRUD_produtos import CrudProduto
from crud_compra import CrudCompra
from CRUD_vendedor import CrudVendedor


def menu_principal():
    print("\n===== SISTEMA DO BAR =====")
    print("1. Gerenciar clientes")
    print("2. Gerenciar produtos")
    print("3. Gerenciar vendedores")
    print("4. Gerenciar compras")
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
        print("6. Exibir cliente pelo ID")
        print("7. Relatório de clientes")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            idade = int(input("Idade: "))
            cidade = input("Cidade: ")
            torce = input("Torce Flamengo? (s/n): ").lower() == "s"
            assiste = input("Assiste One Piece? (s/n): ").lower() == "s"
            crud.inserir(nome, telefone, email, idade, cidade, torce, assiste)
        elif opcao == "2":
            id_cliente = int(input("ID do cliente: "))
            nome = input("Novo nome: ")
            telefone = input("Novo telefone: ")
            email = input("Novo email: ")
            idade = int(input("Nova idade: "))
            cidade = input("Nova cidade: ")
            torce = input("Torce Flamengo? (s/n): ").lower() == "s"
            assiste = input("Assiste One Piece? (s/n): ").lower() == "s"
            crud.alterar(id_cliente, nome, telefone, email, idade, cidade, torce, assiste)
        elif opcao == "3":
            crud.pesquisar_por_nome(input("Nome a pesquisar: "))
        elif opcao == "4":
            crud.remover(int(input("ID do cliente: ")))
        elif opcao == "5":
            crud.listar_todos()
        elif opcao == "6":
            crud.exibir_um(int(input("ID do cliente: ")))
        elif opcao == "7":
            crud.relatorio()
        elif opcao == "0":
            break

def menu_produtos():
    crud = CrudProduto()
    while True:
        print("\n --PRODUTOS-- ")
        print("1. Inserir produto")
        print("2. Alterar produto")
        print("3. Pesquisar produto por nome")
        print("4. Remover produto")
        print("5. Listar todos os produtos")
        print("6. Exibir produto pelo ID")
        print("7. Relatório de produtos")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade: "))
            tipo = input("Tipo (bebida/comida): ")
            origem = input("Origem (cidade): ")
            crud.inserir(nome, preco, quantidade, tipo, origem)
        elif opcao == "2":
            id_produto = int(input("ID do produto: "))
            nome = input("Novo nome: ")
            preco = float(input("Novo preço: "))
            quantidade = int(input("Nova quantidade: "))
            tipo = input("Tipo (bebida/comida): ")
            origem = input("Origem (cidade): ")
            crud.alterar(id_produto, nome, preco, quantidade, tipo, origem)
        elif opcao == "3":
            crud.pesquisar_por_nome(input("Nome a pesquisar: "))
        elif opcao == "4":
            crud.remover(int(input("ID do produto: ")))
        elif opcao == "5":
            crud.listar_todos()
        elif opcao == "6":
            crud.exibir_um(int(input("ID do produto: ")))
        elif opcao == "7":
            crud.relatorio()
        elif opcao == "0":
            break

def menu_vendedores():
    crud = CrudVendedor()
    while True:
        print("\n --VENDEDORES-- ")
        print("1. Inserir vendedor")
        print("2. Alterar vendedor")
        print("3. Remover vendedor")
        print("4. Listar vendedores")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            matricula = input("Matrícula: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            crud.inserir(nome, cpf, matricula, email, telefone)
        elif opcao == "2":
            id_v = int(input("ID do vendedor: "))
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            telefone = input("Novo telefone: ")
            status = input("Status (ativo/inativo/ferias/afastado): ")
            crud.alterar(id_v, nome, email, telefone, status)
        elif opcao == "3":
            crud.remover(int(input("ID do vendedor: ")))
        elif opcao == "4":
            crud.listar_todos()
        elif opcao == "0":
            break

def menu_compras():
    crud = CrudCompra()
    while True:
        print("\n --COMPRAS-- ")
        print("1. Nova compra")
        print("2. Adicionar item à compra")
        print("3. Finalizar compra")
        print("4. Listar compras")
        print("5. Relatório de compras")
        print("0. Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            cliente_id = int(input("ID do cliente: "))
            vendedor_id = int(input("ID do vendedor: "))
            crud.nova_compra(cliente_id, vendedor_id)
        elif opcao == "2":
            compra_id = int(input("ID da compra: "))
            produto_id = int(input("ID do produto: "))
            qtde = int(input("Quantidade: "))
            crud.adicionar_item(compra_id, produto_id, qtde)
        elif opcao == "3":
            compra_id = int(input("ID da compra: "))
            forma_id = int(input("ID da forma de pagamento: "))
            crud.finalizar(compra_id, forma_id)
        elif opcao == "4":
            crud.listar_todos()
        elif opcao == "5":
            crud.relatorio()
        elif opcao == "0":
            break

def main():
    while True:
        menu_principal()
        opcao = input("Escolha: ")

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_vendedores()
        elif opcao == "4":
            menu_compras()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("⚠️ Opção inválida!")

if __name__ == "__main__":
    main()
