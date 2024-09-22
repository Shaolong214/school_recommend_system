**Introduction**

Developing a school recommender system involves matching students with suitable schools based on various criteria. Two primary approaches are:

1.  **AI-Based Approach**: Utilizing OpenAI's GPT models to interpret user inputs and generate recommendations.
2.  **Non-AI Approach**: Using traditional programming logic and explicit algorithms to process inputs and produce recommendations.

Below is a concise and intuitive comparison of these approaches, including their methods, technologies, advantages, and disadvantages---especially focusing on the AI approach's potential issues like hallucinations, token limits, and the need for Retrieval-Augmented Generation (RAG) or fine-tuning.

* * * * *

### **1\. Criteria Selection**

**AI-Based Approach**

-   **User Inputs**: Accepts raw inputs directly from users, even if they contain typos or are in different languages.
-   **Criteria**:
    -   Suburb
    -   Grade
    -   Preferred School Type (Government or Non-Government)
    -   Academic Expectation (ATAR Rank)
    -   Preferred Education Region
    -   Preferred School Size
    -   Special Programs

**Non-AI Approach**

-   **Explicit Criteria**: Clearly defined and structured criteria are used.
-   **Criteria**:
    -   Exact Suburb Matching
    -   Grade Level Compatibility
    -   School Type Preference
    -   Academic Performance (ATAR Rank)
-   **User-Defined Weights**: Users assign importance to each criterion, tailoring the recommendations to their preferences.

* * * * *

### **2\. Methods and Technologies Used**

**AI-Based Approach**

-   **Technologies**:
    -   **OpenAI GPT Models**: Leverages GPT-3.5 turbo via the OpenAI API.
    -   **Python & Pandas**: For data handling and preprocessing.
-   **Process**:
    -   **Data Loading**: Schools data loaded into a DataFrame.
    -   **Prompt Creation**: Student preferences and school summaries are compiled into a prompt.
    -   **AI Interaction**: The AI model generates recommendations based on the prompt.
-   **Advantages**:
    -   **Flexibility**: Can interpret and correct user inputs with typos or in different languages.
    -   **Nuanced Understanding**: Provides sophisticated recommendations by understanding context.
-   **Disadvantages**:
    -   **Hallucinations**: The AI may generate plausible but incorrect or irrelevant information.
    -   **Token Limits**: Restrictions on input/output size may limit the amount of data processed.
    -   **Need for RAG or Fine-Tuning**: To enhance accuracy, integrating Retrieval-Augmented Generation or fine-tuning the model may be necessary, adding complexity.

**Non-AI Approach**

-   **Technologies**:
    -   **Python & Pandas**: Used for data manipulation and implementing the recommendation logic.
-   **Process**:
    -   **Data Preprocessing**: Clean and prepare the data for analysis.
    -   **User Input Collection**: Gather structured inputs from the user.
    -   **Scoring Function**: Calculate a score for each school based on criteria and user-assigned weights.
    -   **Recommendation Generation**: Sort schools based on scores and present the top matches.
-   **Advantages**:
    -   **Transparency**: The logic is explicit and understandable.
    -   **Control**: Developers have full control over how recommendations are generated.
    -   **No External Dependencies**: Does not rely on external APIs, avoiding associated costs and potential latency.
-   **Disadvantages**:
    -   **Rigid Input Handling**: May not handle typos or unstructured inputs well.
    -   **Limited Flexibility**: Less capable of interpreting nuanced preferences without additional programming.

* * * * *

### **3\. Validating Effectiveness**

**AI-Based Approach**

-   **Challenges**:
    -   **Hallucinations**: AI might recommend schools that are unsuitable due to incorrect interpretations.
    -   **Validation Difficulty**: The AI's decision-making process is less transparent, making it harder to verify correctness.
-   **Methods**:
    -   **User Feedback**: Collect responses from users about the relevance and accuracy of recommendations.
    -   **Monitoring**: Check for patterns in AI errors to adjust prompts or processes.
    -   **Incremental Refinement**: Use RAG or fine-tuning to improve the model's performance over time.

**Non-AI Approach**

-   **Advantages**:
    -   **Ease of Validation**: The recommendation logic is transparent, making it straightforward to test and verify.
-   **Methods**:
    -   **Testing with Various Inputs**: Ensure the system behaves correctly across a range of scenarios.
    -   **User Feedback**: Solicit user opinions to identify areas for improvement.
    -   **Adjusting Weights and Criteria**: Refine the scoring system based on feedback to better match user expectations.

* * * * *

### **Conclusion**

**AI-Based Approach**

-   **Pros**:
    -   Handles diverse and unstructured inputs gracefully.
    -   Provides personalized and context-aware recommendations.
-   **Cons**:
    -   **Hallucinations**: Risk of generating incorrect or misleading recommendations.
    -   **Token Limitations**: Constraints on data size may impact the system's ability to process all relevant information.
    -   **Complexity**: May require RAG or fine-tuning to achieve acceptable accuracy, increasing development effort.

**Non-AI Approach**

-   **Pros**:
    -   Transparent and explainable logic.
    -   Full control over recommendation criteria and weights.
    -   No reliance on external APIs, avoiding additional costs.
-   **Cons**:
    -   Less flexible in handling user input variations.
    -   May require significant coding to handle complex preferences or input errors.

* * * * *

### **Recommendation**

**hybrid approach** could offer the best of both worlds:

-   **Initial Filtering with Non-AI Methods**:
    -   Use explicit criteria and user-defined weights to filter and score schools.
    -   Ensures transparency and control over fundamental matching.
-   **Refinement with AI Assistance**:
    -   Apply AI to interpret nuanced preferences and provide personalized explanations.
    -   Be cautious of AI limitations by validating outputs and monitoring for hallucinations.

**Key Considerations**:

-   **Mitigating AI Disadvantages**:

    -   **Hallucinations**: Implement checks to verify AI-generated recommendations against reliable data.
    -   **Token Limits**: Optimize prompts to stay within token limits or consider models with larger context windows.
    -   **RAG/Fine-Tuning Needs**: Evaluate whether integrating RAG or fine-tuning is feasible and cost-effective for the project's scope.
-   **Validation Strategy**:

    -   Continuously collect user feedback to refine both AI and non-AI components.
    -   Perform rigorous testing to ensure the system meets user needs effectively.
