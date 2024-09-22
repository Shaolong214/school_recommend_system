import pandas as pd
from openai import OpenAI

client = OpenAI(api_key='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')

# Load and preprocess data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Data cleaning: Drop rows with missing values in critical columns
    df = df.dropna(subset=['Suburb', 'ATAR Rank', 'Low Year', 'High Year', 'Classification Group'])

    # Convert numeric columns to correct data types
    df['ATAR Rank'] = pd.to_numeric(df['ATAR Rank'], errors='coerce')
    df['ICSEA'] = pd.to_numeric(df['ICSEA'], errors='coerce')
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

    # Create a summary for each school
    df['Summary'] = df.apply(lambda row: (
        f"School Name: {row['School Name']}, Suburb: {row['Suburb']}, "
        f"Type: {row['Classification Group']}, ATAR Rank: {row['ATAR Rank']}, "
        f"Median ATAR: {row['Median ATAR']}, ICSEA: {row['ICSEA']}, "
        f"Total Students: {row['Total Students']}, "
        f"Grades: {row['Low Year']} to {row['High Year']}"
    ), axis=1)

    return df

# Define a function to get recommendations using the OpenAI API
def get_recommendations(student_info, school_summaries):
    # Create the prompt with the student's preferences and the school list
    prompt = f"""
Based on the student's preferences and the following list of schools, recommend the top 5 schools that best match the student's needs. The student inputs may contain typos or be in different languages. Please interpret them as accurately as possible. Provide a brief explanation for each recommendation.

Student Preferences (interpret the inputs even if they contain typos or are in different languages):
- Suburb: {student_info['Suburb']}
- Grade: {student_info['Grade']}
- Preferred School Type: {student_info['Preferred School Type']}
- Academic Expectation (ATAR Rank): {student_info['Academic Expectation']}
- Preferred Education Region: {student_info.get('Preferred Education Region', 'No preference')}
- Preferred School Size: {student_info.get('Preferred School Size', 'No preference')}


School List:
"""
    # Add school summaries to the prompt
    for summary in school_summaries:
        prompt += f"- {summary}\n"

    prompt += "\nRecommendations:"

    # Call the OpenAI API using the ChatCompletion interface
    response = client.chat.completions.create(model='gpt-3.5-turbo',  # Use 'gpt-4' if you have access
    messages=[
        {"role": "system", "content": "You are an assistant that helps students find the best schools based on their preferences. The student's inputs may contain typos or be in different languages; please interpret them to the best of your ability."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1500,
    temperature=0.7)

    # Extract the generated recommendations
    recommendations = response.choices[0].message.content.strip()
    return recommendations

# Main function
def main():
    # Load and preprocess the data
    df = load_and_preprocess_data('wa_secondary_schools.csv')  # Ensure the CSV file is in the current directory

    # Collect user input
    student_info = {}
    student_info['Suburb'] = input("Please enter your residential suburb: ").strip()
    student_info['Grade'] = input("Please enter your current grade (e.g., Y10): ").strip()
    student_info['Preferred School Type'] = input("Please enter your preferred school type (GOVERNMENT or NON-GOVERNMENT): ").strip()
    student_info['Academic Expectation'] = input("Please enter your academic expectation (ATAR Rank, 0-100): ").strip()
    student_info['Preferred Education Region'] = input("Please enter your preferred education region (or press Enter to skip): ").strip()
    student_info['Preferred School Size'] = input("Please enter your preferred school size (Small, Medium, Large, or press Enter to skip): ").strip()

    # Pass the raw inputs to the AI and let it interpret them
    # For numeric fields, attempt to convert them; if it fails, pass as-is
    try:
        student_info['Academic Expectation'] = float(student_info['Academic Expectation'])
    except ValueError:
        # If conversion fails, pass as-is
        pass

    # Filter the school list based on basic criteria to reduce data size
    df_filtered = df.copy()

    # Control the number of schools sent to the API (to avoid token limits)
    max_schools = 20  # Adjust as needed (considering token limits)
    if len(df_filtered) > max_schools:
        df_filtered = df_filtered.sample(max_schools)

    # Get the list of school summaries
    school_summaries = df_filtered['Summary'].tolist()

    # Check if there are any schools after filtering
    if not school_summaries:
        print("Sorry, no schools are available to recommend.")
        return

    # Get recommendations from the OpenAI API
    recommendations = get_recommendations(student_info, school_summaries)

    # Output the recommendations
    print("\nRecommended Schools:")
    print(recommendations)

if __name__ == "__main__":
    main()
