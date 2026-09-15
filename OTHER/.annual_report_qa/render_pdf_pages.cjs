const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const canvasLib = require('@napi-rs/canvas');

globalThis.DOMMatrix = canvasLib.DOMMatrix;
globalThis.ImageData = canvasLib.ImageData;
globalThis.Path2D = canvasLib.Path2D;

async function main() {
  const pdfPath = process.argv[2];
  const outputDir = process.argv[3];
  const modulesDir = process.env.CODEX_NODE_MODULES;
  if (!pdfPath || !outputDir || !modulesDir) {
    throw new Error('Usage: render_pdf_pages.cjs input.pdf output_dir with CODEX_NODE_MODULES set');
  }

  fs.mkdirSync(outputDir, { recursive: true });
  const pdfjsPath = path.join(modulesDir, 'pdfjs-dist', 'legacy', 'build', 'pdf.mjs');
  const pdfjs = await import(pathToFileURL(pdfjsPath).href);
  const data = new Uint8Array(fs.readFileSync(pdfPath));
  const pdf = await pdfjs.getDocument({ data, disableWorker: true, useSystemFonts: true }).promise;

  for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber += 1) {
    const page = await pdf.getPage(pageNumber);
    const viewport = page.getViewport({ scale: 2.0 });
    const canvas = canvasLib.createCanvas(Math.ceil(viewport.width), Math.ceil(viewport.height));
    const context = canvas.getContext('2d');
    await page.render({ canvasContext: context, viewport }).promise;
    const outputPath = path.join(outputDir, `page-${pageNumber}.png`);
    fs.writeFileSync(outputPath, await canvas.encode('png'));
    process.stdout.write(`${outputPath}\n`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
