from py2exe import freeze

scripts = ['QMain.py']

libraries = ['AcaCrawler.py', 'Graphicrawl.py']

data_files = [('.', libraries)]

setup(windows=scripts, data_files=data_files)