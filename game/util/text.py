import textwrap
import re


class DocumentWrapper(textwrap.TextWrapper):

    def wrap(self, text):
        wrapped_lines = []
        wrapper = textwrap.TextWrapper.wrap
        ending = re.compile(r"(\n\s*\n)", re.MULTILINE)
        paragraphs = ending.split(text)
        for line in paragraphs:
            if line.isspace():
                if not self.replace_whitespace:
                    if self.expand_tabs:
                        line = line.expandtabs()
                    wrapped_lines.append(line[1:-1])
                else:
                    wrapped_lines.append('')
            else:
                wrapped_lines.extend(wrapper(self, line))
        return wrapped_lines