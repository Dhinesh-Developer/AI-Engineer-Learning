import ollama

MODEL = "llama3.2"

goal = """
    Build a simple expense management application.
"""

prompt = f"""
You are a task planner.

Break this goal into small executable tasks.

Goal: {goal}

Return a numbered list in priority order.
"""

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role":"user","content":prompt}
    ]
)

print(response["message"]["content"])


# **High Priority (Must-Be-Done-First)**

# 1. **Define the Requirements and Scope**:
#         * Research existing expense management applications
#         * Identify the key features and functionalities needed for the application
#         * Determine the target audience and user experience requirements
#         * Create a written specification or requirements document
# 2. **Choose a Development Framework and Tools**:
#         * Select a suitable programming language and framework (e.g., Python, JavaScript, React)
#         * Choose a database management system (e.g., MySQL, MongoDB, Firebase)
#         * Pick a UI library or framework (e.g., Bootstrap, Material-UI, Vue.js)
#         * Set up the development environment and tools (e.g., IDE, code editor, version control)

# **Medium Priority (Should-Be-Done-Soon)**

# 3. **Design the User Interface (UI) and User Experience (UX)**:
#         * Create wireframes and mockups of the application's layout and user interface
#         * Develop a user experience (UX) design plan, including user flow and interaction patterns
#         * Create a visual design style guide for the application
# 4. **Set up the Database and Data Modeling**:
#         * Design the database schema and create the necessary tables
#         * Define the relationships between tables and entities
#         * Populate the database with sample data

# **Low Priority (Can-Be-Done-Later)**

# 5. **Implement the Backend Logic and API**:
#         * Write server-side code to handle user requests and responses
#         * Create APIs for data storage, retrieval, and manipulation
#         * Implement authentication and authorization mechanisms
# 6. **Develop the Frontend User Interface and Interactions**:
#         * Write client-side code to render the UI and handle user interactions
#         * Implement form validation, error handling, and loading animations
#         * Integrate the UI with the backend API
# 7. **Add Advanced Features and Refine the UI/UX**:
#         * Implement features like categorization, tagging, and filtering
#         * Enhance the user interface with animations, transitions, and micro-interactions
#         * Refine the user experience to ensure a smooth and engaging flow
# 8. **Test and Debug the Application**:
#         * Write unit tests and integration tests to ensure the application's correctness
#         * Test the application's UI, UX, and functionality on different devices and browsers
#         * Debug and fix any issues that arise during testing
# 9. **Deploy and Maintain the Application**:
#         * Choose a deployment platform (e.g., Heroku, AWS, Google Cloud)
#         * Set up continuous integration and continuous deployment (CI/CD) pipelines
#         * Monitor the application's performance and fix any issues that arise during use

# By breaking down the goal into smaller tasks and prioritizing them, we can create a manageable project plan that ensures the successful development of a simple expense management application.
