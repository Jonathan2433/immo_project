Utilisez sphinx pour générer dans un dossier “docs” votre documentation en HTML.
pip install sphinx
pip install sphinx-automodule
pip install sphinx-rtd-theme
pip install sphinx_autodoc_typehints
mkdir docs
(cd docs)
sphinx-quickstart
cd ..
sphinx-apidoc -o docs cashtools –ext-autodoc –private
cd docs
make html