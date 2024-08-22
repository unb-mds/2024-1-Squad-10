import pytest
from frontend.Menu import generate_html_with_css

def test_generate_html_with_css():
    html_content = '<img src="images/licitanow.png"> <img src="images/licitacao.png">'
    css_content = "body { background-color: #fff; }"
    logo_base64 = "fake_logo_base64"
    licitacao_base64 = "fake_licitacao_base64"

    expected_output = f"""
        <style>
        {css_content}
        </style>
        <img src="data:image/png;base64,{logo_base64}"> <img src="data:image/png;base64,{licitacao_base64}">
    """
    
    result = generate_html_with_css(html_content, css_content, logo_base64, licitacao_base64)
    assert result.strip() == expected_output.strip()