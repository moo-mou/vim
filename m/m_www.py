import os

from m_base import Base
from util import (
    get_config_yml,
    setup,
)


class WWW(Base):
    def __init__(self):
        super(WWW, self).__init__([
            'jinja2',
        ])

    @setup
    def compile_template(self):
        '''Find jinja2 template and build by using var in config.yaml'''
        jinja2 = self._modules['jinja2']

        config = get_config_yml()
        compile_config = config['compile']

        loader = jinja2.FileSystemLoader(
            './%s' % compile_config['src_dir'], followlinks=True)
        env = jinja2.Environment(loader=loader)

        for temp_name in env.list_templates(
            filter_func=lambda x: not x.startswith(
                '_') and x.endswith(compile_config['ext'])
        ):
            print('Compiling %s...' % temp_name)
            temp = env.get_template(temp_name)

            out_dir = compile_config['out_dir']

            with open('./%s/%s' % (out_dir, temp_name), 'w') as f:
                context = config.get('context', {})
                context['filename'] = os.path.splitext(
                    os.path.basename(temp_name))[0]
                f.write(temp.render(**context).encode('utf-8'))
