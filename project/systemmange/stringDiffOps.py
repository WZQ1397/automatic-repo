#!/usr/bin/python
import difflib

text1 = """text1_lines
"""

text1_lines = text1.splitlines()

text2 = """text2_lines
"""

text2_lines = text2.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print '\n'.join(list(diff))