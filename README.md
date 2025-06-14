# PDF Text-to-Speech Reader

A Python application that extracts text from PDF files and reads it aloud using text-to-speech technology.

## Features

- 📄 Extract text from PDF files
- 🔊 Convert text to speech with customizable settings
- 📖 Page-by-page processing with progress tracking
- ✅ User confirmation before reading
- 🛡️ Comprehensive error handling
- 📱 Command-line interface

## Requirements

### Python Version
- Python 3.6 or higher

### Dependencies
```bash
pip install pyttsx3 PyPDF2
```

## Installation

1. **Clone or download the script:**
   ```bash
   # Save the script as 'myreader.py'
   ```

2. **Install required packages:**
   ```bash
   pip install pyttsx3 PyPDF2
   ```

3. **Verify installation:**
   ```bash
   python myreader.py
   ```

## Usage

### Basic Usage
```bash
python myreader.py <filename.pdf>
```

### Examples
```bash
# Read a document in the same directory
python myreader.py document.pdf

# Read a document with full path
python myreader.py /path/to/your/document.pdf

# Read a document in a subdirectory
python myreader.py documents/report.pdf
```

### Interactive Flow
1. Run the command with your PDF file
2. The program will show:
   - Total number of pages
   - Processing progress for each page
   - Text preview (first 200 characters)
3. Confirm whether you want to proceed with reading
4. The program will read the entire document aloud

## Configuration

The TTS engine comes with default settings that can be modified in the code:

```python
engine.setProperty("rate", 180)    # Speech rate (words per minute)
engine.setProperty("volume", 0.9)  # Volume level (0.0 to 1.0)
```

### Customizing Speech Settings
To change the speech rate or volume, modify these values in the `initialize_engine()` method:
- **Rate**: 150-200 is normal, 100-150 is slower, 200+ is faster
- **Volume**: 0.0 (silent) to 1.0 (maximum volume)

## File Support

### Supported Formats
- ✅ Text-based PDF files
- ✅ PDF files with selectable text

### Not Supported
- ❌ Image-based PDFs (scanned documents)
- ❌ Password-protected/encrypted PDFs
- ❌ Other file formats (only PDF)

## Error Handling

The application handles various error scenarios:
- **File not found**: Clear error message with usage instructions
- **Empty/image-based PDFs**: Warning about no extractable text
- **TTS initialization failure**: Graceful fallback with error message
- **Keyboard interruption**: Clean exit with goodbye message

## Troubleshooting

### Common Issues

**1. "TTS engine failed to initialize"**
```bash
# Try installing/reinstalling pyttsx3
pip uninstall pyttsx3
pip install pyttsx3
```

**2. "No text extracted" from PDF**
- The PDF might be image-based (scanned document)
- Try using OCR software to convert it to text-based PDF first
- Check if the PDF is password-protected

**3. "File not found" error**
- Verify the file path is correct
- Use quotes around filenames with spaces: `"my document.pdf"`
- Check file permissions

**4. Speech sounds robotic or unclear**
- Adjust the speech rate in the code (try 150-180)
- Some system TTS voices are better than others

### Platform-Specific Notes

**Windows**: Usually works out of the box with SAPI5
**macOS**: Uses system speech synthesis
**Linux**: May require additional TTS engines like `espeak`

## Example Output

```
🎤 PDF Text-to-Speech Reader
==============================
📁 Target file: example.pdf

📖 Reading PDF: Passage1.pdf
📄 Total pages: 5
✅ Processed page 1
✅ Processed page 2
✅ Processed page 3
✅ Processed page 4
✅ Processed page 5

📝 Text preview (first 200 characters):
----------------------------------------
Chapter 1: Introduction
This document contains important information about...
----------------------------------------

🔊 Ready to read 2847 characters? (y/n): y
🔊 Starting to read...
✅ Finished reading! Thank You!
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

### Potential Enhancements
- Support for other document formats (DOCX, TXT)
- OCR integration for image-based PDFs
- GUI interface
- Voice selection options
- Reading speed controls during playback
- Bookmark/chapter navigation

## License

This project is open source. Feel free to use and modify as needed.

## Acknowledgments

- Built with [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech
- Uses [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction


