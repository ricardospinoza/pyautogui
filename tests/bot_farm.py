import pyautogui
import time
import os
import ctypes
import sys

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

# List of image filenames
image_filenames = [
    "missao_concluida.jpg",
    "missao_aceita.jpg",
    "pular_bla.jpg",
    "pular_blabla.jpg",
    "pular_blablabla.jpg",
    "diretiva_disponivel_guilda.jpg",
    "guilda_atualizar_diretivas.jpg",
    "guilda_400.jpg",
    "guilda_240.jpg",
    "sair_menu.jpg",
    "equipar.jpg",
    "resussitar.jpg",
    "teletransportar.jpg",
    "toque_na_tela.jpg"
]

def execute():
    while True:
        is_sair_guilda = False

        for image_filename in image_filenames:
            # Ensure the path to the image is correct
            image_path = os.path.join(os.path.dirname(__file__), image_filename)
            #print(f"Procurando imagem: {image_path}")

            try:
                image_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if image_location:
                    if image_filename in ["guilda_400.jpg", "guilda_240.jpg"]:
                        pyautogui.click(577, 592)
                        is_sair_guilda = True
                    else:
                        image_name, _ = os.path.splitext(image_filename)
                        print(f"Detectada acao: {image_name}                         ")
                        x, y = pyautogui.center(image_location)

                        if image_filename == "sair_menu.jpg" and not is_sair_guilda:
                            is_sair_guilda = False
                            continue

                        pyautogui.click(x, y)
                    time.sleep(1)
                #else:
                #    print(f"Imagem não encontrada: {image_filename}")
            except pyautogui.ImageNotFoundException:
                #print(f"Exceção de imagem não encontrada: {image_filename}")
                pass

        animate_rotating_chars(5)

if __name__ == "__main__":
    if run_as_admin():
        execute()
    else:
        print("Você precisa autorizar a execução como administrador.")
