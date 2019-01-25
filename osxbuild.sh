#!/bin/bash
ZONAAPP=dist/zona.app

source venv/bin/activate
python3 appbuild/plistbuild.py
PYTHONOPTIMIZE=2 pyinstaller maingame.py --noconsole
iconutil -c icns ./z.iconset
chmod 777 z.icns
mkdir dist/maingame.app/Contents/MacOS/game
cp -r game/character_set dist/maingame.app/Contents/MacOS/game/character_set
cp -r venv/lib/python3.6/site-packages/pyfiglet dist/maingame.app/Contents/MacOS/
cp -r game/data dist/maingame.app/Contents/MacOS/game/data
cp  z.icns dist/maingame.app/Contents/Resources/icon-windowed.icns
cp appbuild/Info.plist dist/maingame.app/Contents/Info.plist
rm appbuild/Info.plist
rm z.icns
if [ -d "$ZONAAPP" ]; 
then
   rm -rf $ZONAAPP
   echo "Deleted previous zona.app"
fi
mv dist/maingame.app $ZONAAPP
echo "Built dist/zona.app"
