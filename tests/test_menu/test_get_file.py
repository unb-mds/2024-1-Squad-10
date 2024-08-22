import pytest
import os
from frontend.Menu import get_file_paths

def test_get_file_paths(tmp_path):
    base_dir = tmp_path
    
    expected_paths = {
        "html": os.path.join(base_dir, 'index.html'),
        "css": os.path.join(base_dir, 'style.css'),
        "logo_image": os.path.join(base_dir, 'images', 'licitanow.png'),
        "licitacao_image": os.path.join(base_dir, 'images', 'licitacao.png'),
    }
    
    assert get_file_paths(base_dir) == expected_paths