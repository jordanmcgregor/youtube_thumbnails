#!/usr/bin/env python3
"""
Image-to-Image Generation Script for Nano Banana Pro
Supports 1-14 reference images with role descriptions
"""

import os
import sys
import argparse
import io
import base64
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

def parse_image_arg(image_arg):
    """
    Parse image argument in format: 'path:description' or just 'path'
    Returns tuple: (path, description)
    """
    if ':' in image_arg:
        parts = image_arg.split(':', 1)
        return parts[0].strip(), parts[1].strip()
    else:
        return image_arg.strip(), None

def validate_images(image_specs):
    """
    Validate that image files exist and are readable
    Returns list of validated (path, description) tuples
    """
    validated = []
    for path, description in image_specs:
        if not os.path.exists(path):
            print(f"Error: Image file not found: {path}")
            sys.exit(1)

        try:
            # Test if we can open the image
            with Image.open(path) as img:
                img.verify()
            validated.append((path, description))
        except Exception as e:
            print(f"Error: Cannot open image {path}: {e}")
            sys.exit(1)

    return validated

def build_prompt_with_descriptions(base_prompt, image_specs):
    """
    Build enhanced prompt that includes image role descriptions
    """
    if not any(desc for _, desc in image_specs):
        # No descriptions provided, use base prompt only
        return base_prompt

    # Build a prompt that references the images
    enhanced_parts = []

    for i, (path, description) in enumerate(image_specs, 1):
        if description:
            enhanced_parts.append(f"Image {i} ({Path(path).name}): {description}")

    if enhanced_parts:
        image_context = "\n".join(enhanced_parts)
        return f"{image_context}\n\nGenerate: {base_prompt}"
    else:
        return base_prompt

def generate_image(image_specs, prompt, model, output_path, aspect_ratio, resolution):
    """
    Generate image using Gemini API with reference images
    Note: aspect_ratio and resolution are currently not supported in the older API
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)

    # Validate image count
    if len(image_specs) > 14:
        print(f"Error: Maximum 14 reference images allowed. You provided {len(image_specs)}.")
        sys.exit(1)

    if len(image_specs) == 0:
        print("Error: At least 1 reference image is required.")
        sys.exit(1)

    print(f"\n🎨 Generating image with {len(image_specs)} reference image(s)...")
    print(f"Model: {model}")
    print(f"\nReference Images:")
    for i, (path, description) in enumerate(image_specs, 1):
        desc_text = f" - {description}" if description else ""
        print(f"  {i}. {Path(path).name}{desc_text}")

    # Build the enhanced prompt
    enhanced_prompt = build_prompt_with_descriptions(prompt, image_specs)
    print(f"\nPrompt: {enhanced_prompt}\n")

    try:
        # Configure API
        genai.configure(api_key=api_key)

        # Create model
        model_instance = genai.GenerativeModel(model)

        # Build contents array with prompt and images
        contents = [enhanced_prompt]
        for path, _ in image_specs:
            contents.append(Image.open(path))

        # Generate content
        print("Generating... (this may take 10-30 seconds)")
        response = model_instance.generate_content(contents)

        # Save the generated image
        image_saved = False
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                # Extract image data and convert to PIL Image
                image_data = part.inline_data.data
                image = Image.open(io.BytesIO(image_data))
                image.save(output_path)
                print(f"\n✅ Image saved to: {output_path}")
                image_saved = True
                break
            elif hasattr(part, 'text') and part.text:
                print(f"\nModel response: {part.text}")

        if not image_saved:
            print("\n⚠️  No image was generated in the response.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Generate images using reference images with Nano Banana Pro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single image remix
  python image-to-image.py -i "photo.jpg:preserve this person's face" "professional headshot"

  # Multiple images with roles
  python image-to-image.py \\
    -i "person.jpg:main character" \\
    -i "background.jpg:setting and lighting" \\
    -i "logo.png:brand element in corner" \\
    "Create a professional product photo"

  # Custom output and resolution
  python image-to-image.py -i "reference.jpg:art style" "fantasy landscape" -o output.png --resolution 4K
        """
    )

    parser.add_argument(
        '-i', '--image',
        action='append',
        dest='images',
        required=True,
        help='Reference image in format "path:description" or just "path" (can be used multiple times, 1-14 max)'
    )

    parser.add_argument(
        'prompt',
        help='Text prompt describing what to generate'
    )

    parser.add_argument(
        '-o', '--output',
        default='generated_image.png',
        help='Output image path (default: generated_image.png)'
    )

    parser.add_argument(
        '-m', '--model',
        default='gemini-3-pro-image-preview',
        help='Model to use (default: gemini-3-pro-image-preview)'
    )

    parser.add_argument(
        '--aspect-ratio',
        default='1:1',
        choices=['1:1', '2:3', '3:2', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9'],
        help='Aspect ratio (default: 1:1)'
    )

    parser.add_argument(
        '--resolution',
        default='2K',
        choices=['1K', '2K', '4K'],
        help='Resolution (default: 2K)'
    )

    args = parser.parse_args()

    # Parse image arguments
    image_specs = [parse_image_arg(img) for img in args.images]

    # Validate images
    validated_images = validate_images(image_specs)

    # Generate image
    generate_image(
        validated_images,
        args.prompt,
        args.model,
        args.output,
        args.aspect_ratio,
        args.resolution
    )

if __name__ == '__main__':
    main()
