import re
from urllib.parse import urlparse

class EntityNormalizer:
    
    @staticmethod
    def normalize_company_name(name: str) -> str:
        if not name:
            return ""
        
        # Convert to lowercase
        name = name.lower().strip()
        
        # Remove common corporate suffixes
        suffixes = [
            r'\binc\.?', r'\bllc\.?', r'\bltd\.?', r'\bcorp\.?', r'\bcorporation\b',
            r'\bco\.?', r'\bcompany\b', r'\bplc\.?'
        ]
        
        for suffix in suffixes:
            name = re.sub(suffix, '', name)
            
        # Remove punctuation and extra whitespace
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name

    @staticmethod
    def normalize_url(url: str) -> str:
        if not url:
            return ""
            
        url = url.lower().strip()
        
        # Add scheme if missing so urlparse works correctly
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc
            # Remove www.
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            return netloc
        except Exception:
            return url

    @staticmethod
    def normalize_name(name: str) -> str:
        if not name:
            return ""
        name = name.lower().strip()
        name = re.sub(r'[^\w\s]', '', name)
        return re.sub(r'\s+', ' ', name).strip()
