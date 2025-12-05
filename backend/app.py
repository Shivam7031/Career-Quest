from flask import Flask, render_template, request, jsonify
import os
import requests
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import speech_recognition as sr
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import difflib
from markupsafe import Markup

load_dotenv()




def create_sim(search):
    df_org=pd.read_csv('Courser.csv')
    df=df_org.copy()
    df.drop(['University','Difficulty Level','Course Rating','Course URL','Course Description'], axis=1,inplace=True)
    tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

    # Filling NaNs with empty string
    df['cleaned'] = df['Skills'].fillna('')
    # Fitting the TF-IDF on the 'cleaned' text
    tfv_matrix = tfv.fit_transform(df['cleaned'])
    # Compute the sigmoid kernel
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    # Reverse mapping of indices and titles
    indices = pd.Series(df.index, index=df['Course Name']).drop_duplicates()
    
    def give_rec(title, sig=sig):
        # Get the index corresponding to original_title
        idx = indices[title]

        # Get the pairwsie similarity scores 
        sig_scores = list(enumerate(sig[idx]))

        # Sort the courses
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar courses
        sig_scores = sig_scores[1:11]

        # courses indices
        course_indices = [i[0] for i in sig_scores]

        # Top 10 most similar courses
        return df_org.iloc[course_indices]

    namelist=df['Course Name'].tolist()
    word=search
    simlist=difflib.get_close_matches(word, namelist)
    try: 
        findf=give_rec(simlist[0])
        findf=findf.reset_index(drop=True)
    except:
        findf=pd.DataFrame()
    
    return findf




app = Flask(__name__)

# ===================== GEMINI API CONFIGURATION =====================
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with your actual API key

# ===================== ROUTES FOR GEMINI QUESTION GENERATION =====================
@app.route('/generate-questions')
def gemini_index():
    return render_template('index2.html')  # Serve index2.html for Gemini functionality

def get_questions_from_gemini(domain):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate only 1 insightful interview question for a {domain} role."
                    }
                ]
            }
        ]
    }
    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload)
    if response.status_code == 200:
        questions = response.json().get('candidates', [])
        return [question['content']['parts'][0]['text'] for question in questions[:5]]
    else:
        print("API Error Response:", response.json())
        return ["Error: Could not generate questions."]

@app.route('/api/get-questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    domain = data.get('domain', '').strip()
    if not domain:
        return jsonify({"error": "Domain cannot be empty."}), 400
    questions = get_questions_from_gemini(domain)
    return jsonify({"questions": questions})

# ===================== AUDIO PROCESSING AND GEMINI FEEDBACK =====================
def analyze_audio_with_gemini(audio_file, question):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    audio_path = os.path.join(upload_dir, audio_file.filename)
    audio_file.save(audio_path)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcribed_text = "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        transcribed_text = f"Speech recognition service error: {e}"
    except ValueError:
        transcribed_text = "Error: Audio file could not be processed."
    os.remove(audio_path)

    feedback_prompt = (
        f"Please evaluate the following response to the interview question, give short answer as you can in only 1 para "
        f"focusing on weaknesses, and suggestions for improvement.\n\n"
        f"Question: {question}\n\n"
        f"Transcribed Response: {transcribed_text}\n\n"
        "1. Weaknesses: Highlight areas for improvement.\n"
        "2. Suggestions: Provide actionable advice for improvement."
    )

    feedback_payload = {
        "contents": [
            {
                "parts": [{"text": feedback_prompt}]
            }
        ]
    }

    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=feedback_payload)
    if response.status_code == 200:
        feedback = response.json().get('candidates', [])[0].get('content', {}).get('parts', [{}])[0].get('text', "No feedback available.")
        return feedback
    else:
        print("API Error Response:", response.json())
        return f"Error: {response.json().get('message', 'Failed to process audio.')}"

@app.route('/api/submit-audio', methods=['POST'])
def submit_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    audio_file = request.files['audio']
    question = request.form.get('question', '')
    feedback = analyze_audio_with_gemini(audio_file, question)
    return jsonify({"feedback": feedback})

# ===================== COURSE SUGGESTION SYSTEM =====================
l1 = ['Drawing', 'Dancing', 'Singing', 'Sports', 'Video Game', 'Acting', 'Travelling',
      'Gardening', 'Animals', 'Photography', 'Teaching', 'Exercise', 'Coding',
      'Electricity Components', 'Mechanic Parts', 'Computer Parts', 'Researching',
      'Architecture', 'Historic Collection', 'Botany', 'Zoology', 'Physics',
      'Accounting', 'Economics', 'Sociology', 'Geography', 'Psycology', 'History',
      'Science', 'Bussiness Education', 'Chemistry', 'Mathematics', 'Biology',
      'Makeup', 'Designing', 'Content writing', 'Crafting', 'Literature', 'Reading',
      'Cartooning', 'Debating', 'Asrtology', 'Hindi', 'French', 'English',
      'Other Language', 'Solving Puzzles', 'Gymnastics', 'Yoga', 'Engeeniering',
      'Doctor', 'Pharmisist', 'Cycling', 'Knitting', 'Director', 'Journalism',
      'Bussiness', 'Listening Music']

Course = ['BBA- Bachelor of Business Administration',
          'BEM- Bachelor of Event Management',
          'Integrated Law Course- BA + LL.B',
          'BJMC- Bachelor of Journalism and Mass Communication',
          'BFD- Bachelor of Fashion Designing',
          'BBS- Bachelor of Business Studies',
          'BTTM- Bachelor of Travel and Tourism Management',
          'BVA- Bachelor of Visual Arts',
          'BA in History', 'B.Arch- Bachelor of Architecture',
          'BCA- Bachelor of Computer Applications',
          'B.Sc.- Information Technology',
          'B.Sc- Nursing', 'BPharma- Bachelor of Pharmacy',
          'BDS- Bachelor of Dental Surgery',
          'Animation, Graphics and Multimedia',
          'B.Sc- Applied Geology', 'B.Sc.- Physics',
          'B.Sc. Chemistry', 'B.Sc. Mathematics',
          'B.Tech.-Civil Engineering',
          'B.Tech.-Computer Science and Engineering',
          'B.Tech.-Electrical and Electronics Engineering',
          'B.Tech.-Electronics and Communication Engineering',
          'B.Tech.-Mechanical Engineering',
          'B.Com- Bachelor of Commerce', 'BA in Economics',
          'CA- Chartered Accountancy', 'CS- Company Secretary',
          'Diploma in Dramatic Arts', 'MBBS',
          'Civil Services', 'BA in English',
          'BA in Hindi', 'B.Ed.']

# Load and prepare the data
df = pd.read_csv("stud_training.csv")
df.replace({'Courses': {name: idx for idx, name in enumerate(Course)}}, inplace=True)

X = df[l1]
y = df["Courses"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_evaluate_model(algorithm):
    if algorithm == "DecisionTree":
        clf = tree.DecisionTreeClassifier().fit(X_train, y_train)
    elif algorithm == "RandomForest":
        clf = RandomForestClassifier().fit(X_train, y_train)
    elif algorithm == "NaiveBayes":
        clf = GaussianNB().fit(X_train, y_train)
    else:
        clf = None

    # Calculate accuracy if classifier is valid
    if clf:
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
    else:
        accuracy = None
    
    return clf, accuracy

def predict_course(model, interests):
    l2 = [0] * len(l1)
    for interest in interests:
        if interest in l1:
            l2[l1.index(interest)] = 1
    input_test = [l2]
    predicted = model.predict(input_test)[0]
    return Course[predicted] if predicted < len(Course) else "Not Found"

# result = None
list2 = ["Vidhu Baby"]
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    accuracy = None
    if request.method == "POST":
        interests = [request.form.get(f"interest{i}") for i in range(1, 6)]
        algorithm = request.form.get("algorithm")

        clf, accuracy = train_and_evaluate_model(algorithm)

        if clf:
            result = predict_course(clf, interests)
    list2[0] = result
    print(list2)
    return render_template("index.html", interests=l1, result=result, accuracy=accuracy)

# In-memory course data
courses_data = {
    'BBA- Bachelor of Business Administration': [
        {
            'name': 'Principles of Management',
            'category': 'Management',
            'description': 'Introduction to management principles and practices.'
        },
        {
            'name': 'Business Analytics',
            'category': 'Analytics',
            'description': 'Basics of business data analysis and decision-making.'
        }
    ],
    'BEM- Bachelor of Event Management': [
        {
            'name': 'Event Planning and Coordination',
            'category': 'Event Management',
            'description': 'Learn to organize and execute events successfully.'
        },
        {
            'name': 'Marketing for Events',
            'category': 'Marketing',
            'description': 'Understanding promotion strategies for events.'
        }
    ],
    'Integrated Law Course- BA + LL.B': [
        {
            'name': 'Constitutional Law',
            'category': 'Law',
            'description': 'Understanding the framework of constitutional governance.'
        },
        {
            'name': 'Legal Drafting and Advocacy',
            'category': 'Law',
            'description': 'Learn effective legal drafting and advocacy skills.'
        }
    ],
    'BJMC- Bachelor of Journalism and Mass Communication': [
        {
            'name': 'Media Ethics and Laws',
            'category': 'Journalism',
            'description': 'Introduction to ethical practices and media regulations.'
        },
        {
            'name': 'Broadcast Journalism',
            'category': 'Mass Communication',
            'description': 'Basics of television and radio journalism.'
        }
    ],
    'BFD- Bachelor of Fashion Designing': [
        {
            'name': 'Textile Science',
            'category': 'Fashion Design',
            'description': 'Study the properties and uses of various textiles.'
        },
        {
            'name': 'Apparel Design',
            'category': 'Fashion Design',
            'description': 'Learn to create and design apparel collections.'
        }
    ],
    'B.Tech.-Computer Science and Engineering': [
        {
            'name': 'Data Structures and Algorithms',
            'category': 'Computer Science',
            'description': 'Learn basic data structures and algorithms.'
        },
        {
            'name': 'Operating Systems',
            'category': 'Computer Science',
            'description': 'Study the fundamentals of operating system design.'
        }
    ],
    'B.Sc.- Information Technology': [
        {
            'name': 'Database Management Systems',
            'category': 'Information Technology',
            'description': 'Introduction to database design and management.'
        },
        {
            'name': 'Networking Basics',
            'category': 'Information Technology',
            'description': 'Learn the essentials of computer networks.'
        }
    ],
    'B.Sc.- Nursing': [
        {
            'name': 'Anatomy and Physiology',
            'category': 'Healthcare',
            'description': 'Detailed study of the human body.'
        },
        {
            'name': 'Nursing Fundamentals',
            'category': 'Healthcare',
            'description': 'Introduction to basic nursing practices and ethics.'
        }
    ],
    'MBBS': [
        {
            'name': 'Human Anatomy',
            'category': 'Medicine',
            'description': 'Comprehensive study of human anatomy.'
        },
        {
            'name': 'Clinical Medicine',
            'category': 'Medicine',
            'description': 'Basics of diagnosing and treating illnesses.'
        }
    ],
    'B.Arch- Bachelor of Architecture': [
        {
            'name': 'Architectural Design',
            'category': 'Architecture',
            'description': 'Learn principles and techniques of architectural design.'
        },
        {
            'name': 'Building Construction',
            'category': 'Architecture',
            'description': 'Study materials and methods of building construction.'
        }
    ],
    'B.Pharm- Bachelor of Pharmacy': [
        {
            'name': 'Pharmaceutical Chemistry',
            'category': 'Pharmacy',
            'description': 'Study the chemical properties of medicinal compounds.'
        },
        {
            'name': 'Pharmacology',
            'category': 'Pharmacy',
            'description': 'Understand the effects of drugs on biological systems.'
        }
    ],
    'BDS- Bachelor of Dental Surgery': [
        {
            'name': 'Oral Anatomy',
            'category': 'Dentistry',
            'description': 'Detailed study of oral and dental anatomy.'
        },
        {
            'name': 'Prosthodontics',
            'category': 'Dentistry',
            'description': 'Learn the techniques of dental prosthetics.'
        }
    ],
    'Animation, Graphics and Multimedia': [
        {
            'name': '3D Animation Basics',
            'category': 'Design',
            'description': 'Introduction to 3D modeling and animation.'
        },
        {
            'name': 'Graphic Design',
            'category': 'Design',
            'description': 'Learn the principles of visual communication design.'
        }
    ],
    'B.Sc.- Physics': [
        {
            'name': 'Classical Mechanics',
            'category': 'Physics',
            'description': 'Understand the motion of objects under various forces.'
        },
        {
            'name': 'Quantum Physics',
            'category': 'Physics',
            'description': 'Study the behavior of matter at atomic scales.'
        }
    ],
    'B.Sc.- Chemistry': [
        {
            'name': 'Organic Chemistry',
            'category': 'Chemistry',
            'description': 'Study the structure and reactions of organic compounds.'
        },
        {
            'name': 'Physical Chemistry',
            'category': 'Chemistry',
            'description': 'Understand the physical properties of matter.'
        }
    ],
    'B.Sc.- Mathematics': [
        {
            'name': 'Linear Algebra',
            'category': 'Mathematics',
            'description': 'Explore vector spaces and linear mappings.'
        },
        {
            'name': 'Calculus',
            'category': 'Mathematics',
            'description': 'Study limits, functions, derivatives, and integrals.'
        }
    ],
    'BA in Economics': [
        {
            'name': 'Microeconomics',
            'category': 'Economics',
            'description': 'Study individual and business-level economic behavior.'
        },
        {
            'name': 'Macroeconomics',
            'category': 'Economics',
            'description': 'Understand economy-wide phenomena like inflation and GDP.'
        }
    ],
    'CA- Chartered Accountancy': [
        {
            'name': 'Accounting Standards',
            'category': 'Finance',
            'description': 'Learn the principles and rules of financial reporting.'
        },
        {
            'name': 'Taxation Laws',
            'category': 'Finance',
            'description': 'Understand the framework of direct and indirect taxes.'
        }
    ],
    'CS- Company Secretary': [
        {
            'name': 'Corporate Governance',
            'category': 'Business',
            'description': 'Study laws and policies guiding corporate operations.'
        },
        {
            'name': 'Company Law',
            'category': 'Business',
            'description': 'Understand legal aspects of company formation and management.'
        }
    ],
    'Civil Services': [
        {
            'name': 'Indian Polity',
            'category': 'Public Administration',
            'description': 'Understand the structure and functions of the Indian government.'
        },
        {
            'name': 'Current Affairs',
            'category': 'General Knowledge',
            'description': 'Stay updated with global and national developments.'
        }
    ],
    'Diploma in Dramatic Arts': [
        {
            'name': 'Acting Techniques',
            'category': 'Performing Arts',
            'description': 'Learn methods to portray characters effectively.'
        },
        {
            'name': 'Stage Design',
            'category': 'Performing Arts',
            'description': 'Study the principles of designing and managing stage settings.'
        }
    ],
    'B.Ed.': [
        {
            'name': 'Educational Psychology',
            'category': 'Education',
            'description': 'Understand the psychological principles in education.'
        },
        {
            'name': 'Pedagogy and Learning Methods',
            'category': 'Education',
            'description': 'Explore effective teaching and learning techniques.'
        }
    ],
    'BTTM- Bachelor of Travel and Tourism Management': [
        {
            'name': 'Tourism Geography',
            'category': 'Travel and Tourism',
            'description': 'Understand the geographical aspects of tourism destinations.'
        },
        {
            'name': 'Hospitality Management',
            'category': 'Travel and Tourism',
            'description': 'Learn the basics of managing hospitality services.'
        }
    ],
    'BVA- Bachelor of Visual Arts': [
        {
            'name': 'Drawing and Illustration',
            'category': 'Visual Arts',
            'description': 'Learn techniques for creating illustrations and drawings.'
        },
        {
            'name': 'Art History',
            'category': 'Visual Arts',
            'description': 'Explore the evolution of art across cultures and periods.'
        }
    ],
    'BA in History': [
        {
            'name': 'Ancient History of India',
            'category': 'History',
            'description': 'Study the early civilizations and historical developments in India.'
        },
        {
            'name': 'World Wars and Modern History',
            'category': 'History',
            'description': 'Understand the causes and impacts of major world conflicts.'
        }
    ],
    'B.Com- Bachelor of Commerce': [
        {
            'name': 'Financial Accounting',
            'category': 'Commerce',
            'description': 'Learn the fundamentals of financial record-keeping and reporting.'
        },
        {
            'name': 'Business Law',
            'category': 'Commerce',
            'description': 'Understand the legal principles affecting business operations.'
        }
    ],
    'B.Tech.-Civil Engineering': [
        {
            'name': 'Structural Analysis',
            'category': 'Civil Engineering',
            'description': 'Learn methods for analyzing and designing structures.'
        },
        {
            'name': 'Surveying and Geomatics',
            'category': 'Civil Engineering',
            'description': 'Study techniques for land measurement and mapping.'
        }
    ],
    'B.Tech.-Electrical and Electronics Engineering': [
        {
            'name': 'Circuit Theory',
            'category': 'Electrical Engineering',
            'description': 'Understand the principles of electrical circuits and systems.'
        },
        {
            'name': 'Power Systems',
            'category': 'Electrical Engineering',
            'description': 'Learn the fundamentals of electrical power generation and distribution.'
        }
    ],
    'B.Tech.-Electronics and Communication Engineering': [
        {
            'name': 'Digital Signal Processing',
            'category': 'Electronics Engineering',
            'description': 'Study methods for processing and analyzing signals digitally.'
        },
        {
            'name': 'Communication Systems',
            'category': 'Electronics Engineering',
            'description': 'Understand the design and working of modern communication systems.'
        }
    ],
    'B.Tech.-Mechanical Engineering': [
        {
            'name': 'Thermodynamics',
            'category': 'Mechanical Engineering',
            'description': 'Explore the principles of energy conversion and heat transfer.'
        },
        {
            'name': 'Manufacturing Processes',
            'category': 'Mechanical Engineering',
            'description': 'Learn techniques for designing and manufacturing products.'
        }
    ],
    'BA in English': [
        {
            'name': 'Literary Theory',
            'category': 'English Literature',
            'description': 'Understand critical theories for analyzing literature.'
        },
        {
            'name': 'Creative Writing',
            'category': 'English',
            'description': 'Learn techniques to craft engaging and effective writing.'
        }
    ],
    'BA in Hindi': [
        {
            'name': 'Hindi Literature and Poetry',
            'category': 'Hindi',
            'description': 'Study classic and modern works of Hindi literature.'
        },
        {
            'name': 'Grammar and Linguistics',
            'category': 'Hindi',
            'description': 'Understand the structure and usage of the Hindi language.'
        }
    ],
    'MBBS': [
        {
            'name': 'Anatomy',
            'category': 'Medical Science',
            'description': 'Study the structure of the human body.'
        },
        {
            'name': 'Pathology',
            'category': 'Medical Science',
            'description': 'Understand the mechanisms of diseases in humans.'
        }
    ],
    'B.Sc- Nursing': [
        {
            'name': 'Clinical Nursing',
            'category': 'Healthcare',
            'description': 'Learn the practical aspects of nursing care.'
        },
        {
            'name': 'Community Health Nursing',
            'category': 'Healthcare',
            'description': 'Focus on public health and preventive care.'
        }
    ],
    'B.Arch- Bachelor of Architecture': [
        {
            'name': 'Architectural Design',
            'category': 'Architecture',
            'description': 'Learn to design functional and aesthetically pleasing structures.'
        },
        {
            'name': 'Building Construction',
            'category': 'Architecture',
            'description': 'Study the principles of construction materials and techniques.'
        }
    ],
    'B.Sc.- Information Technology': [
        {
            'name': 'Database Management Systems',
            'category': 'IT',
            'description': 'Learn to design, implement, and manage databases.'
        },
        {
            'name': 'Cybersecurity',
            'category': 'IT',
            'description': 'Understand methods to protect systems and networks from cyber threats.'
        }
    ],
    'B.Sc- Applied Geology': [
        {
            'name': 'Mineralogy',
            'category': 'Geology',
            'description': 'Study minerals, their properties, and classifications.'
        },
        {
            'name': 'Petrology',
            'category': 'Geology',
            'description': 'Understand the formation and composition of rocks.'
        }
    ]
}


@app.route('/courses_main', methods=["GET", "POST"])
def courses_main():
    print(list2)
    result1 = list2[0]
    print(result1)
    return render_template("index1.html", result = result1)

@app.route('/api/courses', methods=['GET'])
def get_courses():
    degree = request.args.get('degree')
    # Return the courses for the selected degree
    if degree in courses_data:
        return jsonify(courses_data[degree])
    else:
        return jsonify([])  # Return an empty list if degree is not found



@app.route('/coursera')
def hello_world():
    return render_template("index3.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    if (request.method == 'POST'):
        namec=(request.form['course'])
    
    output=create_sim(namec)
    if output.empty:
        ms='Sorry! we did not find any matching courses, Try adding more keywords in your search.'
        ht=' '
    else:
        ht=output.to_html(render_links=True, index=True)
        ht= Markup(ht)
        ms='Here are some recommendations :'
    return render_template('index3.html',message=ms,pred=ht)



# ===================== MAIN ENTRY POINT =====================
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
