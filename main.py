from source.programming_languages.pl import PL
from source.covid.covid import Covid

def mainfunc():
    # set coefs here
    modelSize = 250
    learnSize = 158
    newLearnSize = 0.7
    # pl = PL("./datasets/programming languages.csv", [modelSize, learnSize], newLearnSize)
    # curlang = 'Rust'
    # pl.analyzeLanguage(curlang) 
    cv = Covid("./datasets/covid.csv", 0.7)
    cv.makePredictions('ill_cnt')

if __name__ == '__main__':
    mainfunc()