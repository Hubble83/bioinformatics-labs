from Bio import SeqIO

record = SeqIO.read("seq_record.gb", "genbank")

#RecolherFuncoes
funct=[]
for i in record.features:
    if i.type == "CDS":
        if 'function' in i.qualifiers:
            funct.append((i.qualifiers["locus_tag"][0],i.qualifiers["function"][0]))

#RecolherTraducao
trad=[]
for i in record.features:
    if i.type=="CDS":
        trad.append((i.qualifiers["locus_tag"][0],i.qualifiers["translation"][0]))

#ImprimirInformacaoRelevante
print ("Gene&Funcao:" + "\n")
print ("Genes com funcao definida: " + str(len(funct)))
print ("Genes com funcao desconhecida: " + str(213-len(funct))+ "\n")
for function in funct:
    print (function)
#print ("\n" + "Gene&Traducao:" + "\n")
#for translation in trad:
#    print (translation)
