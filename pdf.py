import fitz  # (Precisa-se de instalar o pip install PyMuPDF) PyMuPDF é uma biblioteca para trabalhar com documentos PDF
import requests
from collections import Counter

class PDFAnalyzer:
    def __init__(self, pdf_url): # Inicializa o analisador de PDF com uma URL
        self.pdf_url = pdf_url
        self.pdf_bytes = self.download_pdf()
        self.document = self.open_pdf()

    def download_pdf(self): # Realiza o download do PDF da URL
        response = requests.get(self.pdf_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Erro ao fazer o download do PDF da URL: {self.pdf_url}")

    def open_pdf(self): # Abre o PDF a partir dos bytes baixados
        return fitz.open(stream=self.pdf_bytes, filetype="pdf")

    def extract_word_count(self): # Extrai a quantidade de palavras em todo o documento e por página
        total_word_count = 0
        page_word_count = []

        for page_num in range(len(self.document)):
            page = self.document[page_num]
            text = page.get_text()
            words = text.split()
            word_count = len(words)

            total_word_count += word_count
            page_word_count.append((f'Page {page_num + 1}', word_count))

        return total_word_count, page_word_count

    def extract_top_words(self): # Extrai as 20 palavras mais frequentes no documento
        all_text = " ".join([page.get_text() for page in self.document])
        words = all_text.split()
        word_counts = Counter(words)
        top_words = word_counts.most_common(20)
        return top_words

def main():
    pdf_url = 'https://portal.cetfaesa.com.br/midias/manualaluno-157.pdf'
    analyzer = PDFAnalyzer(pdf_url)

    while True:
        print("\nOpções:")
        print("1 - Quantidade total de palavras no manual")
        print("2 - Quantidade de palavras por página")
        print("3 - 20 palavras mais frequentes")
        print("4 - Sair")

        option = input("Escolha uma opção: ")

        if option == '1':
            total_word_count, _ = analyzer.extract_word_count()
            print(f"Quantidade total de palavras no manual: {total_word_count}")
        elif option == '2':
            _, page_word_count = analyzer.extract_word_count()
            for page, count in page_word_count:
                print(f"{page}: {count} palavras")
        elif option == '3':
            top_words = analyzer.extract_top_words()
            print("20 palavras mais frequentes:")
            for word, count in top_words:
                print(f"{word}: {count} vezes")
        elif option == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
