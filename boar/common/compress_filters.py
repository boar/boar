import clevercss
from compressor.filters import FilterBase

class CleverCSSFilter(FilterBase):
    def input(self, **kwargs):
        if 'filename' in kwargs and kwargs['filename'].endswith('ccss'):
            return '@media screen {%s}' % clevercss.convert(self.content.replace('@media screen {', '')[:-1])
        return self.content
