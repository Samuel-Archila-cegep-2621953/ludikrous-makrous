py -m nuitka --mode=standalone --include-data-dir=../src/client/ressources=ressources --windows-icon-from-ico=../src/client/ressources/logo.ico --windows-console-mode=disable --zig --output-filename=client-makrous.exe --output-folder-name=client-build --include-package=ursina --include-package=panda3d --include-package=direct --include-package-data=ursina --include-package-data=panda3d --follow-imports ../src/client/__main__.py
cp ../src/client/config.json client-build.dist/
REM cp ../src/client/serveur.db serveur-build.dist/
cp ../LICENSE client-build.dist/
tar.exe acvf client-standalone.zip client-build.dist/*
