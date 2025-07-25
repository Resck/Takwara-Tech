# generate_carousel.py (versão 5.0 - Com Títulos e Legendas)
import os
import sys
import re
from PIL import Image

# --- CONFIGURAÇÕES ---
DESTINO_BASE = "assets/images/carrosseis-otimizados" 
MAX_WIDTH = 800
JPEG_QUALITY = 80

def sanitize_for_id(text):
    s = text.lower()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s

def create_caption_from_filename(filename):
    """Cria uma legenda legível a partir do nome do ficheiro."""
    name_without_ext = os.path.splitext(filename)[0]
    # Substitui hífens e underscores por espaços
    caption = name_without_ext.replace('_', ' ').replace('-', ' ')
    return caption.capitalize()

def process_images_and_generate_html(source_dir, depth, title=""):
    if not os.path.isdir(source_dir):
        print(f"ERRO: A pasta de origem '{source_dir}' não foi encontrada.")
        return

    gallery_name = os.path.basename(os.path.normpath(source_dir))
    full_dest_dir = os.path.join('docs', DESTINO_BASE, gallery_name)
    
    os.makedirs(full_dest_dir, exist_ok=True)
    print(f"A processar imagens de '{source_dir}'...")

    image_files = []
    for filename in sorted(os.listdir(source_dir)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            source_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(full_dest_dir, filename)
            
            with Image.open(source_path) as img:
                if img.width > MAX_WIDTH:
                    aspect_ratio = img.height / img.width
                    new_height = int(MAX_WIDTH * aspect_ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                if img.mode != 'RGB': img = img.convert('RGB')
                img.save(dest_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            image_files.append(filename)

    carousel_id = f"carrossel-{sanitize_for_id(gallery_name)}"
    
    print("\n--- CÓDIGO HTML DO CARROSSEL (Copie e cole no seu ficheiro .md) ---")
    
    # Inicia o container geral
    html_output = f'<div class="carousel-container">\n'
    # Adiciona o título se ele for fornecido
    if title:
        html_output += f'  <h4 class="carousel-title">{title}</h4>\n'
    
    html_output += f'  <div id="{carousel_id}" class="splide">\n    <div class="splide__track">\n      <ul class="splide__list">\n'
    
    path_prefix = '../' * depth
    
    for filename in image_files:
        relative_image_path = f"{path_prefix}{DESTINO_BASE}/{gallery_name}/{filename}".replace("\\", "/")
        caption = create_caption_from_filename(filename)
        
        html_output += f'        <li class="splide__slide">\n'
        html_output += f'          <img src="{relative_image_path}" alt="{caption}">\n'
        # Adiciona a legenda abaixo da imagem
        html_output += f'          <p class="splide-caption">{caption}</p>\n'
        html_output += f'        </li>\n'

    html_output += '      </ul>\n    </div>\n  </div>\n</div>\n'
    print(html_output)
    print("--------------------------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python <script> <pasta_das_imagens> <profundidade> \"[Título Opcional]\"")
        print("Profundidade é o número de pastas dentro de 'docs'. Ex: 'docs/artigo.md' = 0, 'docs/tech/artigo.md' = 1.")
    else:
        source_dir = sys.argv[1]
        try:
            depth = int(sys.argv[2])
            # O título é opcional
            title = sys.argv[3] if len(sys.argv) > 3 else ""
            process_images_and_generate_html(source_dir, depth, title)
        except ValueError:
            print("ERRO: A profundidade deve ser um número inteiro (0, 1, 2, etc.).")