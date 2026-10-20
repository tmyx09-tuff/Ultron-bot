# Ultron Bot

This repository contains a simple educational robot brain prototype with a Jarvis-style controller and an Ultron-style executor.

## What it does

- Receives a high-level goal from Jarvis
- Decides which robot skill to use
- Executes the action safely
- Uses a fallback planner if no AI API is configured
- Keeps a basic memory of tasks and actions

## Run it

```bash
python ultron_jarvis.py
```

## Example commands

- Move forward
- Say hello to everyone
- Scan the room
- Take a photo
- Check battery
- Grab the box
- Status

## Notes

This is a learning/demo prototype. It is not a real combat or autonomous weapon system and it intentionally uses a safety policy to limit actions.
