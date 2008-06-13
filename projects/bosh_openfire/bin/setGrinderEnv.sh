#!/bin/bash

export GRINDERPATH=`pwd`"/../../../engine/grinder-3.0.1"
export GRINDERPROPERTIES=`pwd`"/../etc/grinder.properties"
export CLASSPATH=`pwd`"/../../../lib/xercesImpl.jar:$GRINDERPATH/lib/grinder.jar:$CLASSPATH"
