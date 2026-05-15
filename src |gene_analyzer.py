"""
Gene Analysis Module for AMR, Virulence, and Essential Gene Detection
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class GeneAnalyzer:
    """Comprehensive gene analysis for AMR, virulence, and essential genes"""
    
    def __init__(self, data_dir: Path = None):
        """
        Initialize the gene analyzer with required databases
        
        Parameters:
        -----------
        data_dir : Path
            Directory containing database files
        """
        if data_dir is None:
            data_dir = Path.cwd()
        
        self.data_dir = data_dir
        self.essential_genes = set()
        self.amr_hits = None
        self.vfdb_hits = None
        self._load_databases()
    
    def _load_databases(self):
        """Load all required databases"""
        print("Loading essential genes...")
        essential_df = pd.read_excel(self.data_dir / "Essential_genes.xls", sheet_name=0, header=0)
        for _, row in essential_df.iterrows():
            if len(row) > 2 and pd.notna(row.iloc[2]):
                self.essential_genes.add(str(row.iloc[2]).strip().lower())
        
        print("Loading AMR hits...")
        with open(self.data_dir / "amr_resfinder.tab", 'r') as f:
            lines = f.readlines()
        header_idx = next((i for i, line in enumerate(lines) if 'GENE' in line), None)
        if header_idx:
            self.amr_hits = pd.read_csv(self.data_dir / "amr_resfinder.tab", sep='\t', skiprows=header_idx)
            if 'GENE' in self.amr_hits.columns:
                self.amr_hits['gene_lower'] = self.amr_hits['GENE'].fillna('').astype(str).str.lower()
        
        print("Loading VFDB hits...")
        with open(self.data_dir / "virulence_vfdb.tab", 'r') as f:
            lines = f.readlines()
        header_idx = next((i for i, line in enumerate(lines) if 'GENE' in line), None)
        if header_idx:
            self.vfdb_hits = pd.read_csv(self.data_dir / "virulence_vfdb.tab", sep='\t', skiprows=header_idx)
            if 'GENE' in self.vfdb_hits.columns:
                self.vfdb_hits['gene_lower'] = self.vfdb_hits['GENE'].fillna('').astype(str).str.lower()
        
        print("✓ Databases loaded successfully")
    
    def normalize_gene_name(self, gene: str) -> str:
        """Normalize gene name for consistent lookup"""
        return gene.strip().lower().replace('_', '').replace('-', '')
    
    def is_essential(self, gene: str) -> bool:
        """Check if a gene is essential"""
        return self.normalize_gene_name(gene) in self.essential_genes
    
    def get_amr_hits(self, gene: str) -> pd.DataFrame:
        """Get AMR hits for a gene"""
        if self.amr_hits is None:
            return pd.DataFrame()
        gene_norm = self.normalize_gene_name(gene)
        return self.amr_hits[self.amr_hits['gene_lower'] == gene_norm]
    
    def get_vfdb_hits(self, gene: str) -> pd.DataFrame:
        """Get VFDB hits for a gene"""
        if self.vfdb_hits is None:
            return pd.DataFrame()
        gene_norm = self.normalize_gene_name(gene)
        return self.vfdb_hits[self.vfdb_hits['gene_lower'] == gene_norm]
    
    def analyze(self, gene: str) -> Dict:
        """
        Comprehensive analysis of a gene
        
        Returns:
        --------
        dict with keys: query, essential, amr_count, vfdb_count, 
                        max_identity, confidence, organisms, products
        """
        amr_hits = self.get_amr_hits(gene)
        vfdb_hits = self.get_vfdb_hits(gene)
        
        # Extract organisms from products
        organisms = set()
        products = []
        for _, hit in amr_hits.iterrows():
            product = str(hit.get('PRODUCT', ''))
            products.append(product)
            # Extract organism from brackets
            import re
            match = re.search(r'\[([^\]]+)\]', product)
            if match:
                org = match.group(1).split()[0] + ' ' + match.group(1).split()[1] if len(match.group(1).split()) > 1 else match.group(1)
                organisms.add(org)
        
        # Calculate max identity
        max_identity = 0
        for _, hit in amr_hits.iterrows():
            try:
                ident = float(hit.get('%IDENTITY', 0))
                max_identity = max(max_identity, ident)
            except:
                pass
        
        # Calculate confidence score
        confidence = 0.4 if self.is_essential(gene) else 0
        confidence += 0.3 if len(amr_hits) > 0 else 0
        confidence += 0.2 if len(vfdb_hits) > 0 else 0
        confidence += 0.1 if len(organisms) > 0 else 0
        confidence = min(confidence, 1.0)
        
        return {
            'query': gene,
            'essential': self.is_essential(gene),
            'amr_count': len(amr_hits),
            'vfdb_count': len(vfdb_hits),
            'max_identity': max_identity,
            'confidence': confidence,
            'organisms': list(organisms),
            'products': products[:5]
        }


def analyze_gene(gene: str, data_dir: Path = None) -> Dict:
    """Convenience function for single gene analysis"""
    analyzer = GeneAnalyzer(data_dir)
    return analyzer.analyze(gene)
