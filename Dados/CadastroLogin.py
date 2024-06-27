import os # Importa a biblioteca os para operações relacionadas ao sistema operacional.
import ast # Importa a biblioteca ast para análise sintática de literais de strings Python.
import re # Importa a biblioteca re para expressões regulares.

def verificar_existencia_usuario(email): # Verifica se um usuário com o email fornecido já existe no arquivo 'usuarios.txt'. Retorna True se o usuário existe, False caso contrário.
    
    if not os.path.exists("usuarios.txt"):  # Verifica se 'usuarios.txt' existe.
        return False  # Retorna False se não existir.

    with open("usuarios.txt", "r") as arquivo:  # Abre 'usuarios.txt' em modo de leitura.
        for linha in arquivo:  
            usuarios = ast.literal_eval(linha)  # Converte a linha em um dicionário Python.
            email_armazenado = usuarios.get("Email")  # Obtém o email armazenado.
            if email == email_armazenado:  # Verifica se o email fornecido já existe.
                return True  
    return False  # Retorna False se o usuário não existe.




def validar_email(email): #Valida o formato do email usando expressão regular. Retorna True se o email estiver no formato correto, False caso contrário.
   
    # Expressão regular para validar o formato do email
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex_email, email) is not None

def validar_senha(senha): # Valida se a senha contém apenas números. Retorna True se a senha contém apenas números, False caso contrário.
   
    return senha.isdigit()




def cadastrar_usuario(): # Solicita informações do usuário e as salva no arquivo 'usuarios.txt'.
    
    nome = input("Digite o nome: ")  
    email = input("Digite o e-mail: ")  



# Valida o formato do email
    if not validar_email(email):
        print("O email inserido não está em um formato válido.")
        return




    if verificar_existencia_usuario(email):  # Verifica se o usuário já está cadastrado.
        print("Este usuário já está cadastrado.")
        return
    else:
        senha = input("Digite a senha: ")  
        confirmacao_senha = input("Confirme a senha: ")  # Confirmação da senha.

        if senha != confirmacao_senha:  # Verifica se as senhas coincidem.
            print("As senhas não coincidem. Tente novamente.")
            return


# Valida se a senha contém apenas números
        if not validar_senha(senha):
            print("A senha deve conter apenas números.")
            return 

        with open("usuarios.txt", "a") as arquivo:  # Abre 'usuarios.txt' em modo de adição.
            dados = {"Nome": nome, "Email": email, "Senha": senha}  # Cria um dicionário com os dados do usuário.
            arquivo.write(str(dados) + "\n")  # Escreve os dados do usuário no arquivo.

        print("Usuário cadastrado com sucesso!")  # Confirmação do cadastro.

def login_usuario(): # Realiza o login do usuário.
    
    email = input("Digite o e-mail: ")  
    senha = input("Digite a senha: ") 

    with open("usuarios.txt", "r") as arquivo:  # Abre 'usuarios.txt' em modo de leitura.
        for linha in arquivo:  
            usuarios = ast.literal_eval(linha)  # Converte a linha em um dicionário Python.
            email_armazenado = usuarios.get("Email")  # Obtém o email armazenado.
            senha_armazenada = usuarios.get("Senha")  # Obtém a senha armazenada.
            if email == email_armazenado and senha == senha_armazenada:  # Verifica se o email e a senha correspondem.
                print("Login bem sucedido!")  
                return
        print("Email e/ou senha incorretos.")  # Mensagem de email ou senha incorretos.

def recuperar_senha(): # Permite ao usuário recuperar sua senha fornecendo seu email.

    email = input("Digite o e-mail para recuperar a senha: ")

    with open("usuarios.txt", "r") as arquivo: # Abre 'usuarios.txt' em modo de leitura.
        for linha in arquivo:
            usuarios = ast.literal_eval(linha) # Converte a linha em um dicionário Python. 
            email_armazenado = usuarios.get("Email") # Obtém o email armazenado.
            if email == email_armazenado: # Verifica se o email fornecido já existe.
                print("Sua senha é:", usuarios.get("Senha")) # Mostra a senha para o usuário.
                return
        print("Email não encontrado. Verifique se o email foi digitado corretamente.")

def main(): # Função principal.
    
    while True:  # Loop principal do programa.
        print("\n=== Sistema de Cadastro ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Recuperar senha")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")  # Solicita a opção ao usuário.

        if opcao == "1":  # Se a opção escolhida for '1', chama a função para cadastrar usuário.
            cadastrar_usuario() 
        elif opcao == "2":  # Se a opção escolhida for '2', chama a função para realizar o login.
            login_usuario()
        elif opcao == "3":
            recuperar_senha()  
        elif opcao == "4":  # Se a opção escolhida for '4', aparece mensagem de saída e sai do loop.
            print("Saindo do programa...")  
            break  
        else:
            print("Opção inválida. Tente novamente.")  # Mensagem de opção inválida.

if __name__ == "__main__":
    main()