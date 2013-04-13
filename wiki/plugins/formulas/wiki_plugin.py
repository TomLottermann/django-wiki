# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.images import views, models, settings, forms
from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title
from wiki.plugins.formulas.mdx.mdx_mathjax import MathJaxExtension

class FormulaPlugin(BasePlugin):
    
    slug = settings.SLUG
    # sidebar = {
    #     'headline': _('Images'),
    #     'icon_class': 'icon-picture',
    #     'template': 'wiki/plugins/images/sidebar.html',
    #     'form_class': forms.SidebarForm,
    #     'get_form_kwargs': (lambda a: {'instance': models.Image(article=a)})
    # }
    
    class RenderMedia:
        js = [
            'wiki/mathjax/markdownConfig.js',
            'wiki/mathjax/MathJax.js?config=default',
        ]
    
    markdown_extensions = [MathJaxExtension()]
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
registry.register(FormulaPlugin)

