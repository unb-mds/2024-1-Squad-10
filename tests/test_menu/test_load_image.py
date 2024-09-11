# test_load_image_base64.py
import base64
from frontend.Menu import load_image_base64


def test_load_image_base64(tmp_path):
    # Dados fictícios para a imagem
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00"
    image_path = tmp_path / "test_image.png"
    image_path.write_bytes(image_content)

    # Chama a função para carregar a imagem e codificá-la em base64
    encoded_image = load_image_base64(image_path)

    # Verifica se a imagem foi codificada corretamente
    assert encoded_image == base64.b64encode(image_content).decode()


def test_load_image_base64_file_not_found():
    # Chama a função para uma imagem que não existe
    result = load_image_base64("non_existing_image.png")

    # Verifica se o resultado é None
    assert result is None
