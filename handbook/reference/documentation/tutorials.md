# Tutorials Guide

## Purpose

This guide provides practical steps for creating effective tutorials following the Diátaxis framework. A tutorial is an experience that takes place under the guidance of a tutor. A tutorial is always learning-oriented. This document helps documentation writers craft tutorials that build learner confidence through carefully designed, hands-on experiences.

## Prerequisites

- Understanding of the Diátaxis framework's four documentation types
- Basic technical writing skills
- Access to the system or product being documented
- Ability to test instructions with beginners

## Understanding Tutorial Fundamentals

### Step 1: Recognize What Makes a Tutorial

A tutorial differs fundamentally from other documentation types. A tutorial is a practical activity, in which the student learns by doing something meaningful, towards some achievable goal. Unlike how-to guides that solve problems, tutorials create controlled learning experiences.

**Example: Tutorial vs How-to Guide**
```markdown
# Tutorial: Your First Python Game (✓)
Let's create a number guessing game together...

# How-to: Configure Game Difficulty Settings (✗)
To adjust difficulty levels in your game...
```

The tutorial creates a learning journey; the how-to assumes existing knowledge.

### Step 2: Design Around Learning, Not Features

Structure tutorials around what learners need to discover, not product capabilities. It's important to understand that while a student will learn by doing, what the student does is not necessarily what they learn. Focus on foundational concepts that enable future independent work.

**Example: Learning-Centered Design**
```python
# Poor: Feature-focused
# "Let's explore all string methods"

# Better: Learning-focused  
# "Let's build a word game to discover text manipulation"
print("Welcome! Enter a word:")
word = input()
print(f"Your word has {len(word)} letters!")
```

## Creating the Tutorial Structure

### Step 3: Establish Clear Learning Objectives

Begin with concrete achievement, not abstract concepts. Providing the picture the learner needs in a tutorial can be as simple as informing them at the outset: In this tutorial we will create and deploy a scalable web application.

**Example: Effective Tutorial Opening**
```markdown
# Building Your First Weather Dashboard

In this tutorial, we'll create a live weather display 
that shows current conditions for any city. You'll see 
your dashboard update in real-time as we build it together.

By the end, you'll have:
- A working weather application
- Experience with API calls
- Understanding of data display
```

### Step 4: Create Meaningful Checkpoints

Every step the learner follows should produce a comprehensible result, however small. Design visible progress markers that confirm success and maintain momentum.

**Example: Progressive Results**
```markdown
## Step 2: Display Your First Temperature

1. Add this code to your file:
   ```python
   temperature = 72
   print(f"Current temperature: {temperature}°F")
   ```

2. Run your program. You should see:
   ```
   Current temperature: 72°F
   ```

Congratulations! You've displayed your first data point.
```

## Writing Tutorial Content

### Step 5: Minimize Explanation Ruthlessly

A tutorial is not the place for explanation. In a tutorial, the user is focused on correctly following your directions and getting the expected results. Provide only essential context, linking to detailed explanations elsewhere.

**Example: Appropriate Explanation Level**
```markdown
# Too Much Explanation (✗)
We use HTTPS because it encrypts data using TLS protocols,
preventing man-in-the-middle attacks through certificate 
validation and symmetric key exchange...

# Just Right (✓)
We use HTTPS because it's more secure. 
[Learn more about HTTPS →](../explanation/https-security.md)
```

### Step 6: Maintain Narrative Guidance

Keep up a narrative of expectations: "You will notice that …"; "After a few moments, the server responds with …". Guide learners through each transition with clear signposts.

**Example: Narrative Flow**
```markdown
3. Click "Deploy". You'll see a progress bar appear.

   After about 30 seconds, the status will change to 
   "Live". Your application is now accessible worldwide!

   Notice the URL displayed - this is your app's address.
   
4. Open the URL in a new tab. You should see your 
   weather dashboard displaying "Loading..."
```

### Step 7: Use First-Person Plural Voice

The first-person plural affirms the relationship between tutor and learner: you are not alone; we are in this together. This creates psychological safety and reduces intimidation.

**Example: Voice Comparison**
```markdown
# Distant (✗)
Users must configure their environment variables.

# Collaborative (✓)  
Let's set up our environment variables together.
```

## Ensuring Tutorial Success

### Step 8: Design for Perfect Reliability

A tutorial must inspire confidence. Confidence can only be built up layer by layer, and is easily shaken. Test exhaustively to ensure every learner succeeds.

**Example: Reliability Checklist**
```markdown
Before Publishing:
- [ ] Fresh OS install test
- [ ] Different Python versions (3.8, 3.9, 3.10)
- [ ] Windows, Mac, Linux variations
- [ ] Slow internet connections
- [ ] Behind corporate firewalls
- [ ] Non-English system locales
```

### Step 9: Handle Common Failure Points

Anticipate where learners might stumble and provide safety nets without disrupting flow.

**Example: Graceful Error Handling**
```markdown
5. Install the weather library:
   ```bash
   pip install weatherapi
   ```

   If you see "pip: command not found", you'll need to 
   install Python first. [Quick Python setup →](../install)
   
   For "Permission denied" errors, try:
   ```bash
   pip install --user weatherapi
   ```
```

### Step 10: Create Meaningful Completion

Describe (and admire, in a mild way) what your learner has accomplished. Celebrate achievement while pointing toward next steps.

**Example: Tutorial Conclusion**
```markdown
## Congratulations!

You've built a live weather dashboard that:
- Fetches real-time data from weather services
- Updates automatically every minute  
- Handles errors gracefully

Your dashboard is now running at: https://your-app.com

### What You've Learned
Through building this project, you've discovered how to:
- Make API requests
- Parse JSON data
- Update displays dynamically

### Next Steps
Ready to extend your dashboard?
- [Add a 5-day forecast](../how-to/add-forecast.md)
- [Include weather maps](../how-to/integrate-maps.md)
- [Understand how APIs work](../explanation/api-basics.md)
```

## Testing and Validation

### Step 11: Conduct Beginner Testing

The ultimate test of a tutorial is whether beginners succeed independently. Testing with experts catches technical errors but misses learning obstacles.

**Example: Testing Protocol**
```markdown
1. Recruit 3-5 complete beginners
2. Provide only the tutorial link
3. Observe without intervening
4. Note every hesitation or confusion
5. Revise based on patterns observed
```

### Step 12: Monitor Long-term Reliability

Product changes constantly threaten tutorial integrity. Establish automated testing to catch breaking changes early.

**Example: Automated Validation**
```python
# weekly_tutorial_test.py
def test_weather_tutorial():
    # Test each command from tutorial
    assert run_command("pip install weatherapi") == 0
    assert api_endpoint_exists("weather.com/api/v1")
    assert example_response_format_unchanged()
```

## Common Anti-Patterns to Avoid

### The Explanation Trap

Writers naturally want to explain why things work. Resist this urge completely during tutorials.

**Anti-pattern Example:**
```markdown
# Don't do this in tutorials:
"We use async/await because JavaScript is single-threaded
and needs non-blocking I/O to handle concurrent operations
efficiently..."
```

### The Alternative Path Maze

Offering choices paralyzes beginners. Make decisions for them.

**Anti-pattern Example:**
```markdown
# Avoid options in tutorials:
"You can use either fetch(), axios, or XMLHttpRequest.
Each has trade-offs. Fetch is modern but..."
```

### The Knowledge Assumption

Never assume prior knowledge beyond stated prerequisites.

**Anti-pattern Example:**
```markdown
# Don't assume:
"Obviously, configure your CORS headers first..."
```

## Performance Considerations

Tutorial performance differs from execution performance. Optimize for learning speed, not code efficiency.

**Example: Learning vs Performance**
```python
# Optimized for learning (✓)
names = ["Alice", "Bob", "Carol"]
for name in names:
    print(f"Hello, {name}!")

# Optimized for performance (✗ for tutorials)
print("\n".join(f"Hello, {n}!" for n in ["Alice","Bob","Carol"]))
```

The verbose version helps learners understand each step.

## Maintenance Strategy

Tutorials require more maintenance than any other documentation type. Their end-to-end nature means single changes cascade throughout.

**Maintenance Checklist:**
- Weekly: Run automated tests
- Monthly: Check user feedback patterns
- Quarterly: Full beginner re-test
- Yearly: Evaluate learning objectives relevance

## Quick Reference Card

| Element | Tutorial Approach |
|---------|------------------|
| **Purpose** | Enable learning through doing |
| **Voice** | First-person plural ("we", "let's") |
| **Explanation** | Minimal, with links to details |
| **Alternatives** | None - one blessed path |
| **Testing** | With complete beginners |
| **Success Metric** | Learner confidence and completion |
| **Maintenance** | Continuous, automated where possible |

## Conclusion

Writing effective tutorials requires suppressing many natural writing instincts. The urge to explain, to cover edge cases, to demonstrate expertise - all must be set aside in service of the learner's experience. The teacher has responsibility for what the pupil is to learn, what the pupil will do in order to learn it, and for the pupil's success. 

Success comes from maintaining laser focus on the learner's journey, ensuring every step builds confidence through visible achievement. When done well, tutorials transform curious beginners into capable practitioners, ready to explore your documentation's how-to guides, references, and explanations independently.