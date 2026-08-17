#!/usr/bin/env bash

montage render/*.png -tile x1 -geometry +0+0 -background transparent "${PWD##*/}.png"
echo "done!"
