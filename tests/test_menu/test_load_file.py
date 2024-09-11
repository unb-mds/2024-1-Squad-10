# test_load_file.py
from frontend.Menu import load_file


def test_load_file(tmp_path):
    # Dados fictícios para o arquivo de texto
    file_content = "Este é um arquivo de teste."
    test_file = tmp_path / "test_file.txt"
    test_file.write_text(file_content, encoding="utf-8")

    # Chama a função para carregar o arquivo
    loaded_content = load_file(test_file)

    # Verifica se o conteúdo carregado é o esperado
    assert loaded_content == file_content
