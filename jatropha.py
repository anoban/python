with open(r"C:\Users\Anoban\Documents\cmv\data\BLAST\compiled-aligned.fasta", mode = 'r') as fp:
    fasta: str = fp.read()

firsts: list[str] = [line for line in fasta.splitlines() if line.startswith('>')]
accessions: list[str]  = [line.split('|')[0].replace('>', '') for line in firsts]

# print(accessions)

new: str = ""

for acc in accessions:
    try:
        with open(fr"C:\Users\Anoban\Documents\cmv\data\BLAST\blastseqs\{acc}.fasta", mode = 'r') as fp:
            new += fp.read()
            new += "\n\n"
    except FileNotFoundError as fnferr:
        print(f"FileNotFoundError {fnferr}!")
        
# print(new)

with open(r"C:\Users\Anoban\Documents\cmv\data\final\jatropha.fasta", mode = 'a') as fp:
    fp.write(new)
