import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


# client = OpenAI(api_key='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')

# Constants
MAX_SCHOOLS = 20  # Maximum number of schools to send to the API
MAX_CRITERION_SCORE = 100  # Maximum score for any criterion
SMALL_SCHOOL_MAX_SIZE = 500  # Max students for a small school
MEDIUM_SCHOOL_MAX_SIZE = 1000  # Max students for a medium school

# Initialize OpenAI API
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Drop rows with missing critical values
    df = df.dropna(subset=[
        'School Name', 'Suburb', 'Median ATAR', 'Low Year', 'High Year',
        'Classification Group', 'Total Students'
    ])

    # Convert numerical columns
    df['Median ATAR'] = pd.to_numeric(df['Median ATAR'], errors='coerce')
    df['Total Students'] = pd.to_numeric(df['Total Students'], errors='coerce')

    # Map grades to numeric values
    grade_mapping = {
        'KIN': 0, 'PPR': 0, 'Y01': 1, 'Y02': 2, 'Y03': 3, 'Y04': 4,
        'Y05': 5, 'Y06': 6, 'Y07': 7, 'Y08': 8, 'Y09': 9,
        'Y10': 10, 'Y11': 11, 'Y12': 12
    }
    df['Low Year Numeric'] = df['Low Year'].map(grade_mapping)
    df['High Year Numeric'] = df['High Year'].map(grade_mapping)

    # Categorize school size
    def categorize_school_size(total_students):
        if total_students < SMALL_SCHOOL_MAX_SIZE:
            return 'SMALL'
        elif total_students <= MEDIUM_SCHOOL_MAX_SIZE:
            return 'MEDIUM'
        else:
            return 'LARGE'
    df['School Size'] = df['Total Students'].apply(categorize_school_size)

    # Create a summary description for each school
    df['Summary'] = df.apply(lambda row: (
        f"School Name: {row['School Name']}, Suburb: {row['Suburb']}, "
        f"Classification Group: {row['Classification Group']}, Median ATAR: {row['Median ATAR']}, "
        f"Total Students: {row['Total Students']}, School Size: {row['School Size']}, "
        f"Grades: {row['Low Year']} to {row['High Year']}"
    ), axis=1)

    return df

def get_recommendations(student_info, weights, school_summaries):
    # Create the prompt for OpenAI API
    prompt = f"""
Based on the student's preferences and the following list of schools, recommend the top 5 schools that best meet the student's needs. Score and rank the schools according to the weights provided for each criterion.

Student preferences (interpret accurately even with typos or different languages):
- Suburb: {student_info['Suburb']}
- Grade: {student_info['Grade']}
- Preferred School Type: {student_info['Preferred School Type']}
- Academic Expectation (Median ATAR): {student_info['Academic Expectation']}
- Preferred School Size: {student_info.get('Preferred School Size', 'No preference')}

Weights assigned by the student to the following criteria (total must sum to 1):
- Location Weight: {weights['location_weight']}
- Academic Performance Weight: {weights['academic_weight']}
- School Type Weight: {weights['type_weight']}
- School Size Weight: {weights['size_weight']}

Scoring criteria and rules:

1. **Location**:
   - If the school's Suburb matches the student's Suburb, score is {MAX_CRITERION_SCORE}, else 0.

2. **Academic Performance**:
   - Score is (Median ATAR / 100) * {MAX_CRITERION_SCORE}.
   - Exclude schools with Median ATAR below the student's expectation.

3. **School Type**:
   - If Classification Group matches Preferred School Type, score is {MAX_CRITERION_SCORE}, else 0.

4. **School Size**:
   - Sizes:
     - SMALL: Total Students < {SMALL_SCHOOL_MAX_SIZE}
     - MEDIUM: {SMALL_SCHOOL_MAX_SIZE} <= Total Students <= {MEDIUM_SCHOOL_MAX_SIZE}
     - LARGE: Total Students > {MEDIUM_SCHOOL_MAX_SIZE}
   - If size matches Preferred School Size, score is {MAX_CRITERION_SCORE}, else 0.

5. **Grade**:
   - School must offer the student's Grade; otherwise, exclude the school.

**Total Score Calculation**:
Total Score = (Location Score * {weights['location_weight']}) + (Academic Score * {weights['academic_weight']}) + (Type Score * {weights['type_weight']}) + (Size Score * {weights['size_weight']})

Score each school based on these rules and recommend the top 5 schools with the highest scores. Provide a brief explanation for each recommendation.

School list:
"""
    # Append school summaries to the prompt
    for summary in school_summaries:
        prompt += f"- {summary}\n"

    prompt += "\nRecommendations:"

    # Call the OpenAI API
    response = client.chat.completions.create(model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are an assistant helping a student find the most suitable schools based on their preferences. Please score and recommend schools according to the student's criteria and weights."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1500,
    temperature=0.7)

    # Extract recommendations
    recommendations = response.choices[0].message.content.strip()
    return recommendations

def main():
    # Load and preprocess data
    df = load_and_preprocess_data('wa_secondary_schools.csv')

    # Collect user input
    student_info = {}
    student_info['Suburb'] = input("Please enter your residential suburb: ").strip().upper()
    student_info['Grade'] = input("Please enter your current grade (e.g., Y10): ").strip().upper()
    student_info['Preferred School Type'] = input("Please enter your preferred school type (GOVERNMENT, NON-GOVERNMENT, SECONDARY SCHOOLS, DISTRICT HIGH SCHOOLS, K-12 SCHOOLS): ").strip().upper()
    student_info['Academic Expectation'] = input("Please enter your minimum acceptable Median ATAR (0-100): ").strip()
    student_info['Preferred School Size'] = input("Please enter your preferred school size (SMALL, MEDIUM, LARGE): ").strip().upper()

    # Convert Academic Expectation to float if possible
    try:
        student_info['Academic Expectation'] = float(student_info['Academic Expectation'])
    except ValueError:
        pass  # Keep original input if conversion fails

    # Collect weights for each criterion
    print("Please assign weights to the following criteria. The total must sum to 1.")
    weights = {}
    weights['location_weight'] = float(input("Weight for location (0-1): ").strip())
    weights['academic_weight'] = float(input("Weight for academic performance (0-1): ").strip())
    weights['type_weight'] = float(input("Weight for school type (0-1): ").strip())
    weights['size_weight'] = float(input("Weight for school size (0-1): ").strip())

    # Ensure total weight sums to 1
    total_weight = sum(weights.values())
    if total_weight != 1.0:
        # Normalize weights
        weights = {k: v / total_weight for k, v in weights.items()}

    # Limit the number of schools sent to the API
    if len(df) > MAX_SCHOOLS:
        df_filtered = df.sample(MAX_SCHOOLS)
    else:
        df_filtered = df.copy()

    # Get school summaries
    school_summaries = df_filtered['Summary'].tolist()

    # Check if any schools are available
    if not school_summaries:
        print("Sorry, there are no schools available for recommendation.")
        return

    # Get recommendations
    recommendations = get_recommendations(student_info, weights, school_summaries)

    # Output recommendations
    print("\nRecommended Schools:")
    print(recommendations)

if __name__ == "__main__":
    main()


