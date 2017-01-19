from Bio import SwissProt
from Bio import SeqIO
from io import StringIO
import requests
from urllib.request import urlopen

#Obter os dados da proteína
def getDataFromProt(protid):
    #Ir buscar à net os ficheiros
    url = "http://www.uniprot.org/uniprot/" + protid + ".txt"
    txt = urlopen(url).read()
    #Criar um dat que possa ser tratado
    f = open("usable.dat", "w")
    f.write(txt.decode('utf-8'))
    f.close()
    handle = open("usable.dat")
    #Obter dados relevantes do txt
    parsed = SwissProt.read(handle)
    status, locale, fmol, bio, name, id, function, gname = getInfoTxt(parsed)
    return name, id, locale, status, fmol, bio, function, gname

#Obter dados relevantes do txt
def getInfoTxt(parsed):
    status = str(parsed.data_class)
    locale = ""
    aux = parsed.description
    aux = aux.split("=")
    aux = aux[1].split("{")
    name = aux[0]
    fmol = []
    function = ""
    bio = []
    id = str(parsed.entry_name)
    for cr in parsed.cross_references:
        if cr[0] == "GO":
            (type, ids, cl, pis) = cr
            if type == "GO":
                cls = str(cl).split(":")
                if cls[0] == 'F':
                    fmol.append(cls[1])
                if cls[0] == 'P':
                    bio.append(cls[1])
                if cls[0] == 'C':
                    locale = cls[1]
    for cr in parsed.comments:
        cr = str(cr).split(":")
        if cr[0] == "FUNCTION":
            function = cr[1].split("{")[0]
    aux = parsed.gene_name
    aux = aux.split("OrderedLocusNames=")[1]
    gname = aux.split(" ")[0]
    if function == "":
        function = "Unavailable"
    return status, locale, fmol, bio, name, id, function, gname

#Imprimir todos os dados selecionados do txt no ficheiro
def printProteinAnalysisAll():
    ids = []
    temp = "Unavailable"
    seq_record = SeqIO.read("seq_record.gb", "genbank")
    for feat in seq_record.features:
        if feat.type == 'CDS':
            ID_prot = feat.qualifiers["protein_id"][0]
            ids.append(ID_prot)
    file = open("protein_analysis_all.txt", "w")
    for protid in ids:
        params = {"query": protid, "format": "fasta"}
        frecord = requests.get("http://www.uniprot.org/uniprot/", params)
        for record in SeqIO.parse(StringIO(frecord.text), "fasta"):
            aux = record.id
            idfasta = str(aux).split("|")[1]
        name, id, locale, status, fmol, bio, function, gname = getDataFromProt(idfasta)
        file.write("\nLocus Name : " + gname)
        file.write("\nProtein Name : " + name)
        file.write("\nProtein ID : " + id)
        if locale == "":
            aux = temp
        else:
            aux = locale
        file.write("\nCellular Locale : " + aux)
        file.write("\nStatus : " + status)
        if str(bio) == "[]":
            aux = temp
        else:
            aux = str(bio)
        file.write("\nBiological Process : " + aux)
        if str(fmol) == "[]":
            aux = temp
        else:
            aux = str(fmol)
        file.write("\nMolecular Function : " + aux)
        file.write("\nFunction : " + function)
        file.write("\n")
    file.close()

printProteinAnalysisAll()
