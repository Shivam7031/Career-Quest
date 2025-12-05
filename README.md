# Career Quest

<div align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini API">
</div>

## 📋 Description

Career Quest is an innovative full-stack web application designed to assist students and professionals in their career development journey. Leveraging machine learning algorithms and AI-powered features, the platform provides personalized course recommendations, interview preparation tools, and educational resources to help users make informed career decisions.

## ✨ Features

- **🎯 Interest-Based Course Recommendations**: Uses machine learning models (Decision Tree, Random Forest, Naive Bayes) to suggest suitable courses based on user interests
- **🤖 AI-Powered Interview Practice**: Generates insightful interview questions using Google's Gemini API and provides feedback on audio responses
- **🔍 Coursera Course Search**: Find similar courses on Coursera using content-based filtering and TF-IDF vectorization
- **🎤 Speech Recognition**: Integrated speech-to-text functionality for interview practice
- **📱 Responsive Design**: Modern, user-friendly interface built with React and TypeScript
- **📊 Data-Driven Insights**: Analyzes student data to predict career paths and course preferences

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Machine Learning**: scikit-learn, pandas, numpy
- **AI Integration**: Google Gemini API
- **Audio Processing**: SpeechRecognition library
- **Data Processing**: TF-IDF Vectorization, Sigmoid Kernel for similarity

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Additional Libraries**: React Speech Recognition, React Webcam

### Database & Storage
- **Data Files**: CSV files for training data and course information
- **File Uploads**: Local storage for audio files

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **Git**

You'll also need:
- A Google Gemini API key (set in `.env` file)
- Required Python packages (listed in `backend/requirements.txt`)
- Node.js dependencies (listed in `frontend/package.json`)

## 🚀 Installation

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the `backend` directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🎯 Usage

### Running the Application

1. **Start the Backend:**
   ```bash
   cd backend
   python app.py
   ```
   The backend will run on `http://localhost:5000`

2. **Start the Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

3. **Access the Application:**
   Open your browser and navigate to `http://localhost:5173`

### Key Features Usage

- **Course Recommendation**: Select your interests and choose an ML algorithm to get personalized course suggestions
- **Interview Practice**: Enter a job domain to generate questions, record your response, and receive AI feedback
- **Course Search**: Search for courses on Coursera and get similar recommendations

## 📡 API Endpoints

The backend provides the following API endpoints:

- `GET /`: Main application route
- `POST /`: Submit interests and algorithm for course prediction
- `GET /generate-questions`: Serve Gemini question generation page
- `POST /api/get-questions`: Generate interview questions for a domain
- `POST /api/submit-audio`: Submit audio for AI feedback analysis
- `GET /courses_main`: Display course information
- `GET /api/courses`: Retrieve courses for a specific degree
- `GET /coursera`: Coursera course search page
- `POST /predict`: Search for similar Coursera courses

## 🤝 Contributing

We welcome contributions to Career Quest! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI-powered features
- Coursera for course data
- Open-source community for the amazing libraries used

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">
  <p>Made with ❤️ for career guidance</p>
</div>
