# Copia e instala o arquivo .desktop
desktop_file = configure_file(
    input: 'io.github.fastoslinux.fasthud.desktop.in',
    output: 'io.github.fastoslinux.fasthud.desktop',
    configuration: configuration_data(),
    install: true,
    install_dir: join_paths(get_option('datadir'), 'applications')
)

# Valida o arquivo .desktop usando desktop-file-validate
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
    test('Validate desktop file',
         desktop_utils,
         args: [desktop_file]
    )
endif

# Copia e instala o arquivo .metainfo.xml
metainfo_file = configure_file(
    input: 'io.github.fastoslinux.fasthud.metainfo.xml.in',
    output: 'io.github.fastoslinux.fasthud.metainfo.xml',
    configuration: configuration_data(),
    install: true,
    install_dir: join_paths(get_option('datadir'), 'metainfo')
)

# Valida o arquivo .metainfo.xml usando appstream-util (se disponível)
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
    test('Validate metainfo file',
         appstream_util,
         args: ['validate', metainfo_file]
    )
endif

# Instala o arquivo de esquema gsettings (o Meson compila o gschema automaticamente)
install_data('io.github.fastoslinux.fasthud.gschema.xml',
             install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas'))

# Valida o arquivo de esquema usando glib-compile-schemas (se disponível)
compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
    test('Validate schema file',
         compile_schemas,
         args: ['--strict', '--dry-run', meson.current_source_dir()]
    )
endif

subdir('icons')
