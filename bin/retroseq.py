import sys
import os

#ugly bwa adapter for retroseq
ME_fasta=sys.argv[1]
candidate_fasta=sys.argv[2]
anchors=sys.argv[3]
prefix=sys.argv[3].split(".")[0]

anchor_structure={}
chromosomes=[]
for line in open(anchors):
    content=line.strip().split("\t")
    if not content[0] in chromosomes:
        chromosomes.append(content[0])

    anchor_structure[ content[3] ]={"chr":content[0],"start":content[1],"end":content[2],"orientation":content[4]}

os.system("bwa index {}".format(ME_fasta))
os.system("bwa mem {} {} > {}.bwamem.sam".format(ME_fasta,candidate_fasta,prefix))
entries={}
for chromosome in chromosomes:
    entries[chromosome]=[]

for line in open("{}.bwamem.sam".format(prefix)):
    content=line.strip().split("\t")
    if line[0] == "@":
        continue
    if content[0] in anchor_structure:
        flag="{0:012b}".format(int(content[1]))
        if not int(flag[-3]):
            orientation = "+"
            quality = "90.00"
            ME_id=content[2]
            mapq=int(content[4])
            if 10 > mapq:
                continue
            if int(flag[-5]) :
                orientation="-"
            entries[anchor_structure[content[0]]["chr"]].append([anchor_structure[content[0]]["chr"],int(anchor_structure[content[0]]["start"]),anchor_structure[content[0]]["end"],ME_id,content[0],anchor_structure[content[0]]["orientation"],orientation,quality])

for chromosome in chromosomes:
    entries[chromosome].sort(key=lambda x: x[1])

for chromosome in chromosomes:
    for entry in entries[chromosome]:
        print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6],entry[7])
