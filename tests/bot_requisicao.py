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

# List of image filenames with paths
image_filenames = [
    "img/requisicao_criacao/uncheck_item_disponivel_criacao.jpg",
    "img/requisicao_criacao/btn_atualizar.jpg",
    "img/requisicao_criacao/criar_experiente.jpg",
    "img/requisicao_criacao/criar_experiente.jpg",
    "img/requisicao_criacao/icone_criacao.jpg",    
    "img/requisicao_criacao/icone_criacao.jpg",
    "img/requisicao_criacao/criar.jpg",
    "img/requisicao_criacao/criar.jpg",
    "img/requisicao_criacao/criar2.jpg",
    "img/requisicao_criacao/ok.jpg",
    "img/requisicao_criacao/ok.jpg",
    "img/requisicao_criacao/fechar.jpg",
    "img/requisicao_criacao/fechar.jpg",    
]

def execute():
    while True:
        for image_filename in image_filenames:
            # Ensure the path to the image is correct
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, image_filename)
            #print(f"Procurando imagem: {image_path}")

            if not os.path.exists(image_path):
                print(f"Arquivo de imagem não encontrado: {image_path}")
                continue

            try:
                all_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=0.8))  # Adjusted confidence to 0.6
                
                if all_locations:
                    # Select the lowest match
                    lowest_location = max(all_locations, key=lambda loc: loc.top)

                    # Get the image name without the extension
                    image_name, _ = os.path.splitext(image_filename)
                    print(f"Detectada acao: {image_name}                         ")

                    # Get the coordinates of the center of the image
                    x, y = pyautogui.center(lowest_location)

                    # Click on the center of the image
                    pyautogui.click(x, y)

                    # Optional pause after each click
                    time.sleep(0.5)  # Adjust delay as needed
                #else:
                #    print(f"Imagem não encontrada na tela: {image_filename}")
            except pyautogui.ImageNotFoundException:
                #print(f"Exceção de imagem não encontrada: {image_filename}")
                pass
            except Exception: # as e:
                #print(f"Ocorreu um erro ao localizar a imagem {image_filename}: {e}")
                pass

        animate_rotating_chars(2)

if __name__ == "__main__":
    if run_as_admin():
        execute()
    else:
        print("Você precisa autorizar a execução como administrador.")
