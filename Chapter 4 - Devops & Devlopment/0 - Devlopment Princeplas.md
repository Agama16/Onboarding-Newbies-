\# Software Development Foundations \& Python Basics



Before building data pipelines or services, it is important to understand the

core principles of modern software development.



This module introduces the development practices, conventions, and tools that

are commonly used in professional engineering environments.



The goal is not only to learn \*what the tools are\*, but also \*why they exist\*

and how they help create maintainable, scalable, and collaborative systems.



\---



\### ⏳ Timeline

Estimated Duration: 2 Days



Day 1 – Software Development Foundations  

\- Development principles and clean architecture

\- Development workflows and collaboration

\- Testing approaches and design paradigms



Day 2 – Python and API Foundations  

\- Python ecosystem and development patterns

\- REST APIs and Python frameworks

\- Testing, mocking, and service design



\---



\### 📚 Resources

Use the resources below and practice researching additional information online.



\- \[Clean Python - Sunil Kapil](hhttps://edu.anarcho-copy.org/Programming%20Languages/Python/Clean%20Python.pdf)

\- \[SOLID Principles Overview](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)

\- \[Python Official Documentation](https://docs.python.org/3/)

\- \[FastAPI Documentation](https://fastapi.tiangolo.com/)

\- \[Flask Documentation](https://flask.palletsprojects.com/)

\- \[Pytest Documentation](https://docs.pytest.org/)



\---



\# Software Development Principles



\### ❓ Guide Questions



1\. What are \*\*Clean Code principles\*\*, and why are they important in software development?  

&#x20;  Explain ideas such as readability, maintainability, and the principle of  

&#x20;  \*\*“Leave the codebase cleaner than you found it.”\*\*

the clean code principles are a set of conventions that implementing them in the code makes it easier to read, understand and modify, that makes it prossible for multiplke people to work on the same code and avoid unnecessary complexity and confusion.
they include:
- giving variables and functions meaningful names and keep them short.
- use comments and documentation that make the code readable for other developers.
- use consistent formatting and indentation, make sure spaces, tabs, whitespaces and line breaks are clean and consistent.
- donwt repeat yourself, if neede make functions more general to avoid code duplication.
- handle errors correctly and cleany.
- use testing
- refactor the code regularly, to improve or adjust the code to changes that need to be made.

these principles help maintain readability which means anyone can read it and understand it (you or other developers), maintainability which means its easy to extand or modify when needed, efficiency and bug reduction by managing errors and writing a clean code.
you should leave the code cleaner than you found it, meaning everytime you look at the code you should review it and improve it.


2\. What are the \*\*SOLID principles\*\*?  

&#x20;  Describe each principle and explain how they help create maintainable

&#x20;  object-oriented systems.

SOLID are the five OOD principles that stand at the core of software development and help maintain it in a way that avoids code smells or refactor, and encourages agile developing ( flexibility, collaboration and customer satisfaction.
SOLID stands for:
- Single responsibility principle :
  every class should have one responsibility only and therefore have only one reason to change. deviding the responsibilities between those classes makes a defined, "each-in-his-territory" design where a change in the code won't cause a chain reaction or a larger change than needed - minimize the affect of code changes.
  
- Open-closed principle :
   objects should be open for extentions but closed for modifications, that means that extantioning a class shouldn't modify it in any way - minimizing the affect of code extention and making the code more collaborative.

- Liskov substitution principle :
  every sub-class or derived class should be able to subtitute their parent class, meaning that an object from a sub-class should satisfy the conditions in a parent-class code.
  an example is a class of rectangles being subtitud by a class of squares, the square will inherit all of the rectangle's attributes, even hight and width but it only needs one of them since thry are similar. both the square and the rectangle should inherit from a more basic group. 

- Interface Segregation Principle :
  a client shouldn't be forced to implement an interface or method that isn't needed by them. That means methods/interfaces shouldn't be dependent on other methods or interfaces that aren't necessarily needed in the same cases - avoiding unneeded object creation/ code running.

- Dependency Inversion Principle :
  high level modules should not rely on low level ones, but on abstractions instead.
  that means that a dependency on a low level module should be broken down to if needed multiple dependencies. that makes it easier to implement the open-closed principle and makes the code more flexible and collaborative.
  higher level modules relying on lower level ones creates tight coupling that prevents reusing the module.
  lets say we have a class for building a house, and a class of bricks, we wont do action from the actual bricks class but we'll use a worker class that can do that, that way a worker can use the bricks class or other actions and the class is reusable.

all 5 of the SOLID principles make sure that the code is easy to work with, comfortable to change and effective for the client.



3\. Explain the \*\*KISS principle\*\* and its importance in software design.

Why does simple and intuitive software scale well?  

&#x20;  Why do overly complex systems tend to fail over time?

the KISS principle is a design principle that keeps the code simple to have better clarity and effectivness. the KISS principles is implemented through:
- identifying core objectives - defining the problem or objective and solution/goals you need to implement.
- focus on essentials - avoid unnecessary functions or objects and prioritize whats important for the solution.
- simplify design and workflow - avoid complicated code design and keep it stream-y.
- prioritize clarity and understandability - keep the solution simple and clear and use understandable language to document it.
- iterate and refine - review the code and refine it to be more simple.
- use simple tools and techniques - avoid tools that bring unnecessary complexity to the code.
- test for simplicity - evaluate the solution by the KISS principle to see if it could be more simple than it is.
- maintain pragmatism - balance simplicity with functionality and scalability.

all of those help maintain an understandable code.


4\. What are the most common \*\*paradigms / programming\*\* (ex. Object Orianted) styles, what are the differences and when should each be used

the most common types of programming styles are:
- procedural or imperative programming - a type of programming in whichcode is written in a top to bottom chain of functions in a linear pipeline and the code writing is very low-level, simple code with no use of advance or high level features. this should be avoided since even though it might help wih optimizing at runtime (and even that barely) , the cost of having a complicated error-prone less readable code is far worse.
- object oriented programming - manipulating or maintaining different core objects using actions or methods usually based on classes. itws one of the easiest and most useful programming styles to implement, and it delivers a clean and well functioning code if done correctly. java and C++ are both object oriented languages.
- functional programming - more functional based rather than class based, meaning that they can also be passed as inputs and outputs. the focus on pure functions means the same input will return the same output, there is no change to other parts of the code or use of other objects other than the input, all values are immutable. JS for an example is a functual language.
we would rather use OOP than FP when there is similarities or dependencies between objects rather than where there is more complication on the functional side, which is where we would rather use FP.


5\. What is \*\*Test Driven Development (TDD)\*\*?  

&#x20;  Explain the development cycle and how it improves code reliability.

test driven development is a code writing way in which you write a code "unit", write a test case to it, write more code to fix it and refactor the code and the test case and do it again with a new case.
that means you test you full program in parts instead of writing a code and then a test case for all of it.
using TTD helps prevent complication while trying to fix error in the code when testing, since looking for the problem and finding a solution in a full code would be much more difficult.
the use or TTD improves code reliability since it makes sure the code is functioning well and constently refactors only the necessary code parts.
the development cycle:
create a list of new cases -> write a test code for one of them -> run the test with all other tests -> write the most simple code that passes the test -> refactor as needed.
we write the test case and run it knowing its going to fail, and make sure the new code solves it and does no extras.
tests should be small to avoid debugging and allow undoing or reverting.

\---



\# Development Workflows \& Architecture Concepts



\### ❓ Guide Questions



1\. Explain the difference between a \*\*Pull Request (PR)\*\*, \*\*Code Review (CR)\*\*,

&#x20;  and \*\*Design Review (DR)\*\*.  

&#x20;  Why are these processes important in team development?


PR - a pull request is a request made by a developer toget his code checked and approved by someone else.
CR - a code review is where you check that the code is actually written correctly, funtioning well and there are no mistakes. meaning it fits the standards required.
DR - a design review is when you review the design of a code (or anything else) to make sure it fits the code's purpose and functions and that the design is implemented well.
this is important in team development because it keeps the code under supervision to make sure no mistakes are being approved, constantly monitoring the progress of developers and improving while itws possible.


2\. Define the role of a \*\*Pull Request (PR) / Merge Request\*\*.

What is \*\*squashing\*\*? Why is it common practice to squash commits before the final merge?

Find how can you \*\*apply specific fixes\*\* from one branch to another without merging the entire history?

What is the process for \*\*safely undoing\*\* a merged PR using git revert?

a PR is a request for someone to review the code so changes/improvements would be done to it. a merge request is done after the PR is done, it means the code is approved and the request is to merge it with already-approved code.
squashing is squashing many commits to one large commit before the final one, its done with git merge --squash feature-branch. this makes the history more clean and clear but only available on private branches. or using rebase (git rebase -i HEAD~X). rebase keeps a linear commit history.
it's common to do squashing before the final merge to make sure the commit history isn't messy and overloaded with small commits (or just in general with many commits).
git revents allows you to undue a commit without changing the commits in commit history, thats why it is safe to use. what it does is just create another commit that does not include what we wanted to "undue" and with that it doesn't cause any loss of work (unlike restart).


3\. Explain the difference between \*\*CLI (Command Line Interface)\*\* and

&#x20;  \*\*UI (User Interface)\*\* applications.  

&#x20;  What are the benefits of each?

a CLI application is an application that is used from the command line (terminal) , while a UI application is an application that is used with an iteractive GUI representation.
a CLI application is more "hands-on" and could be easier depending on the use (pushing to git from pycharm terminal is easier than on the web), and on system or server adminastrations.
a UI application is easier to use and understand, you get more readable feedbecks. 


4\. What is the difference between a \*\*compiler\*\* and an \*\*interpreter\*\*?  

&#x20;  Provide examples of languages that use each approach.

a compiler quite litteraly compiles the code into lower level code that the computer can "understand" . it compiler source code into maching code all at ones for it to actually be executable. it takes time because it finds errors and problems in the code, but it is necessary in compiler based languagessuch as C, C++, etc...
an interpenter is translating higher level languages into machine languages line by line, without saving the machine language and without needing the full code. languages like python are interpented based. execution is done line by line after the interpentation and it catches errors line by line. there is no need to compile the entire code again when a change is made.



5\. What is \*\*event-driven programming\*\*?  

&#x20;  Explain how it differs from procedural execution and where it is commonly used.

event driven programming is writing code that acts according to certain external/internal events that happen and affect it in some ways. those could be coming from the keyboard, mice, or notifications from a thread.
in event driven programming there is usually a listening loop where an event triggers a callback function.
it deffers from procedural execution because it does not define a linear top to bottom chain of functions, the execution process could change according to the different events. 
procedure execution is commonly used in programs where there arent any events that would affect the results of the code. event driven programming would be used when there is a certain output or input that is affected by external intervine or internal entities that aren't pre-scheduled on a regular basis.
\---



\# Python \& API Foundations



\### ❓ Guide Questions



1\. What is \*\*Python\*\*, and what are its main characteristics compared to other

&#x20;  programming languages?  

&#x20;  Discuss readability, ecosystem, and runtime behavior.

python is a high lvel programming language that is known for being easy to write and read. the language is very flexible (for beig dynamically typed) and therefore very easy to use and understand.
python is object oriented and hybrid (both compiled and interpented) even though it is mostly interpented. the compilation or interpentation depends . python could be interpented straight from the original code or it could be compiled to bytecode and then the bytecode is interpented (Cpython). so the engine takes a place.
python can integrate with many third party libraries such as numpy, pandas, igraph for algorithms, matplotlib for vizualization, sqlalchemy for sql db and more.
the code is parsed and analyzed in run-time line by line.


2\. What is a \*\*REST API\*\*?  

&#x20;  Explain the core concepts such as resources, HTTP methods, and stateless communication.

REST API is a way for a client and server to communicate with eachother over HTTP requests using GET, POST, DELETE, and PUT. the response is usually in JSON format.
a request is being sent to the endpoint URL of the server, and a response is being sent as a JSON/XML/etc...
it's technically just a set of protocols that map the REST operations to CRUD operations.
usually a response would be a resource representation (most likely HTML page), and from that links ould be followed to make the state change and give more pages as responses.
the client and server are loosly coupled, meaning that only the first identifier is needed and the rest would be discovered without the client knowing.
REST API is stateless, meaning that when the client sends a requests it needs to include all of the relevent info about it's state because the REST API doesn't remember it.



3\. Compare \*\*Python 2\*\* and \*\*Python 3\*\*.

&#x20;  Explain the key differences in syntax, behavior, and long-term support, and why modern systems standardize on Python 3.

python 3 user print() instead of print '', it strings ad unicode instead of ASCII which is more versatile,it allows decimal devision of integers, and done much more changes.
overall the syntax is easier to understand, and improved performance.
python 2 is considered at the "end of its life" and wouldn't be supported very soon, python 3 gives a significante performence improvement and thats why most systems standardize on it.
the unicode change improves text processing and the standard library is much more effective.


&#x20;  \*\*Bonus:\*\* Compare \*\*FastAPI\*\* and \*\*Flask\*\*.

&#x20;  What are the architectural differences and when would you use each framework?

FastAPI is a web framework that is used to build API'S using python 3.7+ , one of the API'S it can create is REST API. it also provides automation for documating the service.
it provides built-in security ith sanitization and validation of user input, its used for scalable applications and works with nodeJS and go.
Flask is a micro-web framework that is used tobuild lightweight applications. unlike fastAPI it does not require any particular library or framework. it converts HTTP requests to WSGI' unlike fastAPI that instead of HTTP uses hints, and it uses jinja templeting. flask devides the application to small modules. it does not support asynchronic tasks or data validation like fastAPI.
in general fastAPI would have better performences in bigger, more I/O bound applications with large cocurrent connections.
flask is better for smaller applications that dont have many cocurrent connections (since its single threaded) and it also provides unit testing for it. and its better for applications that are  HTML oriented (it's main goal is not to write API'S).




4\. What are e2e testings? What are \*\*tests\*\* in software development, and why are they important?  

&#x20;  Explain unit tests, integration tests, and the role of automated testing.

e2e testing is end-to-end testing, it means validating an entire workflow from begginng to end to simulate the user's experience and make sure the application behaves as expected, that also means testing all possible cases.
they are important to make sure the system behaves like it should,it can be done through:
- unit testing - testing each of the components seperately to ake sure each works like it should.
- integration testing - combining modules and testing them as a group.
- security testing - evaluating vulnerabilities and making sure data is protected.
- usability testing - ealuating how user-friendly the website is.

e2e can be done either in execution until failure, or analysis techniques with no damage to the system, or by fault injection. 
all this can be done through automated testing that provide a structured and efficient way to write tests (in python using pytest) with the execution of the test being automated. systems like LambdaTest do that.



5\. What are \*\*mocks\*\*, and why are they used in testing?  

&#x20;  Compare \*\*pytest\*\* with other Python testing frameworks and explain its advantages.

mocks are a sub-package of unittest that let you mock the affects of testing without them actually happening, its and object that creates methods and attributes as you access them, and acts as an "insider" that lets you know how they would behave without then actually experiencing the affects.
mocks allow you to control your testing enviroment, you can define the responses or paths of the execution and not have to deal with external problems etc...
pytest is an autoaion testing framework that allows to do unit-testing,  integration tests and more in python code.
pytests passes the context for tests by passing them as parameters to the test cases which prevents duplicated code. it also provides assert methods that compare the output to the wanted one.
pytest is different than unittest, it's syntax is much more readable and it doesn't require test classes, which makes it much more flexible and easy to extend.
pytest also provides fixtures which is defined, reliable context for the test that can be passed, which unittest doesn't support.

\---

****************** skilla questions ************************
1. top-down and bottom-up : bottom-up means that you work on the smaller problems first and then integrate them' which gives you reusability of smaller components. top-down approach means you break the problem to bigger components and then you refine them to smaller ones, which is more simplifying and easier to implement.
2. the names of alternatives for TDD : Acceptance test-driven development (ATDD), behavior-driven development (BDD), example-driven development (EDD) and story test-driven development (SDD).
3. throw early catch later : a method where ou throw the exceptions as early as you find them and catch them in a later stage of the code, that can improve code readability and seperates error handling from the regular code flow.
4. .pyc file : the python code "compiled" into bytecde (by an interpenter, not actually compilation by a compiler).
5. tools that existed before git : cvs - centralized architecture , a single repository server where all changes were stored, compared to git it had weak branching and merging. svs - cvs with better branching and some other improvements. both cvs and svs are a single point of failure. clearcase - very strong but was very complicated.
6. why not pass boolean as a parameter : it goes against the single responsibility principle in SOLID since it has now more than one focus.
7. cherry git : a commend that allows to choose certain commits by reference to push to the head, can be used when a commit is done to the wrong branch.
8. what is fastAPI based on : python's pydantic that uses type hints. pydantic does data validatio by turning type hints to runtime validation rules using only one structure given. 
9. use a ds for the parameters if possible, split the function to multiple responsibilities and seperate the parameters. change the implementation.
10. how is git good for collaborative work : git allows prs, crs etc..., it allows users to change data and make progress simultaneously. when most of the files are non-shared and only some of them are or when we need to monitor work and not have immediate option to update data.

\### 🔄 Alternatives

Assignment: Research and briefly compare \*\*two development approaches or tools\*\* mentioned above.



Examples:

\- FastAPI vs Flask

\- Interpreted languages vs compiled languages



Deliverable:

\- A short written comparison (1–2 sentences).

\- Include a \*\*real-life use case\*\* for each alternative.



Goal:

Be able to explain \*\*why a specific tool or development approach would be chosen in a real system.\*\*



\---



\### 🎯 User Story \& Scenario

Assignment: Based on your research, describe a small example of a \*\*Python service or tool\*\*.



Deliverable:

Two short paragraphs describing:



\- A realistic scenario where a Python service is required.

\- How testing (pytest), mocking, and clean code practices would be applied.





