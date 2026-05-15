#!/bin/bash
echo "🚀 Deploying AMR-Plasmid-Analysis-Tool to GitHub..."

# Create repository structure
mkdir -p AMR-Plasmid-Analysis-Tool/{src,notebooks,data/sample_data,docs,tests}
cd AMR-Plasmid-Analysis-Tool

# Initialize git
git init

# Create all files (paste content from above)
# ... 

# Commit and push
git add .
git commit -m "Initial release v1.0.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AMR-Plasmid-Analysis-Tool.git
git push -u origin main

echo "✅ Deployment complete!"
echo "🔗 Visit: https://github.com/YOUR_USERNAME/AMR-Plasmid-Analysis-Tool"
