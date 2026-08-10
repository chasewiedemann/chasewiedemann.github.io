# Editing Papers

Edit `_site/Projects/papers.js`. That one file controls the papers shown on the home page and the Research page.

The important fields are:

- `title`: paper title shown on the site
- `status`: short label, such as `Job market paper`
- `pdf`: PDF filename or full URL
- `summary`: optional short homepage sentence
- `abstract`: optional list of abstract paragraphs

For a simple paper link with no abstract, use:

```js
summary: "",
abstract: []
```

To add another paper, copy one `{ ... }` block in `window.CW_PAPERS`, paste it below the first one, and put a comma between the blocks.

After editing only `papers.js`, you can commit and push. You do not need to rebuild the HTML unless you change the page layout.
