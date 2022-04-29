from distutils.core import setup, Extension

MOD = 'LiuB_mod'
setup(  name = MOD,
        version = '0.1',
        description= 'Branch_methon',
        author = '',
        author_email = '',
        ext_modules = [Extension( MOD,
                                sources = ['Branch_Core.c'],
                                extra_link_args = ['-lssl','-lcrypto'],
                                extra_compile_args = ['--std=c99','-w']
                                )
                                ]
    )
