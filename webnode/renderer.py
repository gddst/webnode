import gettext
import json

from jinja2 import Environment , FileSystemLoader

import webnode

class Renderer( object ):
    """
    Support list:
    1, jinja2
    """
    
    @staticmethod
    def render(template_name , **params ):

        """
        Provide a universal method for web page generating.
        All the template local parameter should be provided by "**params"
        """
        template_dir = params.get('template_dir',webnode.config.get('template_dir'))

        jinja2_env = Environment(
                                 loader=FileSystemLoader(template_dir),
                                 extensions=['jinja2.ext.i18n'])
        
        locale_dir=webnode.config.get('locale_dir')
        lang=params.get('lang','zh_CN')
        jinja2_env.install_gettext_translations(
            gettext.translation('site', locale_dir, languages=[lang]))   
        template = jinja2_env.get_template( '%s.jinja2' % template_name )

        jinjia2_ext={
            "jsondumps":json.dumps
        }
        
        return template.render(
            params,
            ext=jinjia2_ext,
            public_root='/public'
        )