# Task Priority

This is a test project made with ChatGPT with simple prompts (and some adaptations). This application creates a rank os priority of tasks, first input a list of tasks (step 1), then, choose the most important task of each two pairs (step 2).

Demo: [https://task-priority.onrender.com/](https://task-priority.onrender.com/)

----

The used prompts are:

```
1. Create a web application in python where you can enter any number of tasks as text, then it will show the tasks in pairs for the user to choose which one is the priority. Once it count the preference for each task, it will show a rank of the tasks by priority
```

It created a dash application with 3 html templates, but was not updating.

```
2. The session['comparisons'].pop(0) is not updating
```

Attempt to changed for the `dash` app with `dash-bootstrap-components`.

```
3. Make this application using dash bootstrap components
```
It worked, with a bug.

```
4. it says that are 'Duplicate callback outputs'
```

That bug it kept on generating, which had to be manually fixed.