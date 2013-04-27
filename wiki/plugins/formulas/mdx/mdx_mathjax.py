from markdown import Extension
from markdown.preprocessors import Preprocessor
import re

import logging

# Global vars
MATHJAX_PATTERN_RE = re.compile( \
    r'(?P<nli>^\n?)\s*(?P<fence>\${2,})\s*(?P<formula>.*?)\s*(?P=fence)\s*?(?P<nlb>\n?)',
    re.MULTILINE|re.DOTALL
    )

CLEAN_MULTILINE_WRAP = '$$$%s$$$'

CLEAN_INLINE_WRAP = '$$%s$$'

logger = logging.getLogger(__name__)

class MathJaxExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add MathJaxPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('mathjax_block',
                                 MathJaxPreprocessor(md),
                                 "_begin")


class MathJaxPreprocessor(Preprocessor):

    def run(self, lines):
        """ Match and store Fenced Formula Blocks in the HtmlStash.
        Makes sure to make a difference between inline and multiline formulas. """
        text = "\n".join(lines)
        while 1:
            m = MATHJAX_PATTERN_RE.search(text)
            if m:
                formula = self._escape(m.group('formula'))
                nli = m.group('nli')
                nlb = m.group('nlb')

                if not (nli == '' or nlb == ''):
                    wrapped_formula = CLEAN_MULTILINE_WRAP % (formula, )
                else:
                    wrapped_formula = CLEAN_INLINE_WRAP % (formula, )

                # Mark formula as save
                placeholder = self.markdown.htmlStash.store(wrapped_formula, safe=True)
                text = '%s%s%s%s%s'% (text[:m.start()], nli, placeholder, nlb, text[m.end():])
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