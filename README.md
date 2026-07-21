# Soyli Sahedova — Portfolio (editable)

`index.html` is a single, self-contained portfolio page. Every image area is an
upload slot you can fill yourself — no code or tools needed.

## How to upload your assets

1. Open **`index.html`** in a browser (double-click it, or drag it into a
   browser tab). Chrome or Edge work best.
2. Each placeholder ("Certificate 1", "SalesShortcut post 1", "Recommendation
   letter", etc.) is a drop zone. To fill one:
   - **drag an image file onto it**, or
   - **click it** and choose a file ("browse files").
3. Once a slot has an image, hover it to get **Replace** (swap the image) and
   **Edit** (drag to reposition / scroll to zoom the crop).

Accepted image types: **PNG, JPEG, WebP, AVIF**. Images are automatically
resized down for you, so large photos are fine.

## Your uploads now save and reload

Previously the uploads disappeared on refresh. They now persist: uploads are
saved **in the browser you uploaded them from** and are restored automatically
every time you reopen the page. Reloading, closing the tab, and reopening the
file all keep your images.

## Sharing your finished portfolio

The saves above live in *your* browser, not inside the file itself — so just
emailing `index.html` would arrive with empty slots. To send a copy with your
images **baked in**:

1. Fill in the slots you want.
2. Click **"Download shareable copy"** (bottom-right of the page).
3. You'll get `soyli-portfolio-shareable.html`.

Send *that* file. It opens on any computer/browser with your images already in
place, as a clean, **read-only** portfolio — no edit controls, no "Edit mode"
badge. Keep working in `index.html` (your editable master) and re-download a new
shareable copy whenever you update something.

### Two things worth knowing

- **`index.html` = your editable master** (uploads save to this browser).
  **The downloaded copy = the shareable, read-only version** (images baked in).
- **Videos:** slots that mention "MP4" only accept a still image (a poster
  frame) — the component is image-only.

## What was changed

Only a small persistence layer was added at the top of the page. It re-creates
the storage bridge the upload slots expect (which only existed in the original
design tool), backed by the browser's IndexedDB with a localStorage fallback.
The design, layout, fonts, and all existing content are byte-for-byte
unchanged.
