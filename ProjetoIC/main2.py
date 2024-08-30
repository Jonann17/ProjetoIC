import configparser
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # Importar Pillow para manipulação de imagens

# Caminho para o arquivo de configuração
config_file = 'config.ini'

def calcular():
    # Obter os valores de entrada
    furos = int(entry_furos.get())
    largura = float(entry_largura.get())
    altura = float(entry_altura.get())
    comprimento = float(entry_comprimento.get())
    espesH_ceramica = float(entry_espesH_ceramica.get())
    espesV_ceramica = float(entry_espesV_ceramica.get())
    espes_argamassa = float(entry_espes_argamassa.get())

    # Calcular as áreas
    area1 = comprimento * espesH_ceramica
    area2 = comprimento * ((altura - ((furos / 2) + 1) * espesH_ceramica) / (furos / 2))
    area_a = (espes_argamassa * comprimento) + (espes_argamassa * (altura + espes_argamassa))
    areaTijolo = (4 * area1) + (3 * area2)

    # Calcular resistências térmicas
    resistencia1 = largura / COND_CERAMICA
    resistencia2 = (2 * (espesV_ceramica / COND_CERAMICA) + (espesH_ceramica / COND_CERAMICA) + 0.32)
    resistenciaA = largura / COND_ARGAMASSA
    Rtijolo = areaTijolo / (4 * (area1 / resistencia1) + 3 * (area2 / resistencia2))
    Rmodulo = (area_a + areaTijolo) / ((area_a / resistenciaA) + (areaTijolo / Rtijolo))
    Rtotal = 0.13 + Rmodulo + 0.04
    UT = 1 / Rtotal

    # Calcular capacidade térmica
    ct1 = largura * CESP_CERAMICA * DENS_CERAMICA
    ct2 = (2 * espesV_ceramica * CESP_CERAMICA * DENS_CERAMICA) + (espesH_ceramica * CESP_CERAMICA * DENS_CERAMICA)
    ctTijolo = (areaTijolo) / ((4 * area1 / ct1) + (3 * area2 / ct2))
    ctA = largura * CESP_ARGAMASSA * DENS_ARGAMASSA
    ctModulo = (area_a + areaTijolo) / ((area_a / ctA) + ((areaTijolo) / ctTijolo))

    # Calcular espessores equivalentes
    EeqCeramica = ctModulo / (2 * CESP_CERAMICA * DENS_CERAMICA)
    EeqAr = largura - 2 * EeqCeramica

    # Mostrar resultados
    resultado_texto.set(f"A capacidade térmica total é de {round(ctModulo, 3)} KJ/m2K\n"
                        f"A espessura da cerâmica para o modelo equivalente é de {round(EeqCeramica, 3)} m\n"
                        f"A espessura da camada de ar para o modelo equivalente é de {round(EeqAr, 3)} m")

# Função para ler o arquivo de configuração
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Ler as variáveis do arquivo de configuração
    COND_ARGAMASSA = config['DEFAULT'].getfloat('COND_ARGAMASSA')
    print(COND_ARGAMASSA)
    COND_CERAMICA = config['DEFAULT'].getfloat('COND_CERAMICA')
    DENS_ARGAMASSA = config['DEFAULT'].getfloat('DENS_ARGAMASSA')
    DENS_CERAMICA = config['DEFAULT'].getfloat('DENS_CERAMICA')
    CESP_CERAMICA = config['DEFAULT'].getfloat('CESP_CERAMICA')
    CESP_ARGAMASSA = config['DEFAULT'].getfloat('CESP_ARGAMASSA')
    RAr = config['DEFAULT'].getfloat('RAr')

    return COND_ARGAMASSA, COND_CERAMICA, DENS_ARGAMASSA, DENS_CERAMICA, CESP_CERAMICA, CESP_ARGAMASSA, RAr

# Variáveis globais para armazenar os frames
frame_sobre_atual = None
frame_principal = None

def sobre(root):
    global frame_sobre_atual, frame_principal

    # Ocultar o frame principal
    frame_principal.grid_forget()

    # Se já houver um frame, destrua-o completamente
    if frame_sobre_atual:
        frame_sobre_atual.destroy()

    # Criar um novo frame para exibir as informações sobre os desenvolvedores
    frame_sobre_atual = tk.Frame(root)
    frame_sobre_atual.grid(row=0, column=0, columnspan=2, pady=10)

    texto_sobre0 = ("[protótipo]\nSoftware Calculador de Propriedades Térmicas")

    texto_sobre1 = ("Este aplicativo tem objetivo de facilitar a inserção de componentes construtivos de edificações,\n"
                    "especificamente paredes, no software EnergyPlus, buscando simplificar a entrada de dados \n"
                    "para simulações de consumo de energia e desempenho térmico. O programa calcula o equivalente homogêneo\n"
                    "de um fechamento heterogêneo, ou seja, de um elemento construtivo que não possui distribuição\n"
                    "uniforme dos materiais, mantendo suas propriedades térmicas. O resultado esperado é aumentar a \n"
                    "confiabilidade na entrada de dados no EnergyPlus, além de reduzir o tempo necessário para o \n"
                    "cálculo de fechamentos equivalentes por parte do usuário.")

    texto_sobre2 = ("Desenvolvido por: Sofia Gaona e Jonathan Salinas\n\n"
                    "Prof. Dr. Egon Vettorazzi\nOrientador\n\n"
                    "Prof. Dr. Joylan N. Maciel.\nColaborador\n\n"
                    "Universidade Federal da Integração Latino Americana (UNILA)\nCopyright 2024")

    # Adicionar o texto com formatação em negrito, tamanho 12 e centralizado
    label_sobre1 = tk.Label(frame_sobre_atual, text=texto_sobre0, font=('Arial', 18, 'bold'), justify='center')
    label_sobre1.grid(row=0, column=0, padx=10, pady=10)

    # Adicionar o texto com formatação em negrito, tamanho 12 e centralizado
    label_sobre1 = tk.Label(frame_sobre_atual, text=texto_sobre1, font=('Helvetica', 14), justify='center')
    label_sobre1.grid(row=1, column=0, padx=10, pady=10)

    # Adicionar o texto com formatação em negrito, tamanho 12 e centralizado
    label_sobre2 = tk.Label(frame_sobre_atual, text=texto_sobre2, font=('Helvetica', 14, 'bold'), justify='center')
    label_sobre2.grid(row=2, column=0, padx=10, pady=10)

    # Carregar e exibir a imagem no frame "Sobre"
    imagem = Image.open("image/logo_unila.png")  # Substitua pelo caminho da sua imagem
    imagem = imagem.resize((174, 100), Image.Resampling.LANCZOS)  # Redimensionar a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)
    label_imagem = tk.Label(frame_sobre_atual, image=imagem_tk)
    label_imagem.image = imagem_tk  # Manter uma referência à imagem para evitar que seja coletada pelo garbage collector
    label_imagem.grid(row=3, column=0, pady=10)  # Posicionar a imagem no frame "Sobre"

    # Adicionar botão para fechar o frame "Sobre" e reexibir o frame principal
    button_fechar = tk.Button(frame_sobre_atual, text="Fechar", command=lambda: fechar_sobre(root))
    button_fechar.grid(row=4, column=0, pady=10)

def teste(root):
    global frame_sobre_atual, frame_principal

    # Ocultar o frame principal
    frame_principal.grid_forget()

    # Se já houver um frame, destrua-o completamente
    if frame_sobre_atual:
        frame_sobre_atual.destroy()

    # Criar um novo frame para exibir a imagem na janela "Teste"
    frame_sobre_atual = tk.Frame(root)
    frame_sobre_atual.grid(row=0, column=0, columnspan=2, pady=10)

    # Carregar e exibir a imagem no frame "Teste"
    imagem = Image.open("image/logo_unila.png")  # Substitua pelo caminho da sua imagem
    imagem = imagem.resize((174, 100), Image.Resampling.LANCZOS)  # Redimensionar a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)
    label_imagem = tk.Label(frame_sobre_atual, image=imagem_tk)
    label_imagem.image = imagem_tk  # Manter uma referência à imagem para evitar que seja coletada pelo garbage collector
    label_imagem.grid(row=0, column=0, pady=10)  # Posicionar a imagem no frame "Teste"

    # Adicionar botão para fechar o frame "Teste" e reexibir o frame principal
    button_fechar = tk.Button(frame_sobre_atual, text="Fechar", command=lambda: fechar_sobre(root))
    button_fechar.grid(row=1, column=0, pady=10)

def fechar_sobre(root):
    global frame_sobre_atual, frame_principal

    # Destruir o frame "Sobre" ou "Teste"
    if frame_sobre_atual:
        frame_sobre_atual.destroy()

    # Reexibir o frame principal
    frame_principal.grid(row=0, column=0, columnspan=2)

def criar_interface_grafica(root):
    global entry_furos, entry_largura, entry_altura, entry_comprimento, entry_espesH_ceramica, entry_espesV_ceramica, entry_espes_argamassa, resultado_texto, frame_principal

    # Criar o frame principal
    frame_principal = tk.Frame(root)
    frame_principal.grid(row=0, column=0, columnspan=2)

    label_furos = tk.Label(frame_principal, text="Quantidade de furos do bloco cerâmico:")
    label_furos.grid(row=0, column=0)

    # Usar Combobox em vez de Entry para selecionar a quantidade de furos
    entry_furos = ttk.Combobox(frame_principal, values=[3, 6, 9, 12])
    entry_furos.grid(row=0, column=1)
    entry_furos.current(0)  # Definir a primeira opção como padrão

    label_largura = tk.Label(frame_principal, text="Largura do bloco cerâmico (m):")
    label_largura.grid(row=1, column=0)
    entry_largura = tk.Entry(frame_principal)
    entry_largura.grid(row=1, column=1)

    label_altura = tk.Label(frame_principal, text="Altura do bloco cerâmico (m):")
    label_altura.grid(row=2, column=0)
    entry_altura = tk.Entry(frame_principal)
    entry_altura.grid(row=2, column=1)

    label_comprimento = tk.Label(frame_principal, text="Comprimento do bloco cerâmico (m):")
    label_comprimento.grid(row=3, column=0)
    entry_comprimento = tk.Entry(frame_principal)
    entry_comprimento.grid(row=3, column=1)

    label_espesH_ceramica = tk.Label(frame_principal, text="Espessura horizontal do bloco cerâmico (m):")
    label_espesH_ceramica.grid(row=4, column=0)
    entry_espesH_ceramica = tk.Entry(frame_principal)
    entry_espesH_ceramica.grid(row=4, column=1)

    label_espesV_ceramica = tk.Label(frame_principal, text="Espessura da face do bloco cerâmico (m):")
    label_espesV_ceramica.grid(row=5, column=0)
    entry_espesV_ceramica = tk.Entry(frame_principal)
    entry_espesV_ceramica.grid(row=5, column=1)

    label_espes_argamassa = tk.Label(frame_principal, text="Espessura da argamassa (m):")
    label_espes_argamassa.grid(row=6, column=0)
    entry_espes_argamassa = tk.Entry(frame_principal)
    entry_espes_argamassa.grid(row=6, column=1)

    # Adicionar um botão para calcular
    button_calcular = tk.Button(frame_principal, text="Calcular", command=calcular)
    button_calcular.grid(row=7, columnspan=2)

    # Mostrar resultados
    resultado_texto = tk.StringVar()
    label_resultado = tk.Label(frame_principal, textvariable=resultado_texto)
    label_resultado.grid(row=8, columnspan=2)

def main():
    global COND_ARGAMASSA, COND_CERAMICA, DENS_ARGAMASSA, DENS_CERAMICA, CESP_CERAMICA, CESP_ARGAMASSA, RAr
    # Chamar a função para ler as variáveis do arquivo de configuração
    COND_ARGAMASSA, COND_CERAMICA, DENS_ARGAMASSA, DENS_CERAMICA, CESP_CERAMICA, CESP_ARGAMASSA, RAr = read_config(config_file)

    # Criar a janela principal
    root = tk.Tk()
    root.title("[Protótipo] Calculadora de Propriedades Térmicas")

    # Criar o menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adicionar menu Ajuda
    menu_ajuda = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
    menu_ajuda.add_command(label="Sobre", command=lambda: sobre(root))
    menu_ajuda.add_command(label="Teste", command=lambda: teste(root))  # Adicionar opção "Teste" ao menu

    # Criar a interface gráfica
    criar_interface_grafica(root)

    # Iniciar a interface gráfica
    root.mainloop()

if (__name__ == "_main_"):
    main()