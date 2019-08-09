import mistune


class CustomMistuneRenderer(mistune.Renderer):
    def image(self, src, title, alt_text):
        return "<img src='%s' title='%s' alt='%s' data-action='zoom'>" % (
            src, title, alt_text)
