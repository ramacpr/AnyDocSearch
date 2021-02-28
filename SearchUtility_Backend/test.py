import PyPDFEx as PDFHelper
pdf_file_obj = open("D:\\Projects\\SearchUtility\\SearchUtility_Backend\\pdfFiles\\pandas.pdf", "rb")
pdf_reader = PDFHelper.PdfFileReader(pdf_file_obj)
page_obj = pdf_reader.getPage(4)
content = page_obj.extractText().lower()
print(content)