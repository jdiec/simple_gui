# Copyright 2011, Thomas G. Dimiduk
#
# This file is part of GroupEng.
#
# GroupEng is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GroupEng is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with GroupEng.  If not, see <http://www.gnu.org/licenses/>.

import re

class InputError(Exception):
    def __init__(self, line, lineno, inf):
        self.line
        self.lineno
        self.inf
    def __str__(self):
        return "Can't understand: {0} at line {1} of {2}".format(
            self.line, self.lineno, self.inf)

def read_input(infile):
    if isinstance(infile, basestring):
        infile = file(infile)

    lines = infile.readlines()
    lines = [l.strip() for l in lines if l.strip() != '' and l.strip()[0] != '#']
    
    dek = {}

    rules = []

    i = 0

    while i < len(lines):
        line = lines[i]
        if re.match('class_?list', line):
            dek['classlist'] = split_key(line)[1]
        elif re.match('(group_?)?size', line):
            dek['group_size'] = split_key(line)[1]
        elif re.match('student_identifier', line) or re.match('[Ii][Dd]', line):
            dek['student_identifier'] = split_key(line)[1]
        elif line[0] == '-':
            line = line[1:]
            # read a rule
            rule = {}
            rule['name'] = split_key(line)[0]
            rule['attribute'] = split_key(line)[1]

            # read extra arguments
            while i+1 < len(lines) and lines[i+1][0] != '-':
                i += 1
                line = lines[i]
                key, val = split_key(line)
                val = tuple([v.strip() for v in val.split(',')])
                vals = []
                for v in val:
                    vs = tuple([vi.strip() for vi in v.split('=')])
                    if len(vs) == 1:
                        vs = vs[0]
                    vals.append(vs)
                rule[key] = vals
            rules.append(rule)
        else:
            raise InputError(line, i+1, infile.name)
                     
        i += 1

    dek['rules'] = rules
        
    return dek

def split_key(st):
    return [s.strip() for s in st.split(':')]
