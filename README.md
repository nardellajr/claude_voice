# Claude Voice

A press-to-talk voice dictation tool using OpenAI's Whisper for speech-to-text transcription. Designed to work seamlessly with Claude Code CLI.

## How It Works

1. **Hold Right Ctrl** to start recording your voice
2. **Release Right Ctrl** to stop recording and transcribe
3. The transcribed text is automatically:
   - Copied to your clipboard
   - Typed into the previously active window (e.g., Claude CLI)

The tool uses the Whisper "small" model for transcription, running locally on your machine.

## Features

- **Press-to-talk**: Simple hotkey-based recording (Right Ctrl)
- **Local transcription**: Uses Whisper AI model locally - no cloud API needed
- **Auto-type**: Transcribed text is automatically typed into your terminal
- **Clipboard integration**: Text is also copied to clipboard via xclip
- **Desktop launcher**: Includes a .desktop file for easy launching from your application menu

## Requirements

### System Dependencies

```bash
sudo apt-get install xclip xdotool
```

### Python Dependencies

```bash
pip install openai-whisper sounddevice numpy pynput
```

Note: Whisper requires PyTorch. See [Whisper installation](https://github.com/openai/whisper#setup) for details.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nardellajr/claude_voice.git
   cd claude_voice
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv ~/.venvs/whisper
   source ~/.venvs/whisper/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install openai-whisper sounddevice numpy pynput
   ```

4. (Optional) Install the desktop launcher:
   ```bash
   cp VoiceClaude.desktop ~/.local/share/applications/
   ```
   Edit the file to update paths to match your system.

## Usage

### Standalone Voice Dictation

```bash
source ~/.venvs/whisper/bin/activate
python whisper_dictate.py
```

Then hold **Right Ctrl** to record and release to transcribe.

### With Claude Code CLI

Run the launcher script to open both the voice dictation tool and Claude CLI:

```bash
./launch_voice_claude.sh
```

This opens two terminals:
- **Voice Dictation**: Runs the Whisper transcription service
- **Claude CLI**: Ready to receive your voice-transcribed input

## Files

| File | Description |
|------|-------------|
| `whisper_dictate.py` | Main voice dictation script |
| `launch_voice_claude.sh` | Launcher script for voice + Claude CLI |
| `VoiceClaude.desktop` | Desktop entry for application menu |

## Configuration

To change the hotkey, edit `whisper_dictate.py` and modify:

```python
HOTKEY = keyboard.Key.ctrl_r  # Change to your preferred key
```

To use a different Whisper model (tiny, base, small, medium, large):

```python
model = whisper.load_model("small")  # Change model size here
```

Larger models are more accurate but slower and require more VRAM.

## License

MIT
