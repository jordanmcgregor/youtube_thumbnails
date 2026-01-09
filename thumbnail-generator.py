"""
YouTube Thumbnail Generator with Consistent Character
Uses a consistent set of reference images to maintain your digital avatar across all thumbnails
"""

import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import argparse
import glob
import io

# Load environment variables
load_dotenv()

# Default reference folder for your consistent avatar
DEFAULT_REFERENCE_FOLDER = "./reference photos"

def get_reference_images(reference_path=None):
    """
    Load reference images from a folder or list of files.
    If no path provided, uses the default reference folder for consistency.
    """
    if reference_path is None:
        reference_path = DEFAULT_REFERENCE_FOLDER

    # If it's a folder, get all images from it
    if os.path.isdir(reference_path):
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(reference_path, ext)))
            image_files.extend(glob.glob(os.path.join(reference_path, ext.upper())))

        if not image_files:
            raise ValueError(f"No images found in {reference_path}")

        # Limit to 5 images for character consistency
        image_files = sorted(image_files)[:5]
        return image_files
    else:
        # If it's a single file or list, return as-is
        return [reference_path] if isinstance(reference_path, str) else reference_path


def generate_thumbnail(prompt, reference_images=None, style_reference=None, logo_references=None, output_path="thumbnail.png",
                      aspect_ratio="16:9", resolution="4K"):
    """
    Generate a YouTube thumbnail with consistent character using reference images.

    Args:
        prompt: Description of the thumbnail scene (e.g., "shocked expression with hands on face")
        reference_images: List of paths to your reference photos, or path to reference folder
                         If None, uses DEFAULT_REFERENCE_FOLDER for consistency
        style_reference: Optional path to example thumbnail for style/composition reference
        logo_references: Optional list of paths to logo/icon images to include in the thumbnail
        output_path: Where to save the generated thumbnail
        aspect_ratio: YouTube thumbnails are 16:9
        resolution: 4K for high quality thumbnails
    """

    # Configure API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return None

    genai.configure(api_key=api_key)

    # Load reference images
    if reference_images is None:
        print(f"Using default reference folder: {DEFAULT_REFERENCE_FOLDER}")
        reference_images = get_reference_images()
    elif isinstance(reference_images, str):
        reference_images = get_reference_images(reference_images)

    # Build the prompt with instruction
    enhanced_prompt = prompt
    if style_reference and os.path.exists(style_reference):
        print(f"\n📸 Style Reference: {style_reference}")
        enhanced_prompt = f"Create a thumbnail inspired by the style reference image. {prompt}"

    if logo_references:
        logo_list = logo_references if isinstance(logo_references, list) else [logo_references]
        print(f"\n🎨 Logo References: {len(logo_list)} logo(s)")
        for logo_path in logo_list:
            if os.path.exists(logo_path):
                print(f"   ✓ {os.path.basename(logo_path)}")

    print(f"\n👤 Loading {len(reference_images)} character reference images for consistency...")
    for img_path in reference_images:
        print(f"   ✓ {os.path.basename(img_path)}")

    print(f"\n🎨 Generating thumbnail...")
    print(f"   Prompt: '{enhanced_prompt}'")
    print(f"   Resolution: {resolution} | Aspect Ratio: {aspect_ratio}")

    # Build content with text and images
    content_parts = [enhanced_prompt]

    # Add style reference if provided
    if style_reference and os.path.exists(style_reference):
        content_parts.append(Image.open(style_reference))

    # Add logo references if provided
    if logo_references:
        logo_list = logo_references if isinstance(logo_references, list) else [logo_references]
        for logo_path in logo_list:
            if os.path.exists(logo_path):
                content_parts.append(Image.open(logo_path))

    # Add character reference images
    for img_path in reference_images:
        if os.path.exists(img_path):
            content_parts.append(Image.open(img_path))

    # Create model and generate
    model = genai.GenerativeModel("gemini-3-pro-image-preview")

    try:
        response = model.generate_content(content_parts)

        # Extract image from response
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                image = Image.open(io.BytesIO(image_data))
                image.save(output_path)
                print(f"\n✅ Thumbnail saved: {output_path}")
                return output_path

        print("❌ No image generated in response")
        return None

    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None


def setup_reference_folder():
    """
    Create the reference folder and provide instructions for setup.
    """
    if not os.path.exists(DEFAULT_REFERENCE_FOLDER):
        os.makedirs(DEFAULT_REFERENCE_FOLDER)
        print(f"✅ Created reference folder: {DEFAULT_REFERENCE_FOLDER}")
        print("\n📋 SETUP INSTRUCTIONS:")
        print("=" * 70)
        print("To create a consistent AI avatar of yourself:")
        print("\n1. Take 3-5 high-quality photos of yourself:")
        print("   • Front-facing (looking at camera)")
        print("   • Slight left turn")
        print("   • Slight right turn")
        print("   • Different expressions (neutral, smiling)")
        print("   • Consistent lighting (well-lit, avoid harsh shadows)")
        print("\n2. Save these photos to:")
        print(f"   {os.path.abspath(DEFAULT_REFERENCE_FOLDER)}/")
        print("\n3. Name them clearly:")
        print("   • face_front.jpg")
        print("   • face_left.jpg")
        print("   • face_right.jpg")
        print("   • etc.")
        print("\n4. Use the SAME photos for ALL thumbnails to ensure consistency!")
        print("=" * 70)
    else:
        # Check if folder has images
        existing_images = get_reference_images(DEFAULT_REFERENCE_FOLDER)
        if existing_images:
            print(f"✅ Reference folder already set up with {len(existing_images)} images:")
            for img in existing_images:
                print(f"   • {os.path.basename(img)}")
        else:
            print(f"⚠️  Reference folder exists but is empty: {DEFAULT_REFERENCE_FOLDER}")
            print("   Add 3-5 reference photos of yourself to this folder.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate consistent YouTube thumbnails using your reference images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First-time setup (creates reference folder)
  python thumbnail-generator.py --setup

  # Generate thumbnail using default reference folder (recommended for consistency)
  python thumbnail-generator.py "shocked expression pointing at camera"

  # With style reference (e.g., Mr Beast thumbnail)
  python thumbnail-generator.py "excited mouth open" -s mr_beast_example.jpg

  # Use custom reference photos (not recommended, reduces consistency)
  python thumbnail-generator.py "serious look" -r custom_photos/

  # Generate multiple variations for A/B testing
  python thumbnail-generator.py "pointing at viewer surprised face" --batch 3

TIPS FOR MAXIMUM CONSISTENCY:
  • Always use the default reference folder (don't use -r flag)
  • Use the SAME reference photos for all your thumbnails
  • Take high-quality, well-lit reference photos initially
        """
    )

    parser.add_argument('prompt', type=str, nargs='?',
                       help='Description of the thumbnail scene and expression')
    parser.add_argument('-r', '--references', default=None,
                       help='Path to reference folder or images (default: ./reference photos/)')
    parser.add_argument('-s', '--style', default=None,
                       help='Optional: Path to example thumbnail for style reference')
    parser.add_argument('-l', '--logo', action='append', dest='logos',
                       help='Optional: Path to logo/icon image to include in thumbnail (can be used multiple times)')
    parser.add_argument('-o', '--output', default='thumbnail.png',
                       help='Output filename (default: thumbnail.png)')
    parser.add_argument('--aspect-ratio', default='16:9',
                       choices=['16:9', '9:16', '4:3', '1:1'],
                       help='Aspect ratio (default: 16:9 for YouTube, 9:16 for Shorts)')
    parser.add_argument('--resolution', default='4K',
                       choices=['1K', '2K', '4K'],
                       help='Resolution (default: 4K for maximum quality)')
    parser.add_argument('--batch', type=int, default=1,
                       help='Generate multiple variations (default: 1)')
    parser.add_argument('--setup', action='store_true',
                       help='Set up the reference folder for first-time use')

    args = parser.parse_args()

    # Setup mode
    if args.setup:
        setup_reference_folder()
        return

    # Require prompt if not in setup mode
    if not args.prompt:
        parser.error("the following arguments are required: prompt (or use --setup)")

    # Check if reference folder exists
    if args.references is None and not os.path.exists(DEFAULT_REFERENCE_FOLDER):
        print(f"⚠️  Reference folder not found: {DEFAULT_REFERENCE_FOLDER}")
        print("Run with --setup flag first to create it:")
        print("  python thumbnail-generator.py --setup")
        return

    # Generate thumbnails
    if args.batch == 1:
        generate_thumbnail(
            prompt=args.prompt,
            reference_images=args.references,
            style_reference=args.style,
            logo_references=args.logos,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        )
    else:
        # Generate multiple variations
        base_name = os.path.splitext(args.output)[0]
        ext = os.path.splitext(args.output)[1] or '.png'

        for i in range(args.batch):
            output_path = f"{base_name}_v{i+1}{ext}"
            print(f"\n{'='*60}")
            print(f"🎬 Generating variation {i+1}/{args.batch}")
            print(f"{'='*60}")
            generate_thumbnail(
                prompt=args.prompt,
                reference_images=args.references,
                style_reference=args.style,
                logo_references=args.logos,
                output_path=output_path,
                aspect_ratio=args.aspect_ratio,
                resolution=args.resolution
            )


if __name__ == "__main__":
    main()
