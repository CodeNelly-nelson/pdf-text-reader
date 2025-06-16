# PDF Text-to-Speech Reader

A powerful command-line PDF reader that converts PDF documents to speech with intelligent voice selection, real-time controls, and multi-language support.

## ✨ Features

### 🎯 Core Functionality
- **PDF Text Extraction**: Reads text from PDF files using PyPDF2
- **Text-to-Speech**: High-quality speech synthesis using pyttsx3
- **Real-time Controls**: Pause, resume, speed adjustment, and volume control while reading
- **Smart Text Processing**: Automatic sentence segmentation and text cleaning

### 🌍 Advanced Voice Management
- **Language-Grouped Voice Selection**: Voices organized by language for easy selection
- **Voice Testing**: Test voices before starting to read
- **Multi-language Support**: Supports all system-installed TTS voices
- **Intelligent Voice Mapping**: Clean display names for better voice identification

### 🎮 Interactive Controls
- **Pause/Resume**: `pause` or `p`
- **Speed Control**: `faster`/`+` and `slower`/`-`
- **Volume Control**: `louder`/`up` and `quieter`/`down`
- **Navigation**: `restart`/`r` to start over
- **Stop/Quit**: `stop`/`s` or `quit`/`q`
- **Help**: `help`/`h` for command reference

### 📊 Progress Tracking
- Real-time sentence-by-sentence progress
- Page-by-page processing feedback
- Total sentence count and current position

## 🔧 Installation

### Prerequisites
- Python 3.6 or higher
- Required Python packages:
  ```bash
  pip install pyttsx3 PyPDF2
  ```

### System Requirements
- **macOS**: Full voice selection features (recommended)
- **Windows**: Basic functionality with limited voice options
- **Linux**: Basic functionality with espeak/festival

### macOS Setup (Recommended)
macOS provides the best experience with high-quality voices:
```bash
# Install Python dependencies
pip install pyttsx3 PyPDF2

# macOS comes with built-in high-quality voices
# You can add more voices in System Preferences > Accessibility > Speech
```

### Windows Setup
```bash
# Install Python dependencies
pip install pyttsx3 PyPDF2

# Windows uses SAPI voices
# Additional voices can be installed from Microsoft Store
```

### Linux Setup
```bash
# Install Python dependencies
pip install pyttsx3 PyPDF2

# Install espeak (most common TTS engine for Linux)
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
# or for Fedora/CentOS:
sudo yum install espeak espeak-devel
```

## 🚀 Usage

### Basic Usage
```bash
python myreader.py document.pdf
```

### Command Line Arguments
```bash
python myreader.py <filename.pdf>
```

**Example:**
```bash
python myreader.py research_paper.pdf
python myreader.py "My Document with Spaces.pdf"
```

## 📖 How It Works

### 1. Voice Selection
When you start the program, you'll be presented with voice selection options:

```
🌍 Language Selection:
1. View all voices grouped by language
2. Select by language first  
3. Use default voice
```

**Option 1** - View all voices:
- Shows voices grouped by language (English, Spanish, French, etc.)
- Each voice is numbered for easy selection
- Displays additional language support for multilingual voices

**Option 2** - Select by language:
- First choose your preferred language
- Then select from voices available in that language
- Ideal when you know the language you want

**Option 3** - Use default:
- Skip voice selection and use system default
- Fastest option to get started

### 2. Voice Testing
After selecting a voice:
- The program will test the voice with a sample phrase
- You can confirm if you like the voice or try another
- Ensures you're happy with the voice before reading long documents

### 3. PDF Processing
- Opens and validates the PDF file
- Extracts text page by page with progress feedback
- Processes and cleans the text for optimal speech
- Shows a preview of the content before reading

### 4. Interactive Reading
Once reading starts, you have full control:
- Type commands while the document is being read
- Commands are processed between sentences
- Real-time feedback for all adjustments

## 🎮 Interactive Commands

### Playback Control
| Command | Aliases | Description |
|---------|---------|-------------|
| `pause` | `p` | Pause/resume reading |
| `stop` | `s` | Stop reading completely |
| `restart` | `r` | Restart from beginning |
| `quit` | `q` | Exit the program |

### Audio Adjustment  
| Command | Aliases | Description |
|---------|---------|-------------|
| `faster` | `+` | Increase reading speed (+20 WPM) |
| `slower` | `-` | Decrease reading speed (-20 WPM) |
| `louder` | `up` | Increase volume (+10%) |
| `quieter` | `down` | Decrease volume (-10%) |

### Information
| Command | Aliases | Description |
|---------|---------|-------------|
| `help` | `h` | Show all available commands |
| *(empty)* | | Continue without command |

### Speed and Volume Ranges
- **Speed**: 100-300 WPM (Words Per Minute)
- **Volume**: 0-100%
- **Default Speed**: 180 WPM
- **Default Volume**: 100%

## 🌍 Language Support

The program automatically detects and organizes all system-installed voices by language:

### Commonly Supported Languages
- **English**: US, UK, Australian, Canadian variants
- **Spanish**: Spain, Mexico, and other regional variants  
- **French**: France, Canadian variants
- **German**: Standard German voices
- **Italian**: Italian voices
- **Portuguese**: Brazil, Portugal variants
- **Chinese**: Simplified and Traditional
- **Japanese**: Japanese voices
- **Korean**: Korean voices
- **Arabic**: Arabic voices
- **Hindi**: Hindi voices
- **Russian**: Russian voices
- **And many more...**

### Adding More Voices

#### macOS
1. Go to **System Preferences** > **Accessibility** > **Speech**
2. Click **System Voice** dropdown
3. Select **Customize...**
4. Download additional voices

#### Windows  
1. Go to **Settings** > **Time & Language** > **Speech**
2. Under **Manage voices**, click **Add voices**
3. Download voices from Microsoft Store

#### Linux
Install additional espeak voice packages:
```bash
sudo apt-get install espeak-data-*
```

## 🛠️ Troubleshooting

### Common Issues

#### "No voices available"
- **macOS**: Check System Preferences > Accessibility > Speech
- **Windows**: Ensure Windows Speech Platform is installed
- **Linux**: Install espeak: `sudo apt-get install espeak`

#### "TTS engine failed to initialize"
- Restart the program
- Check if other applications are using audio
- On Linux, ensure audio drivers are working

#### "File not found"
- Verify the PDF file path is correct
- Use quotes around filenames with spaces
- Ensure the file has read permissions

#### "No text extracted"
- PDF might be image-based (scanned document)
- Try using OCR software first to convert images to text
- PDF might be password-protected or encrypted

#### Voice cuts out or stutters
- Try a different voice
- Reduce reading speed with `slower` command
- Close other audio applications

### Performance Tips

#### For Large PDFs
- The program processes PDFs page by page
- Very large files may take time to load initially
- Consider splitting extremely large PDFs

#### For Better Audio Quality
- Use higher-quality voices (typically found on macOS)
- Adjust speed to comfortable listening pace
- Use headphones for better audio experience

#### For Different Languages
- Install native language voices for best pronunciation
- Test voices before reading long documents
- Some voices handle mixed-language text better than others

## 📁 File Structure

```
pdf-reader/
├── myreader.py          # Main program file
├── README.md           # This documentation
└── sample_docs/        # (Optional) Sample PDF files
    ├── test.pdf
    └── example.pdf
```

## 🔧 Technical Details

### Dependencies
- **pyttsx3**: Cross-platform text-to-speech library
- **PyPDF2**: PDF processing and text extraction
- **threading**: For non-blocking input handling
- **select**: Unix-style input availability checking
- **re**: Regular expressions for text processing

### Architecture
- **ReadMyText Class**: Main application class
- **Voice Management**: Handles voice detection, grouping, and selection
- **Text Processing**: Cleans and segments text for optimal speech
- **Control System**: Real-time command processing during playback
- **PDF Processing**: Robust text extraction with error handling

### Platform Compatibility
- **Cross-platform**: Works on macOS, Windows, and Linux
- **Voice Quality**: Best on macOS, good on Windows, basic on Linux
- **Input Handling**: Advanced on Unix-like systems, basic on Windows

## 🤝 Contributing

### Reporting Issues
If you encounter bugs or have feature requests:
1. Check existing issues first
2. Provide detailed error messages
3. Include your operating system and Python version
4. Attach sample PDF if the issue is file-specific

### Feature Requests
Popular feature requests:
- Bookmark support for long documents
- Multiple file queue
- Export audio to file
- GUI interface
- OCR integration for image-based PDFs

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 👨‍💻 Author

**Nelson Soh**  
*AI/ML Research Engineer*

Passionate about creating accessible technology solutions that bridge the gap between complex documents and audio learning. This project combines AI/ML expertise with practical accessibility tools to enhance document consumption for diverse learning styles.

## 🙏 Acknowledgments

- Built with [pyttsx3](https://pyttsx3.readthedocs.io/) for text-to-speech
- Uses [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing
- Inspired by accessibility needs and audio learning preferences

---

**Made with ❤️ for better document accessibility by Nelson Soh**

*Happy Reading! 🔊📚*