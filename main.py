from transformers import pipeline
import spacy
# from spacy.lang.pl.examples import sentences
from config.config import tagset, tagkey, tagother
from inferate import Inferator


def __main__():
    text = """W WIG20 to właśnie przedstawiciele tych dwóch sektorów zaliczyli największe spadki. Kurs LPP spadł o 6,66 proc., 
natomiast KGHM-u o 6,12 proc. O ile w przypadku LPP nie pojawiły się nowe informacje cenotwórcze, WIG20, WIG20, WIG20, WIG20
o tyle spadek ceny akcji KGHM-u można tłumaczyć sprzedażą faktów po publikacji raportu wynikowego."""
    
    # print(inferate(text))

    with open("./data/test/test_data.txt", "r") as f:
        text = f.read()
#     text = """Klienci PKO BP i jego internetowej marki Inteligo na utrudnienia powinni przygotować się w niedzielę (20 listopada). 
# Od godz. 0:00 do 12:00 nie będzie można korzystać z internetowego i telefonicznego serwisu iPKO i iPKO biznes, aplikacji iPKO biznes, funkcji Open Banking."""
    inferator = Inferator()
    print(inferator.inferate(text = text, translated = False))


if __name__ == '__main__':
    __main__()