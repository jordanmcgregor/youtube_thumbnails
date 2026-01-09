
import google.generativeai as genai
from PIL import Image
import argparse
import os
from dotenv import load_dotenv

def main():
    """
    Generates an image based on a text prompt using the Gemini API and saves it.
    """
    load_dotenv()  # Load environment variables from .env file
    parser = argparse.ArgumentParser(description="Generate an image from a text prompt using the Gemini API.")
    parser.add_argument("prompt", type=str, help="The text prompt to generate the image from.")
    parser.add_argument("-o", "--output", type=str, default="generated_image.png", help="The output filename for the generated image. Defaults to 'generated_image.png'.")
    parser.add_argument("-m", "--model", type=str, default="gemini-3-pro-image-preview", help="The model to use for image generation. Defaults to 'gemini-3-pro-image-preview'.")
    args = parser.parse_args()

    # --- IMPORTANT: Configure your API key ---
    # You can set your API key as an environment variable 'GEMINI_API_KEY'
    # or replace "YOUR_API_KEY" below with your actual key.
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY")

    if not api_key or api_key == "YOUR_API_KEY":
        print("Error: API key not found.")
        print("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_API_KEY' in the script.")
        return

    try:
        genai.configure(api_key=api_key)

        print(f"Generating image with prompt: '{args.prompt}' using model '{args.model}'...")

        # Create the model
        model = genai.GenerativeModel(args.model)

        # Generate content
        response = model.generate_content(args.prompt)

        # The response may contain text and/or an image. We need to find the image.
        image = None
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                # Extract image data and convert to PIL Image
                import io
                import base64
                image_data = part.inline_data.data
                image = Image.open(io.BytesIO(image_data))
                break

        if image:
            print(f"Image generated successfully. Saving to '{args.output}'...")
            image.save(args.output)
            print("Done.")
        else:
            print("Error: The model did not return an image.")
            # It can be helpful to see the full response for debugging
            if hasattr(response, 'text'):
                print("Full response:", response.text)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
