# YouTube Audio Downloader Bot

A Telegram bot that downloads audio from YouTube videos. Users send YouTube links and receive high-quality audio files.

## 🎵 Features

- Download audio from any YouTube video (128kbps MP4)
- Automatic quality selection
- Progress tracking and status updates
- Automatic cleanup of temporary files
- Production-ready error handling
- Comprehensive logging

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd YouTube-Audio-Bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Create a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. **Run the bot:**
```bash
python youtube_audio_bot.py
```

## 🐳 Docker Deployment

### Build and run:
```bash
docker build -t youtube-audio-bot .
docker run -d --name youtube-bot --env-file .env youtube-audio-bot
```

### View logs:
```bash
docker logs -f youtube-bot
```

## ☁️ Deploy to Zeabur

1. **Push this repo to GitHub**

2. **In Zeabur Dashboard:**
   - Click "Add Service" → "Git"
   - Select this repository
   - Add environment variable: `TELEGRAM_BOT_TOKEN`
   - Deploy!

3. **Or use custom start command:**
   ```
   python youtube_audio_bot.py
   ```

## 📝 Bot Commands

- `/start` - Welcome message and introduction
- `/help` - Usage instructions

**To download:** Just send any YouTube URL!

### Supported URL formats:
- `https://youtube.com/watch?v=...`
- `https://youtu.be/...`
- `https://www.youtube.com/watch?v=...`

## 📁 Project Structure

```
.
├── youtube_audio_bot.py       # Main bot application
├── youtube_audio_only.py      # Standalone audio downloader
├── youtube_downloader_test.py # Testing script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── logs/                      # Log files (auto-created)
└── downloads/                 # Temporary downloads (auto-created)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | Yes |

### Logging

Logs are stored in `logs/youtube_audio_bot.log` with rotation.

## 🧪 Testing

Run the standalone audio downloader:
```bash
python youtube_audio_only.py
```

Run the full downloader test (video + audio):
```bash
python youtube_downloader_test.py
```

## 🐛 Troubleshooting

### Bot not responding
1. Check if the process is running
2. Verify `TELEGRAM_BOT_TOKEN` is correct
3. Check logs: `tail -f logs/youtube_audio_bot.log`

### Download fails
- Verify internet connection
- Check YouTube URL is valid and accessible
- Some videos may be region-restricted

### FFmpeg not found (Docker)
- FFmpeg is auto-installed in Docker
- For local: `apt install ffmpeg` (Linux) or `brew install ffmpeg` (Mac)

## 📊 Performance

- Average download time: 30-60 seconds (depending on video length)
- Supported file formats: MP4 audio, M4A
- Maximum file size: Limited by Telegram (50MB for bots)

## 🔒 Security

- Environment variables are never logged
- Temporary files are deleted after upload
- No data is stored permanently

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Issues and pull requests are welcome!

---

**Made with ❤️ for easy YouTube audio downloads**
