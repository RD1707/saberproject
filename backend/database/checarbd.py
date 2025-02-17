from bdsaber import criar_tabela, checar_bd

criar_tabela()

usuarios = checar_bd()
for usuario in usuarios: 
    print(usuario)