from diffusers import StableDiffusionPipeline
from diffusers import AutoPipelineForText2Image

import torch
import sys
from run_ollama import LLM_Util 
import ollama

from PIL import Image
import base64
import io

class ReImagine:

    def __init__(self):
        self.imageDescriptionModel = LLM_Util("llava:7b")
        self.textModel = LLM_Util("llama3.2")

    def encode_image(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def generateDescription(self, image_path):
        image_b64 = self.encode_image(image_path)

        print("\nGenerating description using 'llava:7b'...\n")
        query = "Describe this image in rich detail with emotions & visual elements."
        description = self.imageDescriptionModel.ask(query, [image_b64])
        return description

    def generateStableDiffusionImage(self, prompt, output_path):
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32
        ).to("cpu")  # or "cpu" , "cuda" for GPU

        result = pipe(prompt)
        imageCount = len(result.images)
        print(f"stable-diffusion-v1-5 Total Images {imageCount}")
        image = result.images[0]
        image.save(f"stable-diffusion-v1-5_{output_path}")

    def generateSdTurboImage(self, prompt, output_path):
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=torch.float32
        ).to("cpu")
        result = pipe(prompt)
        imageCount = len(result.images)
        print(f"sd-turbo Total Images {imageCount}")
        image = result.images[0]
        image.save(f"sd-turbo_output_{output_path}")
    
    def process(self, inputImagePath, outputImagePath):
        description = self.generateDescription(inputImage_path)
        #print("\n Generated Description:\n", description)
        
        # Refine the image description to below 77 tokens, as diffusion model is limited to process 77 tokens.
        descriptionRefinePrompt = f"""
            Refine & redefine this image description below 70 tokens without lossing the key information 
            & details of the information: {description}, 
            Don't add your thoughts or additional information. 
            you are restricted to share the image description alone.
        """
        
        imagePrompt = self.textModel.ask(descriptionRefinePrompt)
    
        prompt = f"A high definition image with cartoon style for {imagePrompt}"

        print(f"Image Prompt:: {prompt}")
        # 1. First image model
        self.generateStableDiffusionImage(prompt, outputImage_path)
        # 2. Second image model
        self.generateSdTurboImage(prompt, outputImage_path)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reimagine.py <input_image path> <output_image path>")
        sys.exit(1)

    inputImage_path = sys.argv[1]
    outputImage_path = sys.argv[2]
    reimagine = ReImagine()
    reimagine.process(inputImage_path, outputImage_path)

    