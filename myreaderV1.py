import pyttsx3
import sys
import PyPDF2
import os
import threading
import time
import select
import sys
from collections import defaultdict


class ReadMyText:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.is_paused = False
        self.should_stop = False
        self.should_restart = False
        self.current_text = ""
        self.current_sentence_index = 0
        self.sentences = []
        self.rate = 180
        self.volume = 1.0
        self.selected_voice = None
        self.available_voices = []
        self.voices_by_language = defaultdict(list)

    def initialize_engine(self):
        """Initialize TTS engine - called per sentence to avoid threading issues"""
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.rate)
            engine.setProperty("volume", self.volume)
            
            # Set selected voice if available
            if self.selected_voice:
                engine.setProperty('voice', self.selected_voice)
                
            return engine
        except Exception as e:
            print(f"Unable to initialize TTS engine: {e}")
            return None

    def get_available_voices(self):
        """Get all available system voices and group them by language"""
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            self.available_voices = []
            self.voices_by_language = defaultdict(list)
            
            if voices:
                for i, voice in enumerate(voices):
                    # Clean up voice info for better display
                    voice_name = voice.name if voice.name else f"Voice {i+1}"
                    voice_id = voice.id
                    languages = voice.languages if voice.languages else ["Unknown"]
                    
                    voice_info = {
                        'index': i,
                        'id': voice_id,
                        'name': voice_name,
                        'languages': languages
                    }
                    
                    self.available_voices.append(voice_info)
                    
                    # Group by primary language
                    primary_language = self.get_primary_language(languages)
                    self.voices_by_language[primary_language].append(voice_info)
            
            # Clean up temp engine
            try:
                temp_engine.stop()
                del temp_engine
            except:
                pass
                
            return len(self.available_voices) > 0
            
        except Exception as e:
            print(f"❌ Error getting voices: {e}")
            return False

    def get_primary_language(self, languages):
        """Extract and clean primary language from language list"""
        if not languages or languages == ["Unknown"]:
            return "Unknown"
        
        primary = languages[0]
        
        # Common language mappings for cleaner display
        language_mappings = {
            'en_US': 'English (US)',
            'en_GB': 'English (UK)',
            'en_AU': 'English (AU)',
            'en_CA': 'English (CA)',
            'es_ES': 'Spanish (Spain)',
            'es_MX': 'Spanish (Mexico)',
            'fr_FR': 'French (France)',
            'fr_CA': 'French (Canada)',
            'de_DE': 'German',
            'it_IT': 'Italian',
            'pt_BR': 'Portuguese (Brazil)',
            'pt_PT': 'Portuguese (Portugal)',
            'ru_RU': 'Russian',
            'ja_JP': 'Japanese',
            'ko_KR': 'Korean',
            'zh_CN': 'Chinese (Simplified)',
            'zh_TW': 'Chinese (Traditional)',
            'ar_SA': 'Arabic',
            'hi_IN': 'Hindi',
            'th_TH': 'Thai',
            'sv_SE': 'Swedish',
            'no_NO': 'Norwegian',
            'da_DK': 'Danish',
            'fi_FI': 'Finnish',
            'pl_PL': 'Polish',
            'nl_NL': 'Dutch',
            'tr_TR': 'Turkish'
        }
        
        # Try to map to cleaner name
        if primary in language_mappings:
            return language_mappings[primary]
        
        # If not in mapping, try to extract language code
        if '_' in primary:
            lang_code = primary.split('_')[0].upper()
            country_code = primary.split('_')[1].upper()
            return f"{lang_code} ({country_code})"
        
        # Return as-is if no pattern matches
        return primary.title()

    def display_voices_grouped(self):
        """Display available voices grouped by language"""
        print("\n🌍 Available Voices (Grouped by Language):")
        print("=" * 60)
        
        # Sort languages for consistent display
        sorted_languages = sorted(self.voices_by_language.keys())
        
        voice_counter = 1
        for language in sorted_languages:
            voices = self.voices_by_language[language]
            
            print(f"\n📢 {language} ({len(voices)} voice{'s' if len(voices) != 1 else ''})")
            print("-" * 40)
            
            for voice in voices:
                # Show additional languages if voice supports multiple
                additional_langs = ""
                if len(voice['languages']) > 1:
                    other_langs = [self.get_primary_language([lang]) for lang in voice['languages'][1:3]]
                    if other_langs:
                        additional_langs = f" (also: {', '.join(other_langs)})"
                        if len(voice['languages']) > 3:
                            additional_langs += "..."
                
                print(f"{voice_counter:2d}. {voice['name']}{additional_langs}")
                voice_counter += 1
            
        print(f"\n📊 Total: {len(self.available_voices)} voices in {len(sorted_languages)} language groups")

    def display_voices_by_language(self, target_language=None):
        """Display voices for a specific language"""
        if target_language and target_language in self.voices_by_language:
            voices = self.voices_by_language[target_language]
            print(f"\n🎙️  {target_language} Voices:")
            print("-" * 40)
            
            for i, voice in enumerate(voices, 1):
                additional_langs = ""
                if len(voice['languages']) > 1:
                    other_langs = voice['languages'][1:3]
                    if other_langs:
                        additional_langs = f" (+{', '.join(other_langs)})"
                        if len(voice['languages']) > 3:
                            additional_langs += "..."
                
                print(f"{i}. {voice['name']}{additional_langs}")
            
            return voices
        return []

    def select_voice(self):
        """Let user select a voice with language grouping"""
        if not self.get_available_voices():
            print("⚠️  No voices available or unable to detect voices")
            return False

        # Check if running on macOS
        import platform
        is_mac = platform.system() == "Darwin"
        
        if not is_mac:
            print("ℹ️  Voice selection is optimized for Mac users")
        
        print(f"🎙️  Found {len(self.available_voices)} voices in {len(self.voices_by_language)} languages")
        
        try:
            while True:
                print("\n🌍 Language Selection:")
                print("1. View all voices grouped by language")
                print("2. Select by language first")
                print("3. Use default voice")
                
                choice = input("\nChoose option (1-3): ").strip()
                
                if choice == "1":
                    self.display_voices_grouped()
                    return self.select_from_all_voices()
                
                elif choice == "2":
                    return self.select_by_language()
                
                elif choice == "3":
                    print("✅ Using default system voice")
                    return True
                
                else:
                    print("❌ Please enter 1, 2, or 3")
                    
        except KeyboardInterrupt:
            print("\n⏭️  Skipping voice selection, using default")
            return True

    def select_by_language(self):
        """Select voice by choosing language first"""
        print("\n🌍 Available Languages:")
        print("-" * 30)
        
        sorted_languages = sorted(self.voices_by_language.keys())
        for i, language in enumerate(sorted_languages, 1):
            voice_count = len(self.voices_by_language[language])
            print(f"{i:2d}. {language} ({voice_count} voice{'s' if voice_count != 1 else ''})")
        
        try:
            while True:
                choice = input(f"\nSelect language (1-{len(sorted_languages)}) or 'back': ").strip().lower()
                
                if choice == 'back':
                    return self.select_voice()
                
                try:
                    lang_index = int(choice) - 1
                    if 0 <= lang_index < len(sorted_languages):
                        selected_language = sorted_languages[lang_index]
                        return self.select_voice_from_language(selected_language)
                    else:
                        print(f"❌ Please enter a number between 1 and {len(sorted_languages)}")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
                    
        except KeyboardInterrupt:
            print("\n⏭️  Using default voice")
            return True

    def select_voice_from_language(self, language):
        """Select a specific voice from chosen language"""
        voices = self.display_voices_by_language(language)
        
        try:
            while True:
                choice = input(f"\nSelect voice (1-{len(voices)}) or 'back': ").strip().lower()
                
                if choice == 'back':
                    return self.select_by_language()
                
                try:
                    voice_index = int(choice) - 1
                    if 0 <= voice_index < len(voices):
                        selected_voice = voices[voice_index]
                        return self.test_and_confirm_voice(selected_voice)
                    else:
                        print(f"❌ Please enter a number between 1 and {len(voices)}")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
                    
        except KeyboardInterrupt:
            print("\n⏭️  Using default voice")
            return True

    def select_from_all_voices(self):
        """Select voice from the numbered list of all voices"""
        try:
            while True:
                choice = input(f"\n🎙️  Select voice (1-{len(self.available_voices)}) or 'back': ").strip().lower()
                
                if choice == 'back':
                    return self.select_voice()
                
                try:
                    voice_index = int(choice) - 1
                    if 0 <= voice_index < len(self.available_voices):
                        selected_voice = self.available_voices[voice_index]
                        return self.test_and_confirm_voice(selected_voice)
                    else:
                        print(f"❌ Please enter a number between 1 and {len(self.available_voices)}")
                except ValueError:
                    print("❌ Please enter a valid number or 'back'")
                    
        except KeyboardInterrupt:
            print("\n⏭️  Using default voice")
            return True

    def test_and_confirm_voice(self, selected_voice):
        """Test selected voice and confirm with user"""
        self.selected_voice = selected_voice['id']
        
        print(f"✅ Selected voice: {selected_voice['name']}")
        
        # Test the selected voice
        print("🎤 Testing selected voice...")
        test_engine = self.initialize_engine()
        if test_engine:
            test_engine.say("Hello! This is how I will sound when reading your PDF.")
            test_engine.runAndWait()
            try:
                test_engine.stop()
                del test_engine
            except:
                pass
        
        try:
            confirm = input("👍 Keep this voice? (y/n): ").lower().strip()
            if confirm in ['y', 'yes', '']:
                return True
            else:
                print("🔄 Let's try another voice...\n")
                return self.select_voice()
        except KeyboardInterrupt:
            print("\n⏭️  Using this voice")
            return True

    def show_controls(self):
        """Display available controls"""
        print("\n🎮 Controls (type command + Enter):")
        print("  'pause' or 'p' - Pause/Resume")
        print("  'stop' or 's' - Stop reading")
        print("  'faster' or '+' - Increase speed")
        print("  'slower' or '-' - Decrease speed")
        print("  'louder' or 'up' - Increase volume")
        print("  'quieter' or 'down' - Decrease volume")
        print("  'restart' or 'r' - Restart from beginning")
        print("  'quit' or 'q' - Quit")
        print("  'help' or 'h' - Show this help")
        print("  '' (just Enter) - Continue without command")
        print("-" * 50)

    def adjust_speed(self, increase=True):
        """Adjust reading speed"""
        if increase:
            self.rate = min(self.rate + 20, 300)  # Max 300 WPM
        else:
            self.rate = max(self.rate - 20, 100)  # Min 100 WPM
        
        print(f"🔧 Speed set to {self.rate} WPM")

    def adjust_volume(self, increase=True):
        """Adjust volume"""
        if increase:
            self.volume = min(self.volume + 0.1, 1.0)
        else:
            self.volume = max(self.volume - 0.1, 0.0)
        
        print(f"🔊 Volume set to {int(self.volume * 100)}%")

    def has_input_available(self):
        """Check if input is available without blocking (Unix/Linux/Mac)"""
        try:
            # This works on Unix-like systems
            if hasattr(select, 'select'):
                ready, _, _ = select.select([sys.stdin], [], [], 0)
                return bool(ready)
        except:
            pass
        return False

    def get_non_blocking_input(self):
        """Get input without blocking if available"""
        try:
            if self.has_input_available():
                return input().strip().lower()
        except:
            pass
        return None

    def prepare_text(self, text):
        """Prepare text by splitting into sentences"""
        # Clean text
        clean_text = text.replace('\n', ' ').replace('\r', ' ')
        clean_text = ' '.join(clean_text.split())  # Remove extra whitespace
        
        # Split into sentences
        import re
        sentences = re.split(r'([.!?]+)', clean_text)
        
        # Rejoin sentences with their punctuation
        self.sentences = []
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i].strip()
            if i+1 < len(sentences):
                sentence += sentences[i+1]
            if sentence.strip() and len(sentence.strip()) > 5:  # Filter very short fragments
                self.sentences.append(sentence.strip())
        
        self.current_sentence_index = 0
        print(f"📝 Prepared {len(self.sentences)} sentences for reading")

    def speak_sentence(self, sentence):
        """Speak a single sentence with fresh engine instance"""
        try:
            # Create fresh engine for each sentence to avoid threading issues
            engine = self.initialize_engine()
            if not engine:
                return False
            
            engine.say(sentence)
            engine.runAndWait()
            
            # Clean up engine
            try:
                engine.stop()
                del engine
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"❌ Error speaking sentence: {e}")
            return False

    def handle_command(self, command):
        """Handle user commands"""
        if not command:
            return True  # Continue
            
        if command in ['pause', 'p']:
            self.is_paused = not self.is_paused
            if self.is_paused:
                print("⏸️  Paused - type 'pause' or 'p' to resume")
            else:
                print("▶️  Resumed")
                
        elif command in ['stop', 's']:
            self.should_stop = True
            print("⏹️  Stopping...")
            
        elif command in ['faster', '+']:
            self.adjust_speed(True)
            
        elif command in ['slower', '-']:
            self.adjust_speed(False)
            
        elif command in ['louder', 'up']:
            self.adjust_volume(True)
            
        elif command in ['quieter', 'down']:
            self.adjust_volume(False)
            
        elif command in ['restart', 'r']:
            self.should_restart = True
            print("🔄 Restarting from beginning...")
            
        elif command in ['quit', 'q']:
            self.should_stop = True
            print("👋 Quitting...")
            return False
            
        elif command in ['help', 'h']:
            self.show_controls()
            
        else:
            print(f"❓ Unknown command: '{command}'. Type 'help' for commands.")
            
        return True

    def speak_text_with_controls(self, text):
        """Main speech function with control handling"""
        self.current_text = text
        self.prepare_text(text)
        self.is_speaking = True
        self.should_stop = False
        self.should_restart = False

        print("🔊 Starting to read...")
        print("💡 Type commands while reading (try 'help' for options)")
        print("-" * 50)

        try:
            while (self.current_sentence_index < len(self.sentences) and 
                   not self.should_stop):
                
                # Handle restart
                if self.should_restart:
                    self.current_sentence_index = 0
                    self.should_restart = False
                    print("🔄 Restarted from beginning")
                    continue

                # Handle pause
                while self.is_paused and not self.should_stop and not self.should_restart:
                    print("   ⏸️  [PAUSED] Type 'pause' to resume...")
                    
                    # Wait for user input while paused
                    try:
                        command = input(">>> ").strip().lower()
                        if not self.handle_command(command):
                            return
                    except KeyboardInterrupt:
                        self.should_stop = True
                        break
                    except:
                        time.sleep(0.1)

                if self.should_stop or self.should_restart:
                    continue

                # Show current progress
                progress = f"[{self.current_sentence_index + 1}/{len(self.sentences)}]"
                sentence = self.sentences[self.current_sentence_index]
                
                print(f"\n{progress} Speaking: {sentence[:80]}{'...' if len(sentence) > 80 else ''}")
                
                # Speak the sentence
                if not self.speak_sentence(sentence):
                    break

                self.current_sentence_index += 1
                
                # Check for commands between sentences
                command = self.get_non_blocking_input()
                if command is not None:
                    if not self.handle_command(command):
                        break
                
                # Small pause between sentences
                time.sleep(0.3)

            if not self.should_stop:
                print("\n✅ Finished reading the entire document!")
                # Ask if user wants to restart
                try:
                    restart_choice = input("\n🔄 Would you like to restart reading? (y/n): ").lower().strip()
                    if restart_choice in ['y', 'yes']:
                        print("\n🔄 Restarting from the beginning...")
                        self.current_sentence_index = 0
                        self.should_stop = False
                        self.should_restart = False
                        # Recursive call to restart reading
                        self.speak_text_with_controls(self.current_text)
                    else:
                        print("👋 Thanks for using the PDF reader!")
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
            else:
                print("\n⏹️  Reading stopped by user")

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by Ctrl+C")
        except Exception as e:
            print(f"\n❌ Error during reading: {e}")
        finally:
            self.is_speaking = False

    def read_pdf_content(self, file_name):
        """Extract text content from PDF file"""
        try:
            if not os.path.exists(file_name):
                print(f"❌ File '{file_name}' not found!")
                return None

            print(f"📖 Opening PDF: {file_name}")
            with open(file_name, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                print(f"📄 Total pages: {num_pages}")

                full_text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            full_text += f"\n{text}\n"
                        print(f"✅ Processed page {page_num + 1}")
                    except Exception as e:
                        print(f"⚠️  Error processing page {page_num + 1}: {e}")

                if not full_text.strip():
                    print("⚠️  Warning: No text extracted. PDF might be image-based or encrypted.")
                    return None

                return full_text.strip()

        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return None

    def get_file(self):
        """Get filename from command line arguments"""
        if len(sys.argv) == 2:
            filename = sys.argv[1]
            print(f"📁 Target file: {filename}")
            return filename
        else:
            print("❌ Usage: python myreader.py <filename.pdf>")
            print("   Example: python myreader.py document.pdf")
            return None

    def run(self):
        """Main execution method"""
        print("🎤 PDF Text-to-Speech Reader with Language-Grouped Voices")
        print("=" * 60)

        filename = self.get_file()
        if not filename:
            return

        # Test TTS engine and select voice
        test_engine = self.initialize_engine()
        if not test_engine:
            print("❌ TTS engine failed to initialize. Exiting.")
            return
        else:
            print("✅ TTS engine initialized successfully")
            try:
                test_engine.stop()
                del test_engine
            except:
                pass

        # Voice selection with language grouping
        print("\n🎙️  Voice Selection")
        if not self.select_voice():
            print("⚠️  Continuing with default voice")

        text = self.read_pdf_content(filename)
        if not text:
            print("❌ No text to read. Exiting.")
            return

        # Show text preview
        print(f"\n📝 Text preview (first 200 characters):")
        print("-" * 50)
        preview = text[:200].replace('\n', ' ')
        print(f'"{preview}..."' if len(text) > 200 else f'"{preview}"')
        print("-" * 50)

        try:
            confirm = input(f"\n🔊 Ready to read {len(text)} characters? (y/n): ").lower()
            if confirm in ["y", "yes"]:
                self.show_controls()
                self.speak_text_with_controls(text)
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