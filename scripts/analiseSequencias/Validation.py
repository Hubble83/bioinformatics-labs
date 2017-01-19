from Bio import SeqIO

seq_record = SeqIO.read("seq_record.gb", "genbank")

featcds = []
featgene=[]
otherfeat=[]
for i in range(len(seq_record.features)):
    if seq_record.features[i].type == "CDS":
        featcds.append(i)
    elif (seq_record.features[i].type == "gene"):
        featgene.append(i)
    else:
        otherfeat.append(i)
    i=+1


f = open("ProteinTable1.txt", 'r')
table=[]
for line in f.readlines():
    table.append(line.split('\t'))
f.close()


cdsProteinID =[]
cdsGeneID =[]
for i in seq_record.features:
    if i.type == "CDS":
        cdsProteinID.append(i.qualifiers["protein_id"][0])
        cdsGeneID.append(i.qualifiers["db_xref"][0].strip("GeneID:"))

valido=True
for j in range (1,len(table)):
    if table[j][5] != cdsGeneID[j-1] or table[j][8] != cdsProteinID[j-1]:
        valido=False

print ("ANALISE DE FEATURES")
print ("\n" + "Number of CDS features: " + str(len(featcds)))
print ("Locations: " + str(featcds))
print ("Number of gene features: " + str(len(featgene)))
print ("Locations: " + str(featgene))
print ("Number of other features: " + str(len(otherfeat)))
print ("Locations: " + str(otherfeat))
print ("\n" + "VALIDACAO")
if valido:
    print ("Todas as features foram validadas!")
else:
    print ("Existem features invalidas!")
