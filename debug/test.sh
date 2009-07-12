echo "GIME Diagnostics script v1.0"
echo "(c) 2009 by ExeGames.PL & Serenity.org.pl"

echo "-- BEGIN --\n\n\n" > $1
echo "-- glxgears windowed --\n\n\n" >> $1

echo "Benchmarking & testing stage..."
echo "GLX Gears in window, 1/2 in stage"
echo "After few (5-20) seconds press ESCAPE"

glxgears >> $1

echo "\n\n\n-- glxgears windowed END: $? --" >> $1
echo "-- glxgears fullscreen --\n\n\n" >> $1

echo "GLX Gears on fullscreen, 2/2 in stage"
echo "After few (5-20) seconds press ESCAPE"


glxgears -fullscreen >> $1

echo "\n\n\n-- glxgears fullscreen END: $? --" >> $1
echo "Collecting GL technical informations."
echo "-- glxinfo --\n\n\n" >> $1
glxinfo >> $1
echo "\n\n\n-- glxinfo END: $? --" >> $1

echo "After few seconds press ESCAPE"
echo "-- glxheads --\n\n\n" >> $1
glxheads :0 >> $1
echo "\n\n\n-- glxheads END: $? --" >> $1

WINEVER=`wine --version`
echo "wine --version: $WINEVER \n" >> $1

python --version >> $1 2>>$1
echo "-- END --" >> $1

echo "All collected, please send $1 to GIME Developers"
