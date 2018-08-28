# -*- coding: utf-8 -*-

from string import Template
import os
import re
import shutil

import jinja2
from functional import seq

import pybee

def replace_str_by_template(text, *mapping, **kwds):
    s = Template(text)
    return s.safe_substitute(*mapping, **kwds)

def replace_by_template(tmp_path, out_path, encoding='UTF-8', \
        mapping=None, **kwds):

    text = pybee.path.read_file_with_encoding(tmp_path, encoding)
    s = replace_str_by_template(text, mapping, **kwds)
    pybee.path.write_file_with_encoding(out_pth, s, encoding)


def replace_by_pattern(fpath, replace_pattern_list, encoding='UTF-8', back_suffix='back'):
    if back_suffix:
        back_path=fpath + '.'+ back_suffix
        shutil.copyfile(fpath, back_path)

    
    compile_pattern_list = [ (re.compile(pattern), reple) for pattern, repl in replace_pattern_list ]

    lines = pybee.path.read_lines_with_encoding(fpath, encoding)
    change_lines=[]
    for idx, line in enumerate(lines):
        replace = False
        for pattern, repl in compile_pattern_list:
            if pattern.match(line):
                replace = True
                m = pattern.sub(repl, line)
                if m is None:
                    change_lines.append(line)
                else:
                    change_lines.append(m)

        if replace: continue
        change_lines.append(line)

    pybee.path.write_file_with_encoding(fpath, ''.join(change_lines), encoding)


def render_str_by_jinja_template(text, *mapping, **kwds):
    t = jinja2.Template(text)
    return t.render(*mapping, **kwds)

def render_by_jinja_template(tmp_path, out_path, encoding='UTF-8', \
        mapping=None, **kwds):

    text = pybee.path.read_file_with_encoding(tmp_path, encoding)
    s = render_str_by_jinja_template(text, mapping, **kwds)
    pybee.path.write_file_with_encoding(out_pth, s, encoding)

def delete_by_line_number(fpath, line_numbers, encoding='UTF-8', back_suffix='back', linesep=os.linesep):

    if back_suffix:
        back_path=fpath + '.'+ back_suffix
        shutil.copyfile(fpath, back_path)

    lines = pybee.path.read_lines_with_encoding(fpath, encoding)

    file_seq = seq(lines)
    text = file_seq.enumerate().filter(lambda x: x[0] not in line_numbers).make_string(linesep)

    pybee.path.write_file_with_encoding(fpath, text, encoding)

def match_by_pattern_list(pattern_list, s):
    for pattern in pattern_list:
        if not pattern.match(s): return False

    return True

def delete_by_pattern(fpath, pattern_str_list, encoding='UTF-8', back_suffix='back', linesep=os.linesep):
    if back_suffix:
        back_path=fpath + '.'+ back_suffix
        shutil.copyfile(fpath, back_path)

    pattern_list = [ re.compile(x) for x in pattern_str_list ]

    lines = pybee.path.read_lines_with_encoding(fpath, encoding)

    file_seq = seq(lines)
    text = file_seq.filter(\
            functools.partial(match_by_pattern_list(pattern_list))\
            ).make_string(linesep)

    pybee.path.write_file_with_encoding(fpath, text, encoding)

def insert_text_by_line_number(fpath, insert_text_list, encoding='UTF-8', back_suffix='back', linesep=os.linesep):
    if back_suffix:
        back_path=fpath + '.'+ back_suffix
        shutil.copyfile(fpath, back_path)

    insert_text_map={}
    for idx, text, after in insert_text_list:
        insert_text_map[idx] = (text, after)

    lines = pybee.path.read_lines_with_encoding(fpath, encoding)
    change_lines=[]
    for idx, line in enumerate(lines):
        if idx not in insert_text_map: 
            change_lines.append(line)
            continue
        text, after = insert_text_map[idx]
        m = text + linesep
        if not after:
            change_lines.append(m)
            change_lines.append(line)
        else:
            change_lines.append(line)
            change_lines.append(m)

    pybee.path.write_file_with_encoding(fpath, ''.join(change_lines), encoding)

def insert_text_by_pattern(fpath, pattern_text_list, encoding='UTF-8'):
    if back_suffix:
        back_path=fpath + '.'+ back_suffix
        shutil.copyfile(fpath, back_path)

    compile_pattern_text_list = [  (re.compile(x[0]), x[1], x[2]) for x in pattern_text_list ]

    lines = pybee.path.read_lines_with_encoding(fpath, encoding)
    change_lines=[]
    for idx, line in enumerate(lines):
        match = False
        for pattern, text, after in compile_pattern_text_list:
            if pattern.match(line):
                match = True
                m = text + linesep
                if not after: 
                    change_lines.append(m)
                    change_lines.append(line)
                else:
                    change_lines.append(line)
                    change_lines.append(m)
                continue

            if match: continue

            change_lines.append(line)

    pybee.path.write_file_with_encoding(fpath, ''.join(change_lines), encoding)
