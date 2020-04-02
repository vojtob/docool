---
title: "Docool - documentation tools"
---

# Dokumentačné nástroje

1. Generovanie obrázkov
1. Vytváranie dokumentácie v html a doc formáte

## Adresárová štruktúra

```
src 
  - img
    - images.json - definitions how to overlay images with icons
    - img_focus.json - definitions how to focus parts of image
    any images in any directory structure. Supported are uxf, mmd and png images
  - model
    - <project_name>.archimate - archi model of project
  - res  
    - icons - icons used to overlay image
  - specifikacia - home of specification in markdown
    - _index.md
    directory structure of specification
utils
  - docool.bat
  - startCmder.bat
```

Generated directories
```
temp
  - img_areas - images with focused areas
  - img_exported - png files from archi and src
  - img_exported_svg - images in svg exported from archi
  - img_icons - images with added icons
  - img_rec - images with named identified rectangles used by areas and icons
  - spec_generated - specification with added archi element descriptions and requirements realizations
  - spec_local - directory with hugo structure of multipage specification to run hugo locally
  - spec_onepage - directory with hugo structure of single page html as base for word generation
release
  - img - all images, decorated
  - <project_name>.docx - generated documentation
```
<div class="mermaid">
graph LR;
  A-->B;
</div>
<script async src="https://unpkg.com/mermaid@8.2.3/dist/mermaid.min.js"></script>
