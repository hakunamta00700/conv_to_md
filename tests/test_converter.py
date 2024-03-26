import pytest
from conv_to_md.converter import MarkdownConverter  # 'your_module'를 해당 모듈 이름으로 바꿔주세요.
from pathlib import Path
import bs4
import tempfile
import shutil
# 임시 디렉토리를 사용하여 파일 시스템에 영향을 주지 않고 테스트


@pytest.fixture
def temp_dir():
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)


def test_read_html_file(temp_dir):
    # 테스트 HTML 파일 생성
    test_html_content = "<html><body><div class='conversation'><h4>Title</h4></div></body></html>"
    test_html_path = Path(temp_dir) / "test.html"
    with open(test_html_path, "w", encoding="utf-8") as file:
        file.write(test_html_content)

    converter = MarkdownConverter(temp_dir)
    content = converter.read_html_file(str(test_html_path))
    assert test_html_content == content


def test_find_conversations():
    test_html_content = "<html><body><div class='conversation'><h4>Title</h4></div></body></html>"
    converter = MarkdownConverter("")
    conversations = converter.find_conversations(test_html_content)
    assert len(conversations) == 1
    assert isinstance(conversations[0], bs4.element.Tag)
    assert conversations[0].find("h4").get_text() == "Title"


def test_replace_element_with_new_tag():
    test_html_content = "<div class='author'>Author Name</div>"
    converter = MarkdownConverter("")
    updated_html = converter.replace_element_with_new_tag(test_html_content, "author", "strong")
    soup = bs4.BeautifulSoup(updated_html, "html.parser")
    assert soup.find("strong").get_text().strip() == "Author Name"


def test_convert_to_markdown():
    test_html_content = "<strong>Test Content</strong>"
    converter = MarkdownConverter("")
    markdown = converter.convert_to_markdown(test_html_content)
    assert "**Test Content**" in markdown


def test_write_and_read_markdown_file(temp_dir):
    test_markdown_content = "# Title\n\nSome content here."
    filename = "test.md"
    converter = MarkdownConverter(temp_dir)
    converter.write_markdown_file(test_markdown_content, filename)

    filepath = Path(temp_dir) / filename
    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    assert content == test_markdown_content
