import pyautogui
import time
import os
import ctypes
import sys
import threading
from datetime import datetime

# Disable the fail-safe feature
pyautogui.FAILSAFE = False

def animate_rotating_chars(duration):
    chars = ['\\', '|', '-', '/']
    index = 0
    start_time = time.time()

    while time.time() - start_time < duration:
        current_char = chars[index]
        print(f"Aguarde {current_char}", end='\r')
        index = (index + 1) % len(chars)
        time.sleep(0.1)  # Adjust delay as needed

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("Execução em administrador.")
        return True
    else:
        print("Solicitando autorização para executar como administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False
    

def start_animation():
    while True:
        animate_rotating_chars(0.5)

# List of image filenames
image_filenames = [    
    "missao_concluida.jpg",
    "missao_aceita.jpg",    
    "pular_bla.jpg",
    "pular_blabla.jpg",
    "pular_blablabla.jpg",
    "limite_campanha_diaria_ignorar_missao.jpg",
    "teletransportar.jpg",
    "diretiva_disponivel_guilda.jpg",
    "guilda_atualizar_diretivas.jpg",    
    "guilda_99.jpg",
    "guilda_240.jpg",
    "guilda_400.jpg",
    "sair_menu.jpg",
    "sair_menu.jpg",    
    "equipar.jpg",
    "resussitar.jpg",
    #"toque_na_tela.jpg",
    "teletransportar.jpg",
    "porcao_zerada.jpg",
    "sendo_atacado.jpg",
    "saida_masmorra.jpg",
    "teletransportar.jpg",
    "teletransportar.jpg",
    "sendo_atacado_3.jpg",
    "saida_masmorra.jpg",
    "teletransportar.jpg",
    "teletransportar.jpg",
    "sobre_ataque.jpg",
    "saida_masmorra.jpg",
    "teletransportar.jpg",    
    "teletransportar.jpg",
    #"receber_tudo.jpg",
    "obter.jpg",
    "guilda_obter.jpg",
    "equipe_ok.jpg",
    "aceitar_masmorra_equipe.jpg",
    "aprovacao_masmorra_equipe.jpg",
    "objetivo_masmorra_equipe_icon.jpg",
    "fechar.jpg"
]

# Variável para armazenar a data em que limite_campanha_diaria foi detectada
limite_detectado_data = None

# Variáveis de controle para cliques únicos masmorra equipe
clicou_resussitar = False
clicou_masmorra = False
masmorra_equipe_aceita = False
masmorra_cliques = 0
masmorra_cliques_data = None

# Variável para armazenar o horário do último clique
ultimo_clique_masmorra = None

def execute():
    # Inicia a animação em uma thread separada
    threading.Thread(target=start_animation, daemon=True).start()

    global clicou_resussitar, clicou_masmorra, masmorra_equipe_aceita, masmorra_cliques, masmorra_cliques_data, ultimo_clique_masmorra

    while True:
        global limite_detectado_data
        is_sair_guilda = False
        is_sair_masmorra = False

        # Obtém a data atual
        hoje = datetime.now().date()

        # Reseta o contador de cliques na masmorra de equipe se for um novo dia
        if masmorra_cliques_data != hoje:
            masmorra_cliques = 0
            masmorra_cliques_data = hoje

        # Verifica se já detectou limite_campanha_diaria hoje
        if limite_detectado_data == hoje:
            ignore_missao_aceita = True
        else:
            ignore_missao_aceita = False

        for image_filename in image_filenames:
            # Ignora "missao_aceita.jpg" se já detectou "limite_campanha_diaria_ignorar_missao.jpg" no dia atual
            if ignore_missao_aceita and (image_filename == "missao_aceita.jpg" or image_filename == "diretiva_disponivel_guilda.jpg"):
                continue

            # Caminho para a imagem
            image_path = os.path.join(os.path.dirname(__file__), image_filename)

            try:
                image_location = pyautogui.locateOnScreen(image_path, confidence=0.85)
                if image_location:

                    #INI - Masmorra equipe
                    
                    # Registro de aprovação da masmorra
                    if image_filename == "aceitar_masmorra_equipe.jpg":
                        agora = time.time()  # Obtém o timestamp atual
                        if ultimo_clique_masmorra is None or (agora - ultimo_clique_masmorra) >= 60:
                            #x, y = pyautogui.center(image_location)
                            #pyautogui.click(x, y)
                            print("Clique registrado em 'aceitar_masmorra_equipe.jpg'")
                            ultimo_clique_masmorra = agora  # Atualiza o horário do último clique
                            masmorra_cliques += 1
                            print(f"Masmorra de equipe aceita! Cliques hoje: {masmorra_cliques}")
                            masmorra_equipe_aceita = True
                            clicou_resussitar = True  # Ativa a flag para ressuscitar
                        else:
                            tempo_restante = 60 - (agora - ultimo_clique_masmorra)
                            print(f"Aguardando {tempo_restante:.1f} segundos antes do próximo clique na masmorra de equipe.")
                            #print("Limite diário de cliques na masmorra de equipe atingido.")
                            continue

                    #if image_filename == "aceitar_masmorra_equipe.jpg":
                    #    masmorra_equipe_aceita = True
                    #    clicou_resussitar = True  # Ativa a flag para ressuscitar
                    #    print("Masmorra de equipe aceita!")

                    # Detecção de "resussitar.jpg" condicionada à aprovação da masmorra
                    if image_filename == "resussitar.jpg" and masmorra_equipe_aceita:
                        clicou_resussitar = True  # Ativa a flag para ressuscitar
                        print("Preparado para ressuscitar na masmorra de equipe.")

                    # Clique único após ressuscitar
                    if clicou_resussitar:
                        if image_filename == "objetivo_masmorra_equipe_icon.jpg" and not clicou_masmorra:
                            x, y = pyautogui.center(image_location)
                            x += 40  # Ajusta o clique x pixels para a direita
                            pyautogui.click(x, y)
                            print("Clicou em 'objetivo_masmorra_equipe_icon.jpg'")
                            clicou_resussitar = False  # Reseta a flag de ressuscitar
                            clicou_masmorra = True  # Marca que já clicou na masmorra
                            masmorra_equipe_aceita = False  # Reseta a aprovação da masmorra
                            break

                        elif image_filename == "aceitar_masmorra_equipe.jpg" and not clicou_masmorra:
                            x, y = pyautogui.center(image_location)
                            pyautogui.click(x, y)
                            print("Clicou em 'aceitar_masmorra_equipe.jpg'")
                            clicou_resussitar = False  # Reseta a flag de ressuscitar
                            clicou_masmorra = True  # Marca que já clicou na masmorra
                            masmorra_equipe_aceita = False  # Reseta a aprovação da masmorra
                            break

                    # Ignora "objetivo_masmorra_equipe_icon.jpg" fora do contexto
                    if image_filename == "objetivo_masmorra_equipe_icon.jpg":
                        continue
                    if image_filename == "guilda_obter.jpg":
                        clicou_resussitar = False  # Reseta a flag de ressuscitar
                        clicou_masmorra = False  # Marca que já clicou na masmorra
                        masmorra_equipe_aceita = False  # Reseta a aprovação da masmorra

                    #FIM - Masmorra equipe
 
                    # Se "limite_campanha_diaria_ignorar_missao.jpg" for detectada, salva a data
                    if image_filename == "limite_campanha_diaria_ignorar_missao.jpg":
                        limite_detectado_data = hoje
                        print("Limite de campanha diária detectado. Ignorando missões para o dia.")

                    elif image_filename in ["guilda_99.jpg", "guilda_240.jpg", "guilda_400.jpg"]:
                        pyautogui.click(577, 592)
                        is_sair_guilda = True

                    elif image_filename in ["porcao_zerada.jpg", "sendo_atacado.jpg", "sobre_ataque.jpg", "sendo_atacado_3.jpg"] and not is_sair_masmorra:
                        is_sair_masmorra = True

                    else:
                        image_name, _ = os.path.splitext(image_filename)
                        print(f"Detectada acao: {image_name}                         ")
                        x, y = pyautogui.center(image_location)

                        if image_filename == "sair_menu.jpg" and not is_sair_guilda:
                            is_sair_guilda = False
                            continue

                        if image_filename == "saida_masmorra.jpg" and not is_sair_masmorra:
                            is_sair_masmorra = False
                            continue

                        #if image_filename in ["porcao_zerada.jpg", "sendo_atacado.jpg", "sobre_ataque.jpg", "sendo_atacado_3.jpg"]:
                        #    continue
                        
                        pyautogui.click(x, y)
                        time.sleep(0.5)

            except pyautogui.ImageNotFoundException:
                pass

        #animate_rotating_chars(0.5)

if __name__ == "__main__":
    if run_as_admin():
        execute()
    else:
        print("Você precisa autorizar a execução como administrador.")
