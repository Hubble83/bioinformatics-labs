from Bio import Entrez, SeqIO
Entrez.email = "mariovianaferreira@gmail.com"
handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id="52840256", seq_start="2327101", seq_stop="2610800")
seq_record = SeqIO.read(handle, "genbank")
SeqIO.write(seq_record, 'seq_record.gb', "genbank") #Guarda em formato genbank
handle.close()

#gravar a sequencia num txt
Dfile= open('sequence.txt', 'w')
Dfile.write(str(seq_record.seq))
Dfile.close()

#Dados da proteina (Genbank)
print ("ID da proteina:\t", seq_record.id)
#print ("\nID (genbank): ", seq_record.annotations["gi"])
print ("Nome comum:\t", seq_record.description)
print ("Comprimento da Sequencia:\t", len(seq_record.seq))
#print ("\nSequencia:\t", seq_record.seq)
print ("CDS: Genes e localizacao das bases que codificam o gene: ")
print (seq_record.features[20])
print ("Fonte:", seq_record.features[0])
print ("Dados gerais: ",seq_record.features[1])
print ("Regioes de interesse: ",seq_record.features[2])
print ("Taxonomia: ", seq_record.annotations["taxonomy"])
print ("Referencias: ", seq_record.annotations["references"])
