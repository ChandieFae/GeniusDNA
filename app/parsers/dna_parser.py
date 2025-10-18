from typing import List, Tuple, Optional
import re
from ..models import FileFormat


class DNAParser:
    """Parser for DNA files in various formats"""
    
    @staticmethod
    def detect_format(content: str) -> Optional[FileFormat]:
        """
        Detect the format of a DNA file from its content
        
        Args:
            content: File content as string
            
        Returns:
            FileFormat enum or None if format cannot be detected
        """
        lines = content.strip().split('\n')
        
        # Check for VCF format
        if lines and lines[0].startswith('##fileformat=VCF'):
            return FileFormat.VCF
        
        # Check for 23andMe format
        # 23andMe files have comments starting with # and data lines with rsid
        if any(line.startswith('# rsid') for line in lines[:50]):
            return FileFormat.TWENTYTHREEANDME
        
        # Alternative 23andMe check - look for rsid pattern in data
        for line in lines:
            if line.startswith('#'):
                continue
            if re.match(r'^rs\d+\s+', line):
                return FileFormat.TWENTYTHREEANDME
                
        return None
    
    @staticmethod
    def parse_23andme(content: str) -> List[Tuple[str, str, int, str]]:
        """
        Parse 23andMe format DNA file
        
        Args:
            content: File content as string
            
        Returns:
            List of tuples (rsid, chromosome, position, genotype)
        """
        snps = []
        lines = content.strip().split('\n')
        
        for line in lines:
            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                rsid = parts[0]
                chromosome = parts[1]
                try:
                    position = int(parts[2])
                    genotype = parts[3]
                    
                    # Basic validation
                    if rsid.startswith('rs') and genotype not in ['--', '00']:
                        snps.append((rsid, chromosome, position, genotype))
                except (ValueError, IndexError):
                    continue
        
        return snps
    
    @staticmethod
    def parse_vcf(content: str) -> List[Tuple[str, str, int, str]]:
        """
        Parse VCF format DNA file
        
        Args:
            content: File content as string
            
        Returns:
            List of tuples (rsid, chromosome, position, genotype)
        """
        snps = []
        lines = content.strip().split('\n')
        
        for line in lines:
            # Skip header lines and comments
            if line.startswith('#'):
                continue
            
            if not line.strip():
                continue
            
            parts = line.split('\t')
            if len(parts) >= 10:
                chromosome = parts[0]
                try:
                    position = int(parts[1])
                    rsid = parts[2] if parts[2].startswith('rs') else f"rs{parts[1]}"
                    ref = parts[3]
                    alt = parts[4]
                    
                    # Parse genotype from FORMAT and sample columns
                    format_fields = parts[8].split(':')
                    sample_data = parts[9].split(':')
                    
                    genotype = '--'
                    if 'GT' in format_fields:
                        gt_index = format_fields.index('GT')
                        gt = sample_data[gt_index]
                        
                        # Convert GT format (0/1, 1/1, etc.) to genotype
                        if '/' in gt:
                            alleles = gt.split('/')
                        elif '|' in gt:
                            alleles = gt.split('|')
                        else:
                            alleles = [gt, gt]
                        
                        # Map alleles to bases
                        allele_map = {'0': ref, '1': alt}
                        genotype = ''.join([allele_map.get(a, ref) for a in alleles])
                    
                    if genotype != '--':
                        snps.append((rsid, chromosome, position, genotype))
                except (ValueError, IndexError):
                    continue
        
        return snps


def parse_dna_file(content: str, file_format: Optional[FileFormat] = None) -> List[Tuple[str, str, int, str]]:
    """
    Parse DNA file with automatic format detection
    
    Args:
        content: File content as string
        file_format: Optional file format, will be auto-detected if not provided
        
    Returns:
        List of tuples (rsid, chromosome, position, genotype)
        
    Raises:
        ValueError: If format cannot be detected or is unsupported
    """
    parser = DNAParser()
    
    # Auto-detect format if not provided
    if file_format is None:
        file_format = parser.detect_format(content)
        if file_format is None:
            raise ValueError("Unable to detect DNA file format")
    
    # Parse based on format
    if file_format == FileFormat.TWENTYTHREEANDME:
        return parser.parse_23andme(content)
    elif file_format == FileFormat.VCF:
        return parser.parse_vcf(content)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
