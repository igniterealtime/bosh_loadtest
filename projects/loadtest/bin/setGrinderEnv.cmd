set GRINDERPATH=D:\gsoc\bosh_loadtest\engine\grinder-3.0.1
set JAVA_HOME=C:\Program Files\Java\jdk1.5.0_15

set GRINDERPROPERTIES=%GRINDERPATH%\..\..\projects\loadtest\etc\grinder.properties
set CLASSPATH=%GRINDERPATH%\lib\grinder.jar;%CLASSPATH%
set CLASSPATH=%GRINDERPATH%\..\..\lib\xercesImpl.jar;%CLASSPATH%
PATH=%JAVA_HOME%\bin;%PATH%
