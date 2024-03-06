from source.programming_languages.pl import PL
from source.covid.covid import Covid

def mainfunc():
    learnSize = 0.7
    pl = PL("./datasets/programming languages.csv", learnSize)
    curlang = 'Rust'
    pl.analyzeLanguage(curlang) 
    # cv = Covid("./datasets/covid_clear.csv", learnSize, False)
    # cv.makePredictions('ill_cnt')

if __name__ == '__main__':
    mainfunc()