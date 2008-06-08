call setGrinderEnv.cmd
echo %CLASSPATH%
java -cp %CLASSPATH% net.grinder.Grinder %GRINDERPROPERTIES%
