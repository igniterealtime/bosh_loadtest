#!/bin/bash
export GRINDERPATH=`pwd`"/../../../engine/grinder-3.0.1"
GRINDERPROPERTIES=`pwd`"/../etc/grinder.properties"
CLASSPATH=`pwd`"/../../../lib/xercesImpl.jar:$GRINDERPATH/lib/grinder.jar:$CLASSPATH"
java -cp $CLASSPATH -Dgrinder.agentID=$1 net.grinder.Grinder $GRINDERPROPERTIES