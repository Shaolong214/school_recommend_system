### Introduction

Two prototypes were developed for a school recommendation system: one using AI (OpenAI API) and one using traditional rule-based logic. Both systems use the same set of criteria, but differ in their methods and technologies. Below, we discuss the selected criteria, the methods and technologies used for each prototype, and their limitations.

### Criteria Selected and Rationale

-   **Location (Suburb, Postcode)**: Proximity to home is a key concern for parents and students, as it affects daily commute and accessibility.
-   **Academic Performance (Median ATAR)**: Schools with higher academic performance are often prioritized by families looking for strong educational outcomes.
-   **School Type (Classification Group)**: Filters based on personal preferences for government, non-government, or religious schools.
-   **School Size (Total Students)**: Helps match student preferences for small, medium, or large environments, affecting classroom size and resources.
-   **Grade Level (Low Year, High Year)**: Ensures the school offers the student's current educational level, filtering out irrelevant schools.

### Methods and Technologies for Each Prototype

#### AI Solution

-   **Technologies**:
    -   **OpenAI API**: Generates recommendations based on user preferences and weights using natural language prompts.
    -   **Pandas**: Preprocesses and cleans the data, handles missing values, and categorizes school sizes.
    -   **Python Input Functions**: Captures user preferences (e.g., suburb, grade, weights for criteria).
-   **Limitations**:
    -   **Hallucination**: AI may generate irrelevant or incorrect recommendations (hallucinations) due to misunderstood inputs or incomplete prompts.
    -   **Token Limit**: The amount of data that can be processed at once is limited, potentially requiring **RAG** (retrieval-augmented generation) or **fine-tuning** for more precise responses.
    -   **Input Flexibility**: Handles typos or language variations, but could still misinterpret ambiguous user inputs.

#### Traditional Solution

-   **Technologies**:
    -   **Pandas**: Similar to the AI solution, used to clean and preprocess data.
    -   **Python Functions**: Manual scoring and filtering based on fixed rules for each criterion (location, ATAR, etc.).
-   **Limitations**:
    -   **Input Strictness**: Requires exact user inputs without typos or inconsistencies, reducing flexibility.
    -   **Fixed Logic**: Lacks adaptability, offering rigid recommendations based on fixed criteria, which may not handle nuanced preferences or ambiguous inputs.

### Conclusion

The AI prototype offers more flexibility but faces challenges like hallucinations and token limits, potentially requiring more advanced techniques (RAG or fine-tuning). The traditional solution is simpler but limited by strict input requirements and fixed logic, making it less adaptable to diverse or ambiguous user needs.