#!/usr/bin/bash
[ -z "$1" ] && nitrogen --random --set-zoom-fill --save
SCRIPT_DIR="$(dirname $(readlink -f ${BASH_SOURCE}))"
cd $SCRIPT_DIR
CURRENT_PAPER="$(grep  "file" $HOME/.config/nitrogen/bg-saved.cfg | sed 's/file=//')"
COLOR_BIN="$SCRIPT_DIR/kmeans-colors/kmeans-ansi-palette"
COLOR_FILE="$HOME/.config/kitty/color.conf"
XRESC_FILE="$SCRIPT_DIR/Xresources"


convert "$CURRENT_PAPER" -resize 384x216 input.png
$COLOR_BIN -m ${1:-10} -t 4 input.png -o output.png \
    | grep \# | awk '{print "color" $0}' \
    > "$COLOR_FILE"
    
cat $COLOR_FILE | grep color | awk '{print "*" $1 ": " $2}' > $XRESC_FILE
    
printf "foreground\t$(cat $COLOR_FILE | grep color15 | cut -f 2)\n" | tee -a $COLOR_FILE | awk '{print "*" $1 ": " $2}' >> $XRESC_FILE
printf "background\t$(cat $COLOR_FILE | grep color0 | cut -f 2)\n" | tee -a $COLOR_FILE | awk '{print "*" $1 ": " $2}' >> $XRESC_FILE

kitty @ --to=unix:/tmp/.kitty set-colors --all --configured "$COLOR_FILE"
xrdb -merge $XRESC_FILE
# rm input.png output.png

: '
function luminanace(r, g, b) {
    var a = [r, g, b].map(function (v) {
        v /= 255;
        return v <= 0.03928
            ? v / 12.92
            : Math.pow( (v + 0.055) / 1.055, 2.4 );
    });
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}
function contrast(rgb1, rgb2) {
    return (luminanace(rgb1[0], rgb1[1], rgb1[2]) + 0.05)
         / (luminanace(rgb2[0], rgb2[1], rgb2[2]) + 0.05);
}
contrast([255, 255, 255], [255, 255, 0]); // 1.074 for yellow
contrast([255, 255, 255], [0, 0, 255]); // 8.592 for blue
// minimal recommended contrast ratio is 4.5, or 3 for larger font-sizesz
'