#!/bin/bash

grep --include=\*.{scss,js} --color -rnw ' $' ./assets
grep --color -rnw ' $' ./templates
