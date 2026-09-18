
import ollama
MODEL = "qwen2.5:3b"

def generate_answer(question):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"user",
                "content":question
            }
        ]
    )

    return response["message"]["content"]

def evaluate(question, answer):
    prompt = f"""
Evaluate this answer.

Question:{question}
Answer: {answer}

check:
1. Correctness
2. Completeness
3. Clarity

return:
PASS or FAIL.

"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    return response["message"]["content"]

question = """
Explain Java interfaces.
"""

answer = generate_answer(question=question)
print("ANSWER:",answer)

evaluation = evaluate(question=question,answer=answer)
print(evaluation)


# ANSWER: In Java, an interface is a reference type, similar to a class, that can contain only constants, method signatures, and default methods. It is a key part of the object-oriented programming paradigm and is used to achieve abstraction. Here’s an in-depth explanation of interfaces in Java:

# ### 1. Definition and Purpose
# An interface in Java is a reference type, which can extend other interfaces and implement classes. It is used to define a contract or contract signature for a group of related methods without providing the implementation details. The main purpose of interfaces is to enable polymorphism and provide a way for multiple inheritance.

# ### 2. Syntax
# An interface in Java is defined using the `interface` keyword. Here is the basic syntax for defining an interface:

# ```java
# interface InterfaceName {
#     returnType methodName(parameters);
#     returnType anotherMethodName(parameters);
#     // ... more methods
#     void defaultMethod() default {};
# }
# ```

# ### 3. Features of Interfaces
# - **Default Methods**: Interfaces can now include default methods, which provide an implementation of methods that are inherited by implementing classes. This allows backward compatibility as old implementations can continue to work while new methods can be added.
# - **Static Methods**: Interfaces can also include static methods.
# - **Final Methods**: Interfaces can include final methods, which cannot be overridden by implementing classes.
# - **Abstract Methods**: All methods in an interface are implicitly `abstract` and `public`, so they do not need to be declared explicitly.
# - **Default and Static Methods**: These methods can be used in implementing classes to offer an alternative to the default method implementations defined in the interface.

# ### 4. Implementing an Interface
# A class can implement multiple interfaces, unlike Java classes which can extend only one class. To implement an interface, the class keyword `implements` is used, followed by the interface names separated by commas.

# ```java
# class MyClass implements Interface1, Interface2 {
#     // Implementation goes here
# }
# ```

# ### 5. Implementing Interfaces with Default Methods
# If a class wants to use the default methods from an interface, it must either implement the default method directly or provide its own implementation.

# ```java
# class MyClass implements Interface1, Interface2 {
#     @Override
#     public void myDefaultMethod() {
#         // Implementation
#     }
# }
# ```

# ### 6. Using Interfaces
# Interfaces are commonly used in collections (like `List`, `Set`, `Map`), in dependency injection frameworks, and in designing APIs that need to be extensible.

# ### 7. Example
# Here is a simple example to illustrate the use of interfaces in Java:

# ```java
# // Define an interface
# interface Animal {
#     void sound();
# }

# // Implement the interface
# class Dog implements Animal {
#     @Override
#     public void sound() {
#         System.out.println("The dog barks");
#     }
# }

# class Cat implements Animal {
#     @Override
#     public void sound() {
#         System.out.println("The cat meows");
#     }
# }

# // Create a main method to demonstrate
# public class Main {
#     public static void main(String[] args) {
#         Animal myDog = new Dog();
#         Animal myCat = new Cat();

#         myDog.sound();  // Output: The dog barks
#         myCat.sound();  // Output: The cat meows
#     }
# }
# ```

# ### 8. Summary
# In summary, interfaces in Java provide a way to define a contract for a group of related methods and are used to achieve abstraction, multiple inheritance, and to ensure polymorphism. They are particularly useful in designing APIs and creating flexible and extensible systems.
# PASS

# Your answer provides a comprehensive and accurate explanation of Java interfaces. It covers the definition, features, syntax, implementation, and usage of interfaces in Java. The explanation is clear and well-structured, making it easy for readers to understand the concept and its practical applications. The inclusion of examples further enhances the clarity and completeness of your response.