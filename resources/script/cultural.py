#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


class ParserPdf(object):
    def __init__(self, file_path):
        self._path = file_path
        self.extracted_text = ''
        self.grade_dict = {}
        self.grade_index = 0
        self.doc = self.init_doc()
        self.device, self.interpreter = self.init_device()

    def init_doc(self):
        fp = open(self._path, 'rb')
        pdf_parser = PDFParser(fp)
        doc = PDFDocument()
        pdf_parser.set_document(doc)
        doc.set_parser(pdf_parser)
        doc.initialize('')
        return doc

    @staticmethod
    def init_device():
        """初始化pdf解析对象"""
        rsrc_mgr = PDFResourceManager()
        la_params = LAParams()
        la_params.char_margin = 1.0
        la_params.word_margin = 1.0
        device = PDFPageAggregator(rsrc_mgr, laparams=la_params)
        interpreter = PDFPageInterpreter(rsrc_mgr, device)
        return device, interpreter

    @staticmethod
    def filter_error(text):
        """过来冗余信息"""
        if '.........' in text:
            return False
        if '链接：' in text:
            return False
        if len(text.strip()) == 1 or len(text.strip()) == 2 and '目录' in text:
            return False

        return True

    @staticmethod
    def parse_people(text: str):
        lines = text.split('\n')
        result = []
        for num, line in enumerate(lines):
            if '传：' in line:
                result.append(' '.join(line.split()[:-1]))
                result.append([])
                continue
            names = line.replace('）', ('） ')).replace(')', ') ').split()
            if len(names) == 1 and len(result) == 0:
                return ['', names]
            for index, name in enumerate(names):
                if len(name) == 1:
                    if index + 1 == len(names):
                        lines[num + 1] = name + ' ' + lines[num + 1]
                        break
                    names[index + 1] = ' '.join(names[index: index + 2])
                if len(name) <= 1:
                    continue
                assert len(result) > 1
                result[-1].append(name)
        return result

    def parser(self):
        for page in self.doc.get_pages():
            self.interpreter.process_page(page)
            layout = self.device.get_result()
            if layout.pageid <= 3:
                continue
            for index, lt_obj in enumerate(layout):
                if index <= 2:
                    continue
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    if not self.filter_error(text):
                        continue
                    if lt_obj.height < 20:
                        self.extracted_text += text
                        continue
                    if lt_obj.height >= 20:
                        if self.grade_index > 0:
                            self.grade_dict[self.grade_index].extend(self.parse_people(self.extracted_text))
                        self.extracted_text = ''
                        self.grade_index += 1
                        self.grade_dict[self.grade_index] = []


if __name__ == '__main__':
    pdf_path = '/Users/flytrap/code/github/xym/people/xym.pdf'
    parser = ParserPdf(pdf_path)
    parser.parser()
    print(len(parser.grade_dict))
