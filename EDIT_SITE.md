# Editing the site

The public pages are ordinary Markdown files:

- `index.md` is the About page.
- `research.md` is the Research page.
- `teaching.md` is the Teaching page.

## Add or edit a paper

Open `research.md`. Each paper is one numbered-list item:

```markdown
1. [**Paper title**]({{ '/files/paper-file.pdf' | relative_url }})  
   *Paper status*
```

Put the PDF in the `files` folder, add or edit the list item, then commit and push. GitHub Pages builds the site from the Markdown automatically.
