#!/bin/bash
# Launch Claude CLI with voice dictation

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Launch whisper dictation in one terminal
gnome-terminal --title="Voice Dictation" --geometry=80x12 -- bash -c "
    source /home/mike/.venvs/whisper/bin/activate
    cd '$SCRIPT_DIR'
    python whisper_dictate.py
    exec bash
" &

# Give it a moment to start loading the model
sleep 1

# Launch Claude CLI in another terminal (this one gets focus)
gnome-terminal --title="Claude CLI" --geometry=120x40 -- bash -c "
    cd /home/mike
    /home/mike/.local/bin/claude
    exec bash
"
