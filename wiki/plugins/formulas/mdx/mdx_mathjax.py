from markdown import Extension
from markdown.preprocessors import Preprocessor
import re

# Global vars
MATHJAX_PATTERN_RE = re.compile( \
    r'(?P<fence>^\${2,})[ ]*(?P<formula>.*?)[ ]*(?P=fence)$',
    re.MULTILINE|re.DOTALL
    )

CLEAN_WRAP = '$$%s$$'

class MathJaxExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add MathJaxPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('mathjax_block',
                                 MathJaxPreprocessor(md),
                                 "_begin")


class MathJaxPreprocessor(Preprocessor):

    def run(self, lines):
        """ Match and store Fenced Formula Blocks in the HtmlStash. """

        text = "\n".join(lines)
        while 1:
            m = MATHJAX_PATTERN_RE.search(text)
            if m:
                forumla = self._escape(text[m.start():m.end()])

                # Mark formula as save
                placeholder = self.markdown.htmlStash.store(forumla, safe=True)
                text = '%s%s%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return MathJaxExtension(configs=configs)