# Voice Assistant-Based Attendance Monitoring System

## Description
The Voice Assistant-Based Attendance Monitoring System is an innovative application that leverages speech recognition to simplify attendance tracking. Users can mark their attendance by speaking their names, which are recognized and recorded in real-time. The system maintains a database of attendance records and provides options to view or clear the data.

## Features
- **Voice Recognition**: Allows users to mark attendance by speaking their names.
- **Database Integration**: Stores attendance records in an SQLite database with timestamps.
- **Real-Time Feedback**: Notifies users when attendance is successfully marked.
- **Error Handling**: Prompts users to retry if voice input is not recognized.
- **Attendance Report**: Generates a detailed view of attendance records.
- **Data Management**: Provides options to clear attendance data.

## Requirements
- Python 3.x
- Libraries:
  - `tkinter` (for the GUI)
  - `speech_recognition` (for voice input)
  - `sqlite3` (for database management)

## Setup Instructions
1. Ensure Python 3.x is installed on your system.
2. Install the required libraries using:
   ```bash
   pip install SpeechRecognition
   ```
3. Clone the repository or copy the script to your local system.
4. Run the script using:
   ```bash
   python voice_assistant_attendance.py
   ```

## Usage
1. **Mark Attendance**:
   - Click on the "Mark Attendance" button.
   - Speak your name when prompted.
   - If recognized, your attendance will be recorded.

2. **View Attendance**:
   - Click on the "View Attendance" button.
   - A new window will display the attendance records.

3. **Clear Data**:
   - Click on the "Clear Data" button to delete all attendance records.

4. **Exit**:
   - Click on the "Exit" button to close the application.

## Notes
- Ensure your microphone is functional and accessible by the application.
- Maintain a quiet environment for better accuracy in voice recognition.
- The application uses Google’s Speech Recognition API for processing audio input.

## Future Enhancements
- Add integration with cloud databases for centralized data management.
- Implement voice authentication for enhanced security.
- Generate attendance summary reports for specific dates or periods.

## License
This project is open-source and available under the MIT License.
