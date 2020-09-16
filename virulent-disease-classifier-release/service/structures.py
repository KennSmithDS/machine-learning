# base nucleotides
nucleotides = ["A", "T", "C", "G"]

# nucleotides coded as placeholders for uncertain sequences
uncertainties = ['W', 'U', 'S', 'M', 'K', 'R', 'Y', 'B', 'D', 'H', 'V', 'N', 'Z']

# all possible protein letters
proteins = ['A','D','E','G','F','L','S','Y','C','W','L','P','H','Q','R','I','M','T','N','K','S','R','V']

# complement dictionary for reverse translation
complements = {"A": "T", "T": "A", "G": "C", "C": "G"}

# name lookup of amino acids
amino_acids = {
    'alanine': 'A', 'arginine': 'R', 'Asparagine': 'N', 'Aspartic Acid': 'D',
    'Cysteine': 'C', 'Glutamic Acid': 'E', 'Glutamine': 'Q',
    'Glycine': 'G', 'Histidine': 'H', 'Isoleucine': 'I', 'Leucine': 'L',
    'Lysine': 'K', 'Methionine': 'M', 'Phenylalanine': 'F', 'Proline': 'P',
    'Serine': 'S', 'Threonine': 'T', 'Tryptophan': 'W', 'Tyrosine': 'Y',
    'Valine': 'V'
}

# https://web.expasy.org/protscale/pscale/Hphob.Doolittle.html
hydropathicity = {
    "A":  1.800,"R": -4.500,"N": -3.500,"D": -3.500,"C":  2.500,
    "E": -3.500,"Q": -3.500,"G": -0.400,"H": -3.200,"I":  4.500,
    "L":  3.800,"K": -3.900,"M":  1.900,"F":  2.800,"P": -1.600,
    "S": -0.800,"T": -0.700,"W": -0.900,"Y": -1.300,"V":  4.200
}

# using mRNA in lookup, not tRNA anti-codon
start_codons = ["ATG"]
stop_codons = ["TAA", "TAG", "TGA"]

dna_codons = {
    # 'M' - START, '_' - STOP
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TGT": "C", "TGC": "C",
    "GAT": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "TTT": "F", "TTC": "F",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAT": "H", "CAC": "H",
    "ATA": "I", "ATT": "I", "ATC": "I",
    "AAA": "K", "AAG": "K",
    "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATG": "M",
    "AAT": "N", "AAC": "N",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TGG": "W",
    "": "X",
    "TAT": "Y", "TAC": "Y",
    "TAA": "_", "TAG": "_", "TGA": "_"
}

rna_codons = {
    # 'M' - START, '_' - STOP
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "UGU": "C", "UGC": "C",
    "GAU": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",
    "UUU": "F", "UUC": "F",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    "CAU": "H", "CAC": "H",
    "AUA": "I", "AUU": "I", "AUC": "I",
    "AAA": "K", "AAG": "K",
    "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "AUG": "M",
    "AAU": "N", "AAC": "N",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S", "AGU": "S", "AGC": "S",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "UGG": "W",
    "UAU": "Y", "UAC": "Y",
    "UAA": "_", "UAG": "_", "UGA": "_"
}