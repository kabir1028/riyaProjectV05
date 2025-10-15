# AI-Powered Resume Mock Interviewer

A complete web application that provides AI-style mock interviews based on uploaded resumes and chosen job roles. Built with HTML, CSS, JavaScript frontend and Python Flask backend.

## Features

- **Interactive Mock Interviews**: Take personalized interviews with 10 questions (5 multiple-choice, 5 short-answer)
- **Role-Specific Questions**: Choose from Software Engineer, AI Scientist, or Data Scientist roles
- **Difficulty Levels**: Beginner, Intermediate, and Advanced question sets
- **Performance Analysis**: Get detailed feedback and improvement suggestions
- **Company Recommendations**: Receive company suggestions based on your performance
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
resume-mock-interviewer/
├── app.py                 # Flask backend application
├── data/
│   └── questions.json     # Question database
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       ├── main.js        # Common JavaScript functions
│       ├── interview.js   # Interview page logic
│       └── results.js     # Results page logic
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── start_interview.html # Interview setup page
│   ├── interview.html     # Interview questions page
│   └── results.html       # Results and feedback page
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd resume-mock-interviewer
   ```

2. **Install Flask**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## How to Use

1. **Home Page**: Start by clicking "Start Interview" or create an account
2. **Setup Interview**: 
   - Upload your resume (optional)
   - Select your target job role
   - Choose difficulty level
3. **Take Interview**: Answer 10 questions one by one
4. **View Results**: Get your score, feedback, and company recommendations

## Technical Details

### Backend (Flask)
- **Routes**: Home, login, signup, interview setup, questions, results
- **API Endpoints**: 
  - `/api/questions` - Fetch questions based on role and difficulty
  - `/api/submit-answers` - Submit answers and get performance analysis
- **Scoring Logic**: Calculates score based on correct answers and response quality

### Frontend
- **HTML5**: Semantic markup with responsive design
- **CSS3**: Modern styling with blue (#007BFF), green (#28A745), white color scheme
- **JavaScript**: Interactive features, form validation, AJAX calls

### Question Database
- **Format**: JSON structure organized by role and difficulty
- **Types**: Multiple-choice (with correct answers) and short-answer questions
- **Coverage**: 10 questions per role/difficulty combination

## Customization

### Adding New Questions
Edit `data/questions.json` to add more questions:

```json
{
  "Role Name": {
    "Difficulty Level": [
      {
        "question": "Your question here",
        "type": "multiple-choice",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correctAnswer": 0
      }
    ]
  }
}
```

### Adding New Roles
1. Add questions in `questions.json`
2. Update the role dropdown in `start_interview.html`
3. Update company recommendations in `app.py`

### Styling Changes
Modify `static/css/style.css` to change colors, fonts, or layout.

## Future Enhancements

- User authentication and session management
- Resume parsing and analysis
- Voice interview functionality
- Advanced AI-powered question generation
- Detailed analytics and progress tracking
- Integration with job boards and company APIs

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, contact: info@mockinterviewer.com

---

**Note**: This is a demo application. Login/signup functionality is placeholder and resume upload is UI-only. The scoring system uses mock logic for demonstration purposes.