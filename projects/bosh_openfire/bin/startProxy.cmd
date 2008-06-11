set GRINDERPATH=D:\gsoc\bosh_loadtest\engine\grinder-3.0.1
set CLASSPATH=%GRINDERPATH%\lib\grinder.jar;%CLASSPATH%
rem Problematic with jdk 1.5 
set JAVA_HOME=C:\Program Files\Java\j2re1.4.2_17
PATH=%JAVA_HOME%\bin;%PATH%
java -cp %CLASSPATH% net.grinder.TCPProxy -console -http > ..\tests\grinder.py
