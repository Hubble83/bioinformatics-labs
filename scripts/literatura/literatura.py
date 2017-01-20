from Bio import Entrez
from Bio import Medline

Entrez.email = "mariovianaferreira@gmail.com"
handle = Entrez.egquery(term = "Legionella  pneumophila")
record = Entrez.read(handle)


for row in record["eGQueryResult"]:
    if row["DbName"]=="pubmed":
        y = row["Count"]


handle = Entrez.esearch(db = "pubmed", term = "Legionella  pneumophila", retmax=y)
record = Entrez.read(handle)
idlist = record["IdList"]


handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
records = list(Medline.parse(handle))
record_results = open('res_lit.txt', 'w')
for record in records:
    tit=('Title: ', record.get('TI', '?'))
    aut=('Authors: ', record.get('AU', '?'))
    sour=('Source: ', record.get('SO', '?'))

    record_results.write(str(tit))
    record_results.write("\n")
    record_results.write(str(aut))
    record_results.write("\n")
    record_results.write(str(sour))
    record_results.write("\n")
record_results.close()
