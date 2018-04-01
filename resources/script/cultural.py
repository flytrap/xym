#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


class ParserPdf(object):
    birth_death_tag = ['［', '］']
    nick_tag = ['〔', '〕']
    address_tag = ['＜', '＞']
    relate_tag = ['（', '）']
    all_tags = [birth_death_tag, nick_tag, address_tag, relate_tag]

    def __init__(self, file_path):
        self._path = file_path
        self.extracted_text = ''
        self.grade_dict = {}
        self.grade_index = 0
        self.doc = self.init_doc()
        self.device, self.interpreter = self.init_device()
        self.first_page = self.get_first_line()
        self.is_end = False

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
        """过滤冗余信息"""
        if '.........' in text:
            return False
        if '链接：' in text:
            return False
        if len(text.strip()) == 1 or len(text.strip()) == 2 and '目录' in text:
            return False

        return True

    def get_first_line(self):
        for page in self.doc.get_pages():
            self.interpreter.process_page(page)
            layout = self.device.get_result()
            for index, lt_obj in enumerate(layout):
                if index <= 2:
                    continue
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    if lt_obj.height >= 18 and '.........' not in text and '第一代（祖师）' in text:
                        self.device, self.interpreter = self.init_device()
                        return layout.pageid

    @staticmethod
    def check_end(text):
        if '在《形意拳传承谱系·说明》中，对于排序问题是这样规定的' in text:
            return True
        return False

    @classmethod
    def parse_people(cls, text: str):
        lines = text.split('\n')
        result = []
        names = ''
        for num, line in enumerate(lines):
            if '传：' in line:
                if num != 0:
                    cls.split_names(names, result)
                result.append(line.split('传：')[0].strip())
                result.append([])
                names = ''
                continue
            if len(line) < 15 and line.strip().endswith(' 传'):
                # 补丁，修复有问题数据
                if num != 0:
                    cls.split_names(names, result)
                print(line)
                result.append(line.split(' 传')[0].strip())
                result.append([])
                names = ''
                continue
            names += line
        if names:
            result = cls.split_names(names, result)
        return result

    @classmethod
    def fix_text(cls, text: str):
        for tag in cls.all_tags[0]:
            text = text.replace(' {}'.format(tag), tag)
        text = text.replace(' (', '(')
        return text

    @classmethod
    def split_names(cls, line, result):
        line = cls.fix_text(line)
        names = line.replace('＞', '＞ ').replace('）', ('） ')).split()
        if len(names) == 1 and len(result) == 0:
            return ['', names]
        for index, name in enumerate(names):
            if len(name) == 1:
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
            if layout.pageid < self.first_page:
                continue
            for index, lt_obj in enumerate(layout):
                if index <= 2:
                    continue
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    text = lt_obj.get_text()
                    if not self.filter_error(text):
                        continue
                    if self.check_end(text):
                        self.is_end = True
                    if lt_obj.height < 18 or lt_obj.height > 25:
                        if not self.is_end:
                            self.extracted_text += text
                        continue
                    if lt_obj.height >= 18:
                        if self.grade_index > 0:
                            self.grade_dict[self.grade_index].extend(self.parse_people(self.extracted_text))
                        if self.is_end:
                            return
                        self.extracted_text = ''
                        self.grade_index += 1
                        self.grade_dict[self.grade_index] = []


if __name__ == '__main__':
    pdf_path = '/Users/flytrap/code/github/xym/people/xym.pdf'
    parser = ParserPdf(pdf_path)
    parser.parser()
    print(len(parser.grade_dict))
