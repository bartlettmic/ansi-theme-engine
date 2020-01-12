#!/usr/bin/bash
nitrogen --random --set-zoom-fill --save
SCRIPT_DIR="`dirname ${BASH_SOURCE}`"
cd $SCRIPT_DIR
CURRENT_PAPER="$(grep  "file" $HOME/.config/nitrogen/bg-saved.cfg | sed 's/file=//')"
COLOR_BIN="./image-segmentation/kmeans-ansi-palette"
COLOR_FILE="$HOME/.config/kitty/color.conf"
XRESC_FILE="$SCRIPT_DIR/Xresources"


convert "$CURRENT_PAPER" -resize 384x216 input.png
$COLOR_BIN -m ${1:-10} -t 4 input.png -o output.png \
    | grep \# | awk '{print "color" $0}' \
    > "$COLOR_FILE"
    
cat $COLOR_FILE | grep color | awk '{print "*" $1 ": " $2}' > $XRESC_FILE
xrdb -merge $XRESC_FILE
    
printf "foreground\t$(cat $COLOR_FILE | grep color15 | cut -f 2)\n" >> $COLOR_FILE
printf "background\t$(cat $COLOR_FILE | grep color0 | cut -f 2)\n" >> $COLOR_FILE

kitty @ --to=unix:/tmp/.kitty set-colors --all "$COLOR_FILE"

rm input.png output.png