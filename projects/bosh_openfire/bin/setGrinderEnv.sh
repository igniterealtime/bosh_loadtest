#!/bin/bash
GRINDERPATH=`pwd`/../../../engine/grinder-3.0.1
GRINDERPROPERTIES=`pwd`/../etc/grinder.properties
CLASSPATH=$GRINDERPATH/lib/grinder.jar:$CLASSPATH
CLASSPATH=`pwd`/../../../lib/xercesImpl.jar:$CLASSPATH
export CLASSPATH PATH GRINDERPROPERTIES