from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# This collects all dynamically imported scrapy modules and data files.
hiddenimports = (collect_submodules('mesh_to_sdf')
)
datas = collect_data_files('mesh_to_sdf')