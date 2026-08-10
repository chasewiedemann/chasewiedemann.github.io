# Editing the site

The public pages are ordinary Markdown files:

- `index.md` is the About page.
- `research.md` is the Research page.
- `teaching.md` is the Teaching page.
- `cv.md` is the source for the web and PDF versions of the CV.

## Update the CV

Edit `cv.md`, then run `./build-cv.ps1` in PowerShell to regenerate `files/Chase_Wiedemann_CV.pdf` before publishing the site.

## Add or edit a paper

Open `research.md`. Each paper is one numbered-list item:

```markdown
1. [**Paper title**]({{ '/files/paper-file.pdf' | relative_url }})  
   *Paper status*
```

Put the PDF in the `files` folder, add or edit the list item, then commit and push. GitHub Pages builds the site from the Markdown automatically.
