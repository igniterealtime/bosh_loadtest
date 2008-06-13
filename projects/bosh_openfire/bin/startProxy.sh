#!/usr/bin/bash
./setGrinderEnv.sh
java -cp $CLASSPATH net.grinder.TCPProxy -console -http > ../tests/recorded.py