#!/usr/bin/bash
grep "file" $HOME/.config/nitrogen/bg-saved.cfg | sed 's/file=//'
