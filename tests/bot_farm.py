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
    "guilda_400.jpg",
    "guilda_240.jpg",
    "sair_menu.jpg",
    "sair_menu.jpg",    
    "equipar.jpg",
    "resussitar.jpg",
    #"toque_na_tela.jpg",
    "teletransportar.jpg",
    "porcao_zerada.jpg",
    "sendo_atacado.jpg",
    "sendo_atacado_2.jpg",
    "sobre_ataque.jpg",
    "saida_masmorra.jpg",
    "teletransportar.jpg",
    "equipe_ok.jpg"    
]

# Variável para armazenar a data em que limite_campanha_diaria foi detectada
limite_detectado_data = None

def execute():
    # Inicia a animação em uma thread separada
    threading.Thread(target=start_animation, daemon=True).start()

    while True:
        global limite_detectado_data
        is_sair_guilda = False
        is_sair_masmorra = False

        # Obtém a data atual
        hoje = datetime.now().date()

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
                image_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if image_location:
                    # Se "limite_campanha_diaria_ignorar_missao.jpg" for detectada, salva a data
                    if image_filename == "limite_campanha_diaria_ignorar_missao.jpg":
                        limite_detectado_data = hoje
                        print("Limite de campanha diária detectado. Ignorando missões para o dia.")

                    elif image_filename in ["guilda_400.jpg", "guilda_240.jpg"]:
                        pyautogui.click(577, 592)
                        is_sair_guilda = True

                    elif image_filename in ["porcao_zerada.jpg", "sendo_atacado.jpg", "sobre_ataque.jpg"] and not is_sair_masmorra:
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

                        if image_filename in ["porcao_zerada.jpg", "sendo_atacado.jpg", "sobre_ataque.jpg", "sendo_atacado_2.jpg"]:
                            continue
                        
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
