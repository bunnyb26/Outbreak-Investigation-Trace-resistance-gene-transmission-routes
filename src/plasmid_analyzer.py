"""
Plasmid Analysis Module for IMGPR Plasmid Database
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List

class PlasmidAnalyzer:
    """Comprehensive plasmid analysis from IMGPR database"""
    
    def __init__(self, data_dir: Path = None):
        """Initialize plasmid analyzer with IMGPR data"""
        if data_dir is None:
            data_dir = Path.cwd()
        
        self.data_dir = data_dir
        self.plasmid_df = None
        self.plasmid_index = {}
        self._load_data()
    
    def _load_data(self):
        """Load IMGPR plasmid data"""
        plasmid_file = self.data_dir / "IMGPR_pladmid_data.tsv"
        if plasmid_file.exists():
            self.plasmid_df = pd.read_csv(plasmid_file, sep='\t')
            for _, row in self.plasmid_df.iterrows():
                pid = row.get('plasmid_id')
                if pd.notna(pid):
                    self.plasmid_index[str(pid)] = row.to_dict()
            print(f"✓ Loaded {len(self.plasmid_index)} plasmids")
        else:
            print(f"⚠️ Plasmid file not found: {plasmid_file}")
    
    def get_plasmid(self, plasmid_id: str) -> Optional[Dict]:
        """Get plasmid by ID"""
        return self.plasmid_index.get(str(plasmid_id))
    
    def search_by_organism(self, organism: str) -> pd.DataFrame:
        """Search plasmids by host organism"""
        if self.plasmid_df is None or 'host_taxonomy' not in self.plasmid_df.columns:
            return pd.DataFrame()
        
        mask = self.plasmid_df['host_taxonomy'].str.lower().str.contains(organism.lower(), na=False)
        return self.plasmid_df[mask]
    
    def search_by_ptu(self, ptu: str) -> pd.DataFrame:
        """Search plasmids by PTU"""
        if self.plasmid_df is None:
            return pd.DataFrame()
        return self.plasmid_df[self.plasmid_df['ptu'] == ptu]
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        if self.plasmid_df is None:
            return {}
        
        return {
            'total_plasmids': len(self.plasmid_df),
            'complete_plasmids': len(self.plasmid_df[self.plasmid_df.get('putatively_complete', '') == 'Yes']),
            'linear_plasmids': len(self.plasmid_df[self.plasmid_df.get('topology', '') == 'Linear']),
            'concatemer_plasmids': len(self.plasmid_df[self.plasmid_df.get('topology', '') == 'Concatemer']),
            'with_mob_genes': len(self.plasmid_df[self.plasmid_df.get('mob_genes', '').notna() & (self.plasmid_df.get('mob_genes', '') != '')]),
            'average_length': self.plasmid_df['length'].mean() if 'length' in self.plasmid_df.columns else 0,
            'unique_hosts': self.plasmid_df['host_taxonomy'].nunique() if 'host_taxonomy' in self.plasmid_df.columns else 0
        }
    
    def analyze(self, plasmid_id: str) -> Optional[Dict]:
        """Comprehensive plasmid analysis"""
        plasmid = self.get_plasmid(plasmid_id)
        if not plasmid:
            return None
        
        return {
            'plasmid_id': plasmid_id,
            'ptu': plasmid.get('ptu', 'N/A'),
            'length': plasmid.get('length', 'N/A'),
            'gene_count': plasmid.get('gene_count', 'N/A'),
            'topology': plasmid.get('topology', 'N/A'),
            'complete': plasmid.get('putatively_complete', 'N/A'),
            'mob_genes': plasmid.get('mob_genes', 'None'),
            't4cp_genes': plasmid.get('t4cp_genes', 'None'),
            't4ss_atpase_genes': plasmid.get('t4ss_atpase_genes', 'None'),
            'host_taxonomy': plasmid.get('host_taxonomy', 'Unknown'),
            'closest_reference': plasmid.get('closest_reference', 'N/A'),
            'ani_percent': plasmid.get('closest_reference_ani_percent', 'N/A'),
            'source_type': plasmid.get('source_type', 'N/A'),
            'ecosystem': plasmid.get('ecosystem', 'N/A')
        }


def analyze_plasmid(plasmid_id: str, data_dir: Path = None) -> Optional[Dict]:
    """Convenience function for single plasmid analysis"""
    analyzer = PlasmidAnalyzer(data_dir)
    return analyzer.analyze(plasmid_id)
