<p align="center">
 <img src="/docs/Icon.png" width="150" height="150" >
</p> 

<p align="center">
 <a href="https://travis-ci.com/alexandrapurcarea/exercise-finder" alt="Build Status">
     <img src="https://travis-ci.com/alexandrapurcarea/exercise-finder.svg?branch=master" /></a>
  <a href="/LICENSE">
     <img src="https://img.shields.io/github/license/alexandrapurcarea/exercise-finder" /></a>
</p> 

# Exercise Finder
Being stuck in **self-isolation**, we have been spending time **looking for exercise resources** to help maintain fitness. Creating your own workout plan involves having to **look up exercises** that **match** your **equipment** and what parts of your **body** you want to focus on. We realised that this whole process could be greatly simplified by using Alexa as your **personal training coach**, giving you educated recommendations on what exercises to do. 

## What it does
Alexa will **recommend you exercises** based on the **body part** you want to strengthen and the **equipment** you have available. Further, given your specifications, Alexa can **create a to-do list of exercises** for a workout session. If you want to learn more about an exercise, or do not know how to do it, just ask Alexa, and she will **provide simple instructions**. 

## How we built it
We used the **Python ASK SDK** for the Alexa backend, in combination with the **wger Workout Manager API** to provide the exercise information. Further, we used the **Alexa list management API** to implement the workout lists.

## Challenges we ran into
We encountered problems **implementing request handlers** for the Alexa Conversation API using **Python**, as most learning resources **catered to Node.js**. To overcome this, we had to spend a lot of time really getting to know **how to debug Alexa skills**, via the **test simulator** and **Amazon CloudWatch**. Although it brought much frustration, it was ultimately a great learning experience on troubleshooting.

## Accomplishments that we're proud of
- We are proud of our skill. It was our **first self-made Alexa skill** (not following a tutorial).
- We are proud of our **systematic and methodical thinking** when it came to solving bugs, as many of them were undocumented, given how new Alexa Conversations is.

## What we learned
- How to create **user-friendly interaction models**
- How to plan out **happy paths** and handle their **deviations**.
- How to think about designing an **auditory application**, in contrast to a visual one (on a screen). 

## What's next for Exercise Finder
We would love to implement **stretch recommendations**, **full workout plans** (including the **duration/amount** of each exercise) and make the **instructions more intuitive**, whether that is through augmenting exercise descriptions to **cater to an auditory medium**, or providing more **insightful visual media**.

## Acknowledgments
#### The following creators' images were used in our skill's visual responses:
- [Mark Adriane](https://unsplash.com/photos/xQghSLXYD3M)
- [Victor Freitas](https://unsplash.com/photos/WvDYdXDzkhs)
- [Yulissa Tagle](https://unsplash.com/photos/2YCy6l14Opo)
- [Bruce Mars](https://unsplash.com/photos/gJtDg6WfMlQ)
- [Sergio Pedemonte](https://unsplash.com/photos/LqtHvyd80Mo)
- [Larry Crayton](https://unsplash.com/photos/ICwuKvw9QJk)
- [Jeff Tumale](https://unsplash.com/photos/bdIWJKLp98U)
- [Andrew Valdivia](https://unsplash.com/photos/0-A_G_XeUqc)
- [Dumitriu Robert](https://www.iconfinder.com/icons/3289577/fast_run_running_icon) ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/legalcode))

#### The following creator provided the font used in our skill's visual responses
- [Dalton Maag Ltd](https://www.onlinewebfonts.com/author/Dalton_Maag_Ltd) ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/legalcode))

### TODO
- **Basics**
 - [x] Create basic Alexa conversation model for exercise recommendations.
 - [x] Implement wger Workout Manager REST API with skill.
- **User experience**
 - [x] Make prompts sound more natural.
 - [x] Improve help messages for equipment and body part requests (enumerate all options).
- **Edge Cases**
 - [x] Handle if no exercise was found.
 - [x] Handle if there was an unsuccessful slot match.
- **Features**
 - [x] Allow for users to reprompt for a new exercise with already given specifications.
 - [x] Show guiding images for body parts and equipment.
 - [x] Create a to do list of exercises matching your specifications.
 - [ ] Allow user to repeat specific steps in an instruction.
 - [ ] Show images of exercise (currently unsupported by Alexa Conversations).
 - [ ] Allow users to press buttons when requesting to do something (currently unsupported by Alexa Conversations).
