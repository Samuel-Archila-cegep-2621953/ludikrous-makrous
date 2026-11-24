py -m nuitka --mode=standalone --windows-icon-from-ico=../src/client/ressources/logo.ico --zig --output-filename=serveur-makrous.exe --output-folder-name=serveur-build --include-package=psutil --include-package=customtkinter --include-package=CTkListbox --include-package-data=psutil --include-package-data=customtkinter --include-package-data=CTkListbox  --follow-imports ../src/serveur/__main__.py
py -m nuitka --onefile --zig ../src/serveur/fermeture_serveur.py

cp fermeture_serveur.exe serveur-build.dist/
cp ../src/serveur/config.toml serveur-build.dist/
cp ../src/serveur/serveur.db serveur-build.dist/
cp ../src/serveur/fermeture_serveur.py serveur-build.dist/
cp ../LICENSE serveur-build.dist/
tar.exe acvf serveur-standalone.zip serveur-build.dist/*
