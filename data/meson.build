# Copia o arquivo .desktop diretamente para o diretório de instalação
install_data('io.github.fastoslinux.fasthud.desktop.in',
             install_dir: join_paths(get_option('datadir'), 'applications'))

# Valida o arquivo .desktop usando desktop-file-validate
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: ['io.github.fastoslinux.fasthud.desktop'])
endif

# Instala o arquivo XML de metadados
install_data('io.github.fastoslinux.fasthud.appdata.xml.in',
             install_dir: join_paths(get_option('datadir'), 'appdata'))

# Valida o arquivo XML de metadados usando appstream-util (se disponível)
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', 'io.github.fastoslinux.fasthud.appdata.xml'])
endif

# Instala o arquivo de esquema gsettings
install_data('io.github.fastoslinux.fasthud.gschema.xml',
             install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas'))

# Valida o arquivo de esquema usando glib-compile-schemas (se disponível)
compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

# Continuação do seu arquivo meson.build...
subdir('icons')
