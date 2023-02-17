@echo off
if "%~1"=="" (
  echo Please provide the name of the test case.
  exit /b
)

set name=%1
echo Creating files for %name% ...

echo Creating test_%name%.in ...
type nul > test_%name%.in

echo Creating test_%name%.out ...
type nul > test_%name%.out

echo Creating test_%name%.pysc ...
type nul > test_%name%.pysc

echo Files created successfully.
