# McNabb Family Archive

Family history and biographies, 1702–2025.

[Visit the family archive](https://pduke.github.io/mcnabb.fanclub.rocks/)

## About

Walter Craig Davidson gathered genealogical research on the McNabb, McNeill, Davidson, and related families. According to family recollections, his research included trips to Scotland. Warren Neil McNabb shared Craig’s work with his sister Beverly Nan McNabb Orr and cousin Jimmy Nagle, who extended the family history. Nan gave copies of her notebook to her children; Paul Duke used his copy as the starting point for the website, working with Neeve McNabb to expand it.

The site includes an interactive family tree, biographies, original family photographs, a history of Craig’s research, and a downloadable family archive book. The searchable OCR research collection pairs 277 page texts with their scanned sources. Portions of Craig’s broader research remain unlocated.

## Technical notes

Static HTML, CSS and JavaScript hosted on GitHub Pages. Main pages are in the repository root and `mchtml/`; biographies use `mcpics/`. Historical documents in `mcdata/` and audio in `mcmedia/` are preserved separately.

The OCR search was originally part of an April 2025 Grok-assisted genealogy prototype; these prototype files remain accessible in Git history after the new site replaces them.

**Before publishing:** Replace repository HTML and supporting assets; preserve existing `mcdata/` and `mcmedia/`. The OCR search page is intentionally **not included in this V9 test ZIP**, and remains at `groc_AI/ocr_text.html` on the live site. After the main redesign is published, move that search page to `mchtml/`, add the shared navigation, verify its `../mcdata/` references on GitHub Pages, then update the research link and sitemap.

The printable book will be rebuilt from the approved website content in a later pass; do not treat the bundled PDF as the final corrected edition.

## Credits

Genealogical foundation: Walter Craig Davidson, Beverly Nan McNabb Orr, Warren Neil McNabb, and Jimmy Nagle. Archive compilation: Paul Duke and Neeve McNabb. Site development and digital preservation: Paul Duke.


## V10 rollout notes
The upgraded OCR interface is now at `mchtml/ocr_text.html`, with original OCR `.txt` and scanned `.pdf` pages in existing `mcdata/`. Preserve `mcdata/`, `mcmedia/` and other repository content when deploying. `groc_AI/` is obsolete, but remove it only once the new site is verified. The bundled book PDF is the earlier edition and will be regenerated after website review.
