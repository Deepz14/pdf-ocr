import PyPDF2
import re


class PdfExtract:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def process(self):
        reader = PyPDF2.PdfFileReader(self.pdf_path)
        words_in_the_page = reader.getPage(1).extractText().splitlines()

        source_dictionary = {
            "name": ["firstname", "name", "lastname", "insuredname", "nameofinsured"],
            "contact_number": ["number", "mobilenumber", "contactnumber"],
            "policy_number": ["policynumber", "previouspolicynumber"]
        }

        output_dictionary = {
            "name": [],
            "contact_number": [],
            "policy_number": []
        }

        for word_index, words in enumerate(words_in_the_page):
            words = words.lower()
            words = re.sub(r"[^a-zA-Z0-9]", "", words)

            for source, sourcewords in source_dictionary.items():
                if words in sourcewords:
                    output_dictionary[source].append(words_in_the_page[word_index + 1])
        print(output_dictionary)

        return output_dictionary
