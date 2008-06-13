#!/bin/bash
./setGrinderEnv.sh
java -cp $CLASSPATH -Dgrinder.agentID=$1 net.grinder.Grinder $GRINDERPROPERTIES 