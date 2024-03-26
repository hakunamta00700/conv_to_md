from tqdm import tqdm
from loguru import logger
import html2text
import bs4
from pathlib import Path


class TqdmLoggingHandler:
    def write(self, message):
        # tqdm.write를 사용하여 로그 메시지를 안전하게 출력
        tqdm.write(message, end='')

    def flush(self):
        # 이 메소드는 로거 핸들러에 필요하지만, tqdm.write에서는 필요하지 않음
        pass


logger.remove()

# 새로운 핸들러 추가
logger.add(TqdmLoggingHandler(), format="{time} {level} {message}", level="INFO")


class MarkdownConverter:
    def __init__(self, target_directory):
        self.target_directory = Path(target_directory)
        if self.target_directory.exists() is False:
            Path(target_directory).mkdir()
        self.text_maker = html2text.HTML2Text()

    def read_html_file(self, input_filename):
        with open(input_filename, "r", encoding="utf-8") as file:
            return file.read()

    def find_conversations(self, html_content):
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        return soup.find_all("div", class_="conversation")

    def replace_element_with_new_tag(self, html_content, target_class, new_tag_name):
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        for target_element in soup.find_all("div", class_=target_class):
            new_tag = soup.new_tag(new_tag_name)
            new_tag.string = target_element.get_text()
            target_element.replace_with(new_tag)
        return soup.prettify()

    def write_markdown_file(self, content, filename):
        filepath = self.target_directory / filename
        logger.info(f"Writing to file: {filepath}")
        with filepath.open("w", encoding="utf-8") as file:
            file.write(content)

    def convert_to_markdown(self, html_content):
        return self.text_maker.handle(html_content)

    def process_conversation(self, conversation):
        head = conversation.find("h4").get_text().replace("/", "_").replace("\\", "_")  # Safe filename
        new_html = self.replace_element_with_new_tag(conversation.prettify(), "author", "strong")
        markdown = self.convert_to_markdown(new_html)
        processed_document = "\n".join(line.lstrip() for line in markdown.split("\n"))
        self.write_markdown_file(processed_document, f"{head}.md")

    def convert(self, input_filename):
        html_content = self.read_html_file(input_filename)
        conversations = self.find_conversations(html_content)
        for conv in tqdm(conversations, desc="Converting conversations"):
            try:
                self.process_conversation(conv)
            except Exception as err:
                logger.error(err)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <target_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    target_dir = sys.argv[2]

    converter = MarkdownConverter(target_dir)
    converter.convert(input_file)
