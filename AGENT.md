# LLM DIRECTIVES

This file provides guidance to LLM coding agents when working with code in this repository.

## Project Overview

This is the **Nano Banana Pro** project with two main components:

1. **Prompt Architect System** - AI agent for creating professional image generation prompts for Gemini 3 Pro Image API
2. **YouTube Thumbnail Generator** - Hyper-consistent AI thumbnail creation system using reference photos for character consistency

The project combines documentation, prompt engineering, and practical image generation tools for professional content creators.

## Core Files Architecture

The project consists of three core documentation files that work together:

1. **`SYSTEM PROMPT.md`** - The master prompt that defines the AI agent's behavior
   - Defines the "Prompt Architect" persona and workflow
   - Contains structured collection process (6 categories: Core Creative Vision, Professional Details, Editing Instructions, Reference Inputs, Multi-Image Blending, Brand Style)
   - Must NEVER output final prompt until all required information is collected
   - Uses a guided, step-by-step conversational approach

2. **`IMAGE GENERATION API.md`** - Complete technical documentation for Nano Banana Pro API (4,611 lines)
   - Official Google API documentation and reference
   - Contains code examples in Python, JavaScript, Go, Java, and REST
   - Sections include: text-to-image, image editing, multi-turn conversations, reference images, grounding with Google Search, 4K resolution generation, thinking process, batch generation
   - Comprehensive prompting guide and strategies (starts at line ~1447)
   - This file serves as the knowledge base for the Prompt Architect

3. **`GEMINI.md`** - High-level project overview and usage guide
   - Explains the project structure and purpose
   - Documents how the three files work together
   - Intended for future AI agents working with this directory

## Python Scripts

### `text-to-image.py` - Simple CLI tool for image generation
- Generates images using the Gemini API based on text prompts
- Usage: `python text-to-image.py "your prompt here" -o output.png -m gemini-3-pro-image-preview`
- Requires `GEMINI_API_KEY` environment variable (loaded from `.env` file)
- Dependencies: `google-generativeai`, `pillow`, `python-dotenv`
- Default model: `gemini-3-pro-image-preview`
- Default output: `generated_image.png`

### `thumbnail-generator.py` - YouTube Thumbnail Generator with Consistent Character
**Purpose**: Generate hyper-consistent AI thumbnails using reference photos to maintain the same digital avatar across all thumbnails (Mr Beast-style consistency).

**Key Features**:
- Uses 5 reference photos to create a consistent "digital clone" of yourself
- Supports style references (upload example thumbnails to match their composition/vibe)
- Generates 4K resolution thumbnails (3840x2160) in 16:9 aspect ratio
- Batch generation for A/B testing multiple variations
- Character consistency maintained across all generated thumbnails

**Usage**:
```bash
# Basic thumbnail generation (uses reference photos/ automatically)
python3 thumbnail-generator.py "shocked expression pointing at camera, explosion background"

# With style reference (match an existing thumbnail's composition)
python3 thumbnail-generator.py "confident smile" -s example_thumbnail.jpg -o output.png

# Generate 3 variations for A/B testing
python3 thumbnail-generator.py "excited expression" --batch 3

# Custom reference photos (not recommended - reduces consistency)
python3 thumbnail-generator.py "serious look" -r custom_folder/
```

**Setup Requirements**:
1. Run `python3 thumbnail-generator.py --setup` to create `reference photos/` folder
2. Add 5 reference photos of yourself (see REFERENCE PHOTO GUIDE.md for detailed instructions)
3. Always use the same 5 photos for maximum consistency across all thumbnails

**Reference Photo Requirements**:
- Photo 1: Front-facing, neutral expression
- Photo 2: Front-facing, big smile
- Photo 3: 3/4 view, body rotated right
- Photo 4: 3/4 view, body rotated left
- Photo 5: Front-facing, expressive (your signature thumbnail expression)

**How It Works**:
- The script sends your prompt + 5 reference photos to Gemini 3 Pro Image API
- API uses reference photos to maintain facial consistency (up to 5 human reference images supported)
- Generates 4K thumbnail with your face in any scenario/background you describe
- Result: Hyper-consistent thumbnails that all look like YOU, regardless of scene

**Pro Tips**:
- Be specific in prompts: "jaw dropped shocked, hands on face, colorful explosion background" vs just "surprised"
- Use style references (-s flag) to match successful thumbnail compositions
- Generate batches (--batch 3) to pick the best variation
- Never change your reference photos once set - consistency is key

### `image-to-image.py` - Image remixing with reference images
- Supports 1-14 reference images with optional role descriptions
- Usage: `python image-to-image.py -i "photo.jpg:preserve this person's face" "professional headshot"`
- Requires `GEMINI_API_KEY` environment variable (loaded from `.env` file)

## Environment Setup

Required environment variable:
- `GEMINI_API_KEY` - Set in `.env` file or as environment variable

Python dependencies (install with pip):
```bash
pip install google-generativeai pillow python-dotenv
```

## Model Selection

Two image models available:
- **gemini-2.5-flash-image** (Nano Banana) - Fast generation
- **gemini-3-pro-image-preview** (Nano Banana Pro) - Advanced features including up to 14 reference images, 4K resolution, Google Search grounding, thinking process

## Working with This Project

When modifying the system prompt (`SYSTEM PROMPT.md`):
- Maintain the 6-category structure for information collection
- Never allow the agent to output final prompts before all required info is gathered
- Keep the conversational, guided approach
- Preserve the checklist mechanism for showing progress to users

When referencing the API documentation (`IMAGE GENERATION API.md`):
- This is a large file (4,611 lines) - use targeted searches
- Prompting strategies section starts around line 1447
- Code examples are organized by language (Python, JavaScript, Go, Java, REST)
- Key capabilities: multi-turn editing (line ~379), reference images (line ~714), Google Search grounding (line ~997), 4K resolution (line ~1141), thinking process (line ~1331)

The project is designed for professional image generation workflows where systematic prompt collection leads to better results than free-form prompting.

## Thumbnail Generation Guides

**`REFERENCE PHOTO GUIDE.md`** - General professional photo shoot guide
- Comprehensive guide for creating reference photos with any camera
- 2-speedlight "Clamshell + Fill" lighting setup
- Camera settings and framing best practices
- Quality checklist and troubleshooting tips
- Equipment list and setup instructions

**`QUICK SHOOT CHECKLIST.md`** - One-page reference card
- Print-friendly quick reference for photo shoots
- Speedlight positions diagram
- Camera settings at a glance
- The 5 required shots checklist
- Quick lighting adjustment troubleshooting

**Workflow**:
1. First time: Follow REFERENCE PHOTO GUIDE.md to capture your 5 reference photos
2. Save photos to `reference photos/` folder with proper naming
3. Use the same 5 photos forever for maximum consistency
4. Generate unlimited thumbnails with `thumbnail-generator.py`
5. Only retake reference photos if major appearance change (haircut, facial hair, glasses, etc.)
