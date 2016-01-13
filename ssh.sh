#!/bin/bash

if [[ $(who am i) =~ \([-a-zA-Z0-9\.]+\)$ ]] ; then echo -n y; else echo -n n; fi

