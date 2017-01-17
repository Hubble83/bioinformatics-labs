import os
from Bio import SeqIO
from Bio import Entrez

file = SeqIO.read("seq_record.gb", "genbank")

def sizeSequence(tamanho):
	i=0
	lista=[]
	x=[]
	resultado=[]
	for i in range (len(tamanho)):
		x=tamanho[i]
		lista.extend(x + '-')
		i+=1

	contador=0
	for i in range (len(lista)):
		if (lista[i]!='-'):
			contador+=1

		else:
			resultado.append(str(contador))
			contador=0

	return resultado

features_gene = {
	"GeneID":[],
	"Locus_tag":[],
	"Gene":[]
}

features_protein = {
	"Name":[],
	"Protein_id":[],
	"Size":[],
	"Function":[],
	"EC_number":[],
	"Location":[],
	"Sequence":[],
	"Note":[]
}

for feature in file.features:

	if feature.type == "gene":
		features_gene["GeneID"].append(feature.qualifiers["db_xref"][0])
		features_gene["Locus_tag"].append(feature.qualifiers["locus_tag"][0])
		try:
			features_gene["Gene"].append(feature.qualifiers["gene"][0])
		except:
			features_gene["Gene"].append("")

	if feature.type == "CDS":
		features_protein["Location"].append(feature.location)
		features_protein["Protein_id"].append(feature.qualifiers["protein_id"][0])
		features_protein["Sequence"].append(feature.qualifiers["translation"][0])
		features_protein["Size"] = sizeSequence(features_protein["Sequence"])
		features_protein["Name"].append(feature.qualifiers["product"][0])
		try:
			features_protein["Function"].append(feature.qualifiers["function"][0])
		except:
			features_protein["Function"].append("Function unknown")

		try:
			features_protein["EC_number"].append(feature.qualifiers["EC_number"][0])
		except:
			features_protein["EC_number"].append("")

		try:
			features_protein["Note"].append(feature.qualifiers["note"][0])
		except:
			features_protein["Note"].append("")

	if feature.type == "tRNA" or feature.type == "misc_feature":
		features_protein["Location"].append("")
		features_protein["Protein_id"].append("")
		features_protein["Sequence"].append("")
		features_protein["Size"] = 0
		features_protein["Name"].append("")
		features_protein["Function"].append("Function unknown")
		features_protein["EC_number"].append("")
		features_protein["Note"].append("")

ws = open("table.csv","w")
h = open("tableHTML.html", "w")

uniprot = open("uniprot.txt", "r").readlines()

ws.write('Locus Tag,'+'GeneID,'+'Gene Name,'+'Strand,'+'Uniprot ID,'+'Revision,'+'Accession Number Protein,'+'Protein Name,'+'#AA,'+'EC_Number,'+'Description\n')


for x in range(len(features_gene["GeneID"]) ):
	if(features_protein["Location"][x] != ""):
		start = features_protein["Location"][x].start + 1
		location = "[" + str( start ) + ":" + str( features_protein["Location"][x].end ) + "]"
	else :
		location = ""

	row=[]
	row.append(features_gene["Locus_tag"][x])
	row.append(features_gene["GeneID"][x][7:])
	row.append(features_gene["Gene"][x])
	if(features_protein["Location"][x] != ""):
		if features_protein["Location"][x].strand == 1: 
			row.append("+")
		else: row.append("-")
	else: row.append("")
	uni=uniprot[x].strip().split("\t")
	if len(uni) == 2:
		row.append(uni[0])
		row.append(uni[1])
	else:
		row.append("")
		row.append("")
	row.append(features_protein["Protein_id"][x])
	row.append(features_protein["Name"][x])
	row.append(features_protein["Size"][x])
	row.append(features_protein["EC_number"][x])
	row.append(features_protein["Function"][x])

	#geneId locus geneName strand UniportID Revision AccessionNCBI NAME #AA Location Description
	if (x%2==0): h.write("<tr class='odd' role='row'>")
	else: h.write("<tr class='even' role='row'>")

	for column in row:
		ws.write(column.replace(",",";")+",")
		h.write("<td>"+column+"</td>")

	ws.write("\n")
	h.write("</tr>\n")
	