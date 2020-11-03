import structures
from structures import proteins, nucleotides, dna_codons
import os, sys, traceback
import pandas as pd
import numpy as np
import csv

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.Alphabet import generic_dna

class Virus:

    def __init__(self):
        self.id = [] # accession id, searchable on NCBI
        self.description = [] # text description of strain
        self.gc_content = []
        self.amino_acid_dict = [] # ratio of amino acids in strain
        self.molecular_weight = [] # molecular weight
        self.aromaticity = [] # aromaticity
        self.instability_index = [] # instability index, > 40 means unstable / short half life .instability_index()
        self.nucleotide_sequence = [] # nuleotide sequence
        self.protein_sequence = [] # translated protein sequence

    def validate_sequence(self, seq):
        """
        Validates if input sequence is a valid sequence only made of base nucleotides.
        Returns False if sequences contains letter not in ('A', 'C', 'T', 'G').

        Keyword arguments:
        seq -- uploaded string input
        """

        tmp_seq = seq.upper()
        for nuc in tmp_seq:
            if nuc not in structures.nucleotides:
                return False
        return True

    def translate_nucleotides(self, seq):
        """
        Returns clean sequence assuming generic dna structure, filtering proteins not in valid list.

        Keyword arguments:
        seq -- valid string sequence
        """

        try:
            seq = Seq(seq, generic_dna)
            translated_seq = str(seq.translate()).replace('*', '')
            clean_seq = ''.join([p for p in translated_seq if p in structures.proteins])
            return clean_seq

        except Exception as e:
            print('-'*80)
            print(f"Exception in translating nucleotides: {e}")
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def calculate_gc_content(self, gc_seq):
        """
        Returns count of 'C' plus count of 'G' divided by valid sequence length.

        Keyword arguments:
        seq -- valid string sequence
        """

        return round((gc_seq.count("C") + gc_seq.count("G")) / len(gc_seq) * 100, 3)

    def parse_nuc_sequence(self, n_seq, id=None, desc=None):
        """
        Parses valid RNA sequence, translates nucleotides, calculates GC content and other methods available from ProteinAnalysis() in BioPython module.

        Keyword arguments:
        seq -- valid string sequence
        id -- id obtained from FASTA file record (default None)
        desc -- description obtained from FASTA file record (default None)
        """

        try:
            # append fasta sequence metadata
            self.id.append(id)
            self.description.append(desc)
            self.nucleotide_sequence.append(n_seq)
    
            # translate nucleotide string sequence
            p_seq = self.translate_nucleotides(n_seq)
            self.protein_sequence.append(p_seq)
            # self.protein_sequence.append(str(record.seq.translate()).replace('*', ' '))
            
            # GC content
            self.gc_content.append(self.calculate_gc_content(n_seq))
            
            # protein analysis methods
            analysis = ProteinAnalysis(p_seq)
            self.amino_acid_dict.append(analysis.get_amino_acids_percent())
            self.molecular_weight.append(analysis.molecular_weight())
            self.instability_index.append(analysis.instability_index())
            self.aromaticity.append(analysis.aromaticity())            

        except Exception as e:
            print('-'*80)
            print(f"Exception in parsing uploaded virus sequence: {e}")
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def parse_pro_sequence(self, p_seq, id=None, desc=None):
        try:
            p_seq = ''.join([pro for pro in p_seq if pro in proteins])

            # append fasta sequence metadata
            self.id.append(id)
            self.description.append(desc)

            # reverse translate protein to nucleotide sequence
            n_seq = ''.join([list(dna_codons.keys())[list(dna_codons.values()).index(pro)] for pro in p_seq])
            self.nucleotide_sequence.append(n_seq)
    
            self.protein_sequence.append(p_seq)
            # self.protein_sequence.append(str(record.seq.translate()).replace('*', ' '))
            
            # GC content
            self.gc_content.append(self.calculate_gc_content(n_seq))
            
            # protein analysis methods
            analysis = ProteinAnalysis(p_seq)
            self.amino_acid_dict.append(analysis.get_amino_acids_percent())
            self.molecular_weight.append(analysis.molecular_weight())
            self.instability_index.append(analysis.instability_index())
            self.aromaticity.append(analysis.aromaticity())

        except Exception as e:
            print('-'*80)
            print(f"Exception in parsing uploaded virus sequence: {e}")
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def expand_amino_acids(self, vdf):
        """
        Returns dataframe object after expanding amino acid percents into distinctive columns from dictionary structure.

        Keyword arguments:
        vdf -- virus dataframe constructed after parsing valid sequence
        """

        try:
            amino_acids_percent_df = vdf['amino_acid_percents'].apply(pd.Series)
            amino_acids_percent_df = amino_acids_percent_df.rename(columns = lambda x : 'amino_acid_' + str(x))
            new_vdf = pd.concat([vdf, amino_acids_percent_df], axis=1)
            new_vdf.drop('amino_acid_percents', axis=1, inplace=True)
            return new_vdf

        except Exception as e:
            print('-'*80)
            print(f"Exception in expanding amino acid percent dictionary: {e}")
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def build_virus_dataframe(self, sequence_upload, sequence_type, upload_type,is_file):
        """
        Takes input of sequence text or fasta file from the UI, and iteratively checks if sequences are valid to proceed with parsing or ignoring each record.
        Returns a dataframe object with a row for each record in the uploaded sequence(s).

        Keyword arguments:
        sequence_upload -- the user submitted virus data, in either text or fasta file format
        upload_type -- call for upload type from UI depending on how user submits the virus data
        """

        try:
            # handle text upload
            if upload_type == 'text' and not is_file:
                # split uploaded test on $ if mulitple sequences
                for str_seq in sequence_upload.split('$'):
                    if sequence_type == 'nucleotide':
                        # parse nucleotide sequence if only contains valid base nucleotides
                        if self.validate_sequence(str_seq):
                            self.parse_nuc_sequence(str_seq)
                    elif sequence_type == 'protein':
                        self.parse_pro_sequence(str_seq)
            #handle csv file 
            elif upload_type == 'csv' and is_file:
                # split uploaded test on , if mulitple sequences
                csv_reader = csv.reader(sequence_upload, delimiter=',')
                for row in csv_reader:
                    if sequence_type == 'nucleotide':
                        # parse nucleotide sequence if only contains valid base nucleotides
                        if self.validate_sequence(row[0]):
                            self.parse_nuc_sequence(row[0])
                    elif sequence_type == 'protein':
                        self.parse_pro_sequence(row[0])
            # handle fasta file upload
            elif upload_type == 'fasta' and is_file:
                for sequence in list(SeqIO.parse(sequence_upload, 'fasta')):
                    # convert fasta sequence object to string
                    str_seq = str(sequence.seq)
                    id = sequence.id
                    desc = sequence.description
                    if sequence_type == 'nucleotide':
                        # parse nucleotide sequence if only contains valid base nucleotides
                        if self.validate_sequence(str_seq):
                            self.parse_nuc_sequence(str_seq, id, desc)
                    elif sequence_type == 'protein':
                        self.parse_pro_sequence(str_seq, id, desc)
            
            # handle base case
            else:
                return None

            comp_aa_df = pd.DataFrame({
                "id": self.id,
                "description": self.description,
                "gc_content": self.gc_content,
                "amino_acid_percents": self.amino_acid_dict,
                "molecular_weight": self.molecular_weight,
                "aromaticity": self.aromaticity,
                "instability_index": self.instability_index,
                "nucleotide_sequence": self.nucleotide_sequence,
                "protein_sequence": self.protein_sequence
            })

            comp_aa_df['sequence_length'] = comp_aa_df['nucleotide_sequence'].apply(lambda x: len(x))
            comp_aa_df['id'] = comp_aa_df['id'].fillna(comp_aa_df.index.to_series())
            comp_aa_df['description'] = comp_aa_df['description'].fillna("Unknown")

            return self.expand_amino_acids(comp_aa_df)
                    
        except Exception as e:
            print('-'*80)
            print(f"Exception in building virus datatframe: {e}")
            traceback.print_exc(file=sys.stdout)
            print('-'*80)