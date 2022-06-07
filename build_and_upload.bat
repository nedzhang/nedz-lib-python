@REM ***********************************************************
@REM This script builds and uploads python lib to testpypi
@REM ***********************************************************

echo off

@REM Read the token for pypi from file
set /p PYPI_TOKEN=<"secret/token.txt"

del /Q .\dist\*

python -m build

python -m twine upload --repository testpypi -u __token__ -p %PYPI_TOKEN% --verbose dist/* 

echo ****************************************************************************
echo *     Install the package with command below                               *
echo.
echo pip install --index-url https://test.pypi.org/simple/ --upgrade nedz_library
echo.
echo ****************************************************************************

echo on