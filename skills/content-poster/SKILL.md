---
name: content-poster
description: Create posts for Telegram channel. Use when user provides a topic and wants to create a post with text and images. Searches for current information, writes engaging content, finds relevant images, sends draft to admin for approval before publishing to channel.
---

# Content Poster

Create engaging Telegram channel posts with AI-generated content and curated images.

## Workflow

1. **Receive topic** from admin via Telegram DM
2. **Research** the topic using web search for current information
3. **Write content** - engaging post text in Russian, optimized for Telegram
4. **Find images** - search for relevant photos from the researched sources
5. **Send draft** to admin in DM with preview
6. **Wait for approval**:
   - If admin sends "ok", "да", "пост", "публикуй" → publish to channel
   - If admin sends corrections → revise and resend draft
7. **Publish** approved content to channel

## Content Guidelines

- Write in Russian
- Keep posts concise but informative (300-800 characters)
- Use line breaks for readability
- Add relevant emoji sparingly
- Include source attribution when appropriate
- No clickbait, focus on value
- Also edit the font sparingly (bold, italic, monospace, underline)

## Commands

Admin can use these commands in DM:

- Send topic text → starts new post creation
- "ок" / "да" / "пост" / "публикуй" → approve and publish current draft
- Any other text after draft → treated as revision request

## Image Handling

- Search for images related to the topic
- Prefer high-quality, relevant images
- Download and attach to the post
- If no suitable images found, post text only

## Channel Publishing

Target channel ID is stored in CHANNEL_ID environment variable.
Use Telegram Bot API to send media group or text message.
