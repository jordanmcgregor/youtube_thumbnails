# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Nano Banana Pro Prompt Architect** project - an AI agent system for creating professional image generation prompts for Google's Gemini 3 Pro Image (Nano Banana Pro) API. This is primarily a documentation and prompt engineering project, not a traditional codebase.

## Core Files Architecture

The project consists of three core documentation files that work together:

1. **`system_prompt.md`** - The master prompt that defines the AI agent's behavior
   - Defines the "Prompt Architect" persona and workflow
   - Contains structured collection process (6 categories: Core Creative Vision, Professional Details, Editing Instructions, Reference Inputs, Multi-Image Blending, Brand Style)
   - Must NEVER output final prompt until all required information is collected
   - Uses a guided, step-by-step conversational approach
   - Opening script available at line 116-129

2. **`image_generation.md`** - Complete technical documentation for Nano Banana Pro API (4,611 lines)
   - Official Google API documentation and reference
   - Contains code examples in Python, JavaScript, Go, Java, and REST
   - Sections include: text-to-image, image editing, multi-turn conversations, reference images, grounding with Google Search, 4K resolution generation, thinking process, batch generation
   - Comprehensive prompting guide and strategies (starts at line ~1447)
   - This file serves as the knowledge base for the Prompt Architect

3. **`GEMINI.md`** - High-level project overview and usage guide
   - Explains the project structure and purpose
   - Documents how the three files work together
   - Intended for future AI agents working with this directory

## Python Script

**`generate_image.py`** - Simple CLI tool for image generation
- Generates images using the Gemini API based on text prompts
- Usage: `python generate_image.py "your prompt here" -o output.png -m gemini-3-pro-image-preview`
- Requires `GEMINI_API_KEY` environment variable (loaded from `.env` file)
- Dependencies: `google-generativeai`, `pillow`, `python-dotenv`
- Default model: `gemini-3-pro-image-preview`
- Default output: `generated_image.png`

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

When modifying the system prompt (`system_prompt.md`):
- Maintain the 6-category structure for information collection
- Never allow the agent to output final prompts before all required info is gathered
- Keep the conversational, guided approach
- Preserve the checklist mechanism for showing progress to users

When referencing the API documentation (`image_generation.md`):
- This is a large file (4,611 lines) - use targeted searches
- Prompting strategies section starts around line 1447
- Code examples are organized by language (Python, JavaScript, Go, Java, REST)
- Key capabilities: multi-turn editing (line ~379), reference images (line ~714), Google Search grounding (line ~997), 4K resolution (line ~1141), thinking process (line ~1331)

The project is designed for professional image generation workflows where systematic prompt collection leads to better results than free-form prompting.
