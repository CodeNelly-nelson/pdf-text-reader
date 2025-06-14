import pyttsx3
import sys
import PyPDF2
import os


class ReadMyText:
    def __init__(self):
        self.engine = self.initialize_engine()

    def initialize_engine(
        self,
    ):  # FIXED: Removed 'cls' parameter - this is an instance method
        """This function initializes the TTS engine"""
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)
            return engine  # FIXED: Return the engine, not cls(engine)
        except Exception as e:
            print(f"Unable to initialize TTS engine: {e}")
            return None

    def speak_text(self, text):
        """Speak the provided text using TTS"""
        if self.engine is None:
            print("TTS not available, skipping speech...")
            return

        try:
            print("🔊 Starting to read...")
            self.engine.say(text)
            self.engine.runAndWait()
            print("✅ Finished reading! Thank You!")
        except Exception as e:
            print(f"❌ Error speaking message: {e}")

    def read_pdf_content(self, file_name):
        """Extract text content from PDF file"""
        try:
            # Check if file exists first
            if not os.path.exists(file_name):
                print(f"❌ File '{file_name}' not found!")
                return None

            # Create PDF reader object
            with open(file_name, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Get basic info
                num_pages = len(pdf_reader.pages)
                print(f"📄 Total pages: {num_pages}")

                # Extract text from all pages
                full_text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
                    print(f"✅ Processed page {page_num + 1}")

                # Check if we got any text
                if not full_text.strip():
                    print(
                        "⚠️  Warning: No text extracted. PDF might be image-based or encrypted."
                    )
                    return None

                return full_text

        except FileNotFoundError:
            print("❌ File not found!")
            return None
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return None

    def get_file(self):
        """Get filename from command line arguments"""
        try:
            if len(sys.argv) == 2:
                filename = sys.argv[1]
                print(f"📁 Target file: {filename}")
                return filename
            else:
                print("❌ Usage: python myreader.py <filename.pdf>")
                print("   Example: python myreader.py document.pdf")
                return None
        except Exception as e:
            print(f"❌ Error getting filename: {e}")
            return None

    def run(self):
        """Main execution method"""
        print("🎤 PDF Text-to-Speech Reader")
        print("=" * 30)

        # Get the file to read
        filename = self.get_file()
        if not filename:
            return

        # Check if engine initialized properly
        if not self.engine:
            print("❌ TTS engine failed to initialize. Exiting.")
            return

        # Read PDF content
        print(f"\n📖 Reading PDF: {filename}")
        text = self.read_pdf_content(filename)

        if not text:
            print("❌ No text to read. Exiting.")
            return

        # Show text preview
        print(f"\n📝 Text preview (first 200 characters):")
        print("-" * 40)
        print(text[:200] + "..." if len(text) > 200 else text)
        print("-" * 40)

        # Ask user confirmation
        try:
            confirm = input(
                f"\n🔊 Ready to read {len(text)} characters? (y/n): "
            ).lower()
            if confirm in ["y", "yes"]:
                self.speak_text(text)
            else:
                print("👋 Reading cancelled.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")


def main():
    """Main function"""
    try:
        reader = ReadMyText()
        reader.run()
    except KeyboardInterrupt:
        print("\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
