from source.utils.dataload import loadData
from source.programming_languages.pl import PL

def mainfunc():
    # set coefs here
    modelSize = 250
    learnSize = 158
    pl = PL("./datasets/programming languages.csv", [modelSize, learnSize])
    curlang = 'Rust'
    pl.analyzeLanguage(curlang)    

if __name__ == '__main__':
    mainfunc()