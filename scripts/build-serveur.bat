py -m nuitka --mode=standalone --windows-icon-from-ico=../src/client/ressources/logo.ico --zig --output-filename=serveur-makrous.exe --include-package=psutil --include-package=customtkinter --include-package=CTkListbox --include-package-data=psutil --include-package-data=customtkinter --include-package-data=CTkListbox  --follow-imports ../src/serveur/__main__.py
cp src/serveur/config.toml src/serveur/__main__.dist/
cp src/serveur/serveur.db src/serveur/__main__.dist/
cp LICENSE src/serveur/__main__.dist/
Compress-Archive src/serveur/__main__.dist/* serveur-standalone.zip
