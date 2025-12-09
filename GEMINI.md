# Nano Banana Pro - Prompt Architect

This directory contains the configuration and documentation for an AI agent that acts as a "Prompt Architect" for Google's Nano Banana Pro (Gemini 3 Pro Image) image generation model.

## Directory Overview

The project is designed to guide users in a step-by-step, conversational manner to create high-quality, detailed, and effective prompts for image generation. It is a "non-code" project, and the core of it is the `system_prompt.md` file, which defines the AI agent's persona, rules, and workflow.

## Key Files

*   **`system_prompt.md`**: This is the master prompt that defines the AI agent. It instructs the agent to act as a "Prompt Architect" and systematically collect all necessary information from the user before generating a final, production-ready image prompt. It outlines a structured process covering:
    *   Core Creative Vision
    *   Professional-Level Details
    *   Editing Instructions
    *   Reference Inputs
    *   Multi-Image Blending & Character Consistency
    *   Brand Style

*   **`image_generation.md`**: This file contains the technical documentation for the Nano Banana Pro image generation API. It serves as the knowledge base for the Prompt Architect, providing details on how to generate images, edit them, use multi-turn conversations, and leverage advanced features. It also includes a comprehensive guide on prompt strategies for various use cases.

*   **`GEMINI.md`**: This file (the one you're reading) provides a high-level overview of the project for any AI agent interacting with this directory in the future.

## Usage

The contents of this directory are intended to be used to power an AI assistant. The `system_prompt.md` should be used as the initial system prompt for the AI, and the `image_generation.md` file provides the necessary context and documentation for the AI to understand the nuances of creating effective image prompts for Nano Banana Pro. The overall goal is to create a highly specialized and helpful assistant for professional image generation tasks.
