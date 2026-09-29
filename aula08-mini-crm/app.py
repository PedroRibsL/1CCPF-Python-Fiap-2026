from model import model_lead
import control

def add_lead():
    name = input("Nome: ")
    email = input("E-mail: ")
    company = input("Empresa: ")
    step = input("Etapa de vendas: ")

    # validar as entradas do usuário
    # depois de validar... vamos modelar os dados
    print(model_lead(name, email, company, step))

    # depois de modelado... vamos enviar esse dict (leads) para o leads.json
    # para salvar, vamos usar o módulo control
    control.create_lead(model_lead(name, email, company, step))

    print("Lead adicionado (func)")

def list_leads():
    leads = control.read_leads()
    if not leads:
        print("Nenhum lead ainda")
        return

    print(f"## | {"Nome":<15} | {"E-mail":<10} | Empresa")
    for i, lead in enumerate(leads):
        print(f"{i:02d} | {lead["name"]:<15} | {lead["email"]:<10} | {lead["company"]}")

def search_leads():
    query = input("Buscar por: ").strip().lower()
    if not query:
        print("Consulta vazia!")
        return

    # envia a query para o control realizar a busca no leads.json
    leads_finded = control.read_leads_search(query)

    if not leads_finded:
        print("Nenhum lead encontrado")
        return

    print(f"## | {"Nome":<15} | {"E-mail":<10} | Empresa")
    for i, lead in leads_finded:
        print(f"{i:02d} | {lead["name"]:<15} | {lead["email"]:<10} | {lead["company"]}")


def export_leads():
    path_csv = control.export_csv()

    if path_csv is None:
        print("Não foi possivel exportar os leads")
    else:
        print(f"Exportado para {path_csv}")

def chose_index(): #lista os leads e devolve o q foi escolhido
    leads= control.read_leads()
    if not leads:
        print("Nenhuma lead ainda")
        return None

    list_leads()
    try:
        index = int(input("Digite o número (##) do lead: "))

    except ValueError:
        print("Número invalido!")
        return None

    if index < 0 or index >= len(leads):
        print("Lead não encontrada!")
        return None

    return index

def update_lead():
    index = chose_index()
    if index is None:
        return

    lead = control.read_leads()[index]
    print("Deixe em branco para manter o valor atual")

    new_data = {}
    for field, label in [("name", "Nome"), ("email", "E-mail"), ("company", "Empresa"), ("step", "Etapa de vendas")]:
        value = input(f"{label} [{lead.get(field,"")}]: ").strip()
        if value:
            new_data[field] = value

    if not new_data:
        print("Nada alterado!")
        return

    control.update_lead(index, new_data)
    print("Lead atualizado!")

def delete_lead():
    index = chose_index()
    if index is None:
        return

    confirm = input("Tem certeza que deseja apagar ? (s/n): ").lower().strip()
    if confirm != "s":
        print("Operação cancelada!")
        return

    removed = control.delete_lead(index)
    print(f"Lead {removed["name"]} removido")


def main():
    while True:
        print("\nMini CRM de Leads")
        print("[1] Adicionar lead")
        print("[2] Listar leads")
        print("[3] Buscar (nome/e-mail/empresa)")
        print("[4] Exportar CSV")
        print("[5] Atualizar lead")
        print("[6] Deletar lead")
        print("[0] Sair do programa")

        opt = input("Escolha uma opção: ")

        if opt == "1":
            add_lead()
        elif opt == "2":
            list_leads()
        elif opt == "3":
            search_leads()
        elif opt == "4":
            export_leads()
        elif opt == "5":
            update_lead()
        elif opt == "6":
            delete_lead()
        elif opt == "0":
            print("Até mais...")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
