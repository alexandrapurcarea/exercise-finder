<p align="center">
 <img src="/docs/Icon.png" width="150" height="150" >
</p> 

<p align="center">
 <a href="https://travis-ci.com/alexandrapurcarea/exercise-finder" alt="Build Status">
     <img src="https://travis-ci.com/alexandrapurcarea/exercise-finder.svg?token=6xymSqzTey1a1nyeaEG9&branch=master" /></a>

# Exercise Finder
Being stuck in **self-isolation**, we have been spending time **looking for exercise resources** to help maintain fitness. Creating your own workout plan involves having to **look up exercises** that **match** your **equipment** and what parts of your **body** you want to focus on. We realised that this whole process could be greatly simplified by using Alexa as your **personal training coach**, giving you educated recommendations on what exercises to do. 

## What it does
Alexa will **recommend you exercises** based on the **body part**, or if you want to be more specific, **muscle**, you want to strengthen and the **equipment** you have available. Further, given your specifications, Alexa can **create a to-do list of exercises** for a workout session. If you want to learn more about an exercise, or do not know how to do it, just ask Alexa, and she will **provide simple instructions** accompanied with **images of the exercise**. 

## How we built it
We used the **Python ASK SDK** for the Alexa backend, in combination with the **wger Workout Manager API** to provide the exercise information.

## Challenges we ran into
We encountered problems **implementing request handlers** for the Alexa Conversation API using **Python**, as most learning resources **catered to Node.js**. To overcome this, we had to spend a lot of time really getting to know **how to debug Alexa skills**, via the **test simulator** and **Amazon CloudWatch**. Although it brought much frustration, it was ultimately a great learning experience on troubleshooting.

## Accomplishments that we're proud of
- We are proud of our skill. It was the **first self-made Alexa skill** (not following a tutorial).
- We are proud of our **systematic and methodical thinking** when it came to solving bugs, as many of them were undocumented, given how new Alexa Conversations is.

## What we learned
- How to create **user-friendly interaction models**
- How to plan out **happy paths** and handle their **deviations**.
- How to think about designing an **auditory application**, in contrast to a visual one (on a screen). 

## What's next for Exercise Finder
We would love to implement **stretch recommendations**, **full workout plans** (including the **duration/amount** of each exercise) and make the **instructions more intuitive**, whether that is through augmenting exercise descriptions to **cater to an auditory medium**, or providing more **insightful visual media**.

### TODO
- **Basics**
 - [x] Create Alexa conversation model for exercise recommendations.
 - [x] Implement wger Workout Manager REST API.
- **User experience**
 - [x] Make existing prompts sound more natural.
 - [x] Improve help messages for equipment and body part requests (enumerate all options).
 - **Edge cases**
 - [ ] Create handling for failed success matches of slot values.
- **New Features**
 - [ ] Allow for users to give muscles as input.
 - [ ] Allow for users to reprompt for a new exercise with already given specifications
 - [ ] Allow user to repeat specific steps in an instruction
 - [ ] Show images of exercise
 - [ ] Create a to do list of exercises matching your specifications
