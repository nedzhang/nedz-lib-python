del /Q .\dist\*

python -m build

python -m twine upload --repository testpypi -u __token__ -p pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX --verbose dist/* 

echo off

echo ****************************************************************************
echo *     Install the package with command below                               *
echo.
echo pip install --index-url https://test.pypi.org/simple/ --upgrade nedz_library
echo.
echo ****************************************************************************

echo on