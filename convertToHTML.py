f = open("ProteinTable.txt", "r")
geneFile = open("scriptGene.html", "w")
CDSFile = open ("scriptProtein.html", "w")

data = f.readlines()
nlines = len(data)

accession = data[0].split("|")[1]
ln=1
ng,np=1,1
strand=""
curr=""

locus_tag = ""
gene = ""
db_xref = ""

uniprot_id = ""
revision = ""
protein_id = ""
product = ""
num_aa = ""
location = ""
function = ""

while ln < nlines:
	line = data[ln]
	ln+=1

	if line[0] not in "\t\n" or ln==nlines:
		if curr=="gene":
			geneFile.write("<td>"+strand+"</td>")
			geneFile.write("<td>"+locus_tag+"</td>")
			geneFile.write("<td>"+db_xref+"</td>")
			geneFile.write("<td>"+accession+"</td>")
			if gene!="": geneFile.write("<td>"+gene+"</td>")
			else: geneFile.write("<td>"+locus_tag+"</td>")
			geneFile.write("</tr>\n")

		elif curr=="CDS":
			CDSFile.write("<td>"+strand+"</td>")
			CDSFile.write("<td>"+uniprot_id+"</td>")
			CDSFile.write("<td>"+revision+"</td>")
			CDSFile.write("<td>"+protein_id+"</td>")
			CDSFile.write("<td>"+product+"</td>")
			CDSFile.write("<td>"+num_aa+"</td>")
			CDSFile.write("<td>"+location+"</td>")
			CDSFile.write("<td>"+function+"</td>")
			CDSFile.write("</tr>\n")

		if ln < nlines:
			lst = line.strip().split("\t")
			
			if lst[2]=="gene":

				if (ng%2==0): geneFile.write("<tr class='even' role='row'>")
				else: geneFile.write("<tr class='odd' role='row'>")
				ng+=1
				curr="gene"
				strand=lst[0]+".."+lst[1]
				locus_tag = ""
				gene = ""
				db_xref = ""
			
			elif lst[2]=="CDS":

				if (np%2==0): CDSFile.write("<tr class='even' role='row'>")
				else: CDSFile.write("<tr class='odd' role='row'>")
				np+=1
				curr="CDS"
				uniprot_id = ""
				revision = ""
				protein_id = ""
				product = ""
				num_aa = ""
				location = ""
				function = ""

			else: curr=""

	elif line[0]=="\t":
		if curr=="gene":
			if "locus_tag" in line: locus_tag = line.strip().split("\t")[1]
			if "db_xref" in line: db_xref = line.strip().split("\t")[1][7:]
			if "gene" in line: gene = line.strip().split("\t")[1]

		elif curr=="CDS":
			if "protein_id" in line: protein_id=line.strip().split("|")[1]
			if "product" in line: product=line.strip()[8:]
			if "function" in line: function=line.strip().split("\t")[1]
