#!/usr/bin/env python3
import os
import re
from pathlib import Path

def extract_title_from_filename(filepath):
    """Extract a title from the filename, converting dashes/underscores to spaces and capitalizing"""
    filename = Path(filepath).stem
    # Convert dashes and underscores to spaces
    title = filename.replace('-', ' ').replace('_', ' ')
    # Capitalize each word
    title = title.title()
    # Handle special cases
    title = title.replace('Api', 'API')
    title = title.replace('Ui', 'UI')
    title = title.replace('Mdx', 'MDX')
    title = title.replace('Html', 'HTML')
    title = title.replace('Css', 'CSS')
    title = title.replace('Js', 'JS')
    title = title.replace('Json', 'JSON')
    title = title.replace('Sql', 'SQL')
    title = title.replace('Db', 'Database')
    title = title.replace('App', 'Application')
    title = title.replace('Vdbs', 'Vector Databases')
    title = title.replace('Nlq', 'NLQ')
    title = title.replace('Ecomm', 'E-commerce')
    title = title.replace('Recsys', 'Recommendation System')
    title = title.replace('Rag', 'RAG')
    title = title.replace('Hr', 'HR')
    
    return title

def extract_title_from_first_heading(content):
    """Extract title from the first heading in the content"""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return None

def has_frontmatter_title(content):
    """Check if the content already has a title in frontmatter"""
    if not content.startswith('---'):
        return False
    
    # Find the end of frontmatter
    lines = content.split('\n')
    frontmatter_end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            frontmatter_end = i
            break
    
    if frontmatter_end == -1:
        return False
    
    frontmatter = '\n'.join(lines[1:frontmatter_end])
    return re.search(r'^title\s*:', frontmatter, re.MULTILINE) is not None

def add_title_to_file(filepath):
    """Add title to a file if it doesn't have one"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_frontmatter_title(content):
            print(f"✓ {filepath} already has a title")
            return
        
        # Extract or generate title
        title_from_heading = extract_title_from_first_heading(content)
        title_from_filename = extract_title_from_filename(filepath)
        
        # Prefer title from heading if available, otherwise use filename
        title = title_from_heading if title_from_heading else title_from_filename
        
        if content.startswith('---'):
            # File has frontmatter, add title to it
            lines = content.split('\n')
            frontmatter_end = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    frontmatter_end = i
                    break
            
            if frontmatter_end != -1:
                # Insert title at the beginning of frontmatter
                lines.insert(1, f'title: "{title}"')
                new_content = '\n'.join(lines)
            else:
                # Malformed frontmatter, add new frontmatter
                new_content = f'---\ntitle: "{title}"\n---\n\n{content}'
        else:
            # No frontmatter, add new frontmatter
            new_content = f'---\ntitle: "{title}"\n---\n\n{content}'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Added title '{title}' to {filepath}")
        
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")

def main():
    """Process all .mdx files in the current directory and subdirectories"""
    mdx_files = list(Path('.').rglob('*.mdx'))
    
    print(f"Found {len(mdx_files)} .mdx files")
    print("Processing files...")
    
    for filepath in mdx_files:
        add_title_to_file(str(filepath))
    
    print("\nDone!")

if __name__ == "__main__":
    main() 