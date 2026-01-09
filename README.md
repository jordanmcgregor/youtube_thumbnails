# youtube_thumbnails

A focused toolkit for generating hyper-consistent YouTube thumbnails with Gemini image models, plus supporting prompt architecture and reference guides.

## What this repo contains

- **LLM directives**: `AGENT.md`, `CLAUDE.md`, `GEMINI.md` (identical content)
- **Core prompts/docs**:
  - `SYSTEM PROMPT.md` (Prompt Architect system behavior)
  - `IMAGE GENERATION API.md` (Gemini image API reference)
  - `REFERENCE PHOTO GUIDE.md` (full reference shoot guide)
  - `QUICK SHOOT CHECKLIST.md` (one-page checklist)
- **Scripts**:
  - `thumbnail-generator.py` (consistent character thumbnails)
  - `text-to-image.py` (simple text-to-image)
  - `image-to-image.py` (image remixing with roles)
- **Assets**:
  - `logos/` (logo assets for optional use in thumbnails)
  - `reference photos/` (your reference images used by the thumbnail generator)

## Requirements

- Python 3.9+
- Gemini API key

Install dependencies:
```bash
pip install google-generativeai pillow python-dotenv
```

## Setup

1. Create a `.env` file in the repo root:
```bash
cp .env.example .env
```

2. Add your key:
```text
GEMINI_API_KEY=your_key_here
```

3. Add your reference images to `reference photos/` (3–5 high-quality images).

## Usage

### 1) Thumbnail generator (consistent character)
```bash
# First-time setup (creates the reference photos folder)
python3 thumbnail-generator.py --setup

# Basic thumbnail generation (uses reference photos/ automatically)
python3 thumbnail-generator.py "shocked expression pointing at camera, explosion background"

# With a style reference
python3 thumbnail-generator.py "confident smile" -s example_thumbnail.jpg -o output.png

# Generate multiple variations
python3 thumbnail-generator.py "excited expression" --batch 3
```

### 2) Text-to-image (simple)
```bash
python3 text-to-image.py "A cinematic close-up portrait with soft rim light" -o output.png
```

### 3) Image-to-image (role-based reference images)
```bash
python3 image-to-image.py \
  -i "person.jpg:main character" \
  -i "background.jpg:setting and lighting" \
  -i "logo.png:brand element in corner" \
  "Create a professional product photo"
```

## Reference photos

The thumbnail generator uses the first 5 images in `reference photos/` to maintain consistent identity. Keep these fixed over time for best results.

## Notes

- `past thumbnails/` is ignored and safe for local output archives.
- `D5100 PHOTO SHOOT GUIDE.md` is intentionally ignored.

## License

Private/internal use unless otherwise noted.
