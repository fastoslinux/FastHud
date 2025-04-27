pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'fasthudgtk4devel')
gnome = import('gnome')

gnome.compile_resources('fasthudgtk4devel',
  'fasthudgtk4devel.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())  # Corrigido aqui
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'fasthudgtk4devel.in',
  output: 'fasthudgtk4devel',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

fasthudgtk4devel_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(fasthudgtk4devel_sources, install_dir: moduledir)
