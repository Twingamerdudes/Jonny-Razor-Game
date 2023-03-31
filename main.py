import random
import openai
import time
import asyncio
import aioconsole

date = 0
#based on Myers-Briggs personality types
personalities = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
]
#culutral back-ground, skin-color, 10 races
races = [
    "white",
    "black",
    "asian",
    "hispanic",
    "hawaiian",
    "indian",
    "native",
    "north african",
    "alaska native",
    "pacific islander"
]
#age groups
agroups = [
    "0-17",
    "18-25",
    "26-35",
    "36-43",
    "44-50",
    "51-60",
    "61-70",
    "71-80",
    "81-90",
    "91-100"
]
#economic status
econ = [
    "poverty",
    "poor",
    "middle class",
    "upper middle class",
    "rich"
]
#genders
genders = [
    "Male",
    "Female"
]
currencyNames = [
    "gold",
    "silver",
    "copper",
    "rubles",
    "meme coins"
]
#time measurement names, not real
timeMeasurementNames = [
    "goldburgs",
    "ruls",
    "suns",
    "moons",
    "lunars",
]
currentQuest = ""
currencyName = currencyNames[random.randint(0, len(currencyNames) - 1)]
def GenerateVillageName():
    prompt = "Generate a name for a village in a fantasy world.\nVillage name:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"].strip()
openai.api_key = "YOUR_API_KEY"
villageName = GenerateVillageName()
timeMeasurement = timeMeasurementNames[random.randint(0, len(timeMeasurementNames) - 1)]
class NPC:
    def __init__(self):
        self.personality = personalities[random.randint(0, len(personalities) - 1)]
        self.race = races[random.randint(0, len(races) - 1)]
        self.age = agroups[random.randint(0, len(agroups) - 1)]
        self.econ = econ[random.randint(0, len(econ) - 1)]
        self.gender = genders[random.randint(0, len(genders) - 1)]
        self.hp = 100
        self.mainGoal = ""
        self.secondaryGoal = ""
        self.tertiaryGoal = ""
        self.tasks = []
        self.currentTask = ""
        self.job = ""
        self.taskProgress = 0
        self.name = ""
        self.chatHistory = [{}]
    def generateGoals(self):
        #The main goal is the life goal of the NPC, secondary and tertiary goals are smaller goals that the NPC is working towards
        prompt = "Generate goals for this person based on their personality, race, age, economic class, and gender.\n Personality: " + self.personality + "\n Race: " + self.race + "\n Age: " + self.age + "\n Economic Class: " + self.econ + "\nGender: " + self.gender + "\nGoals(seperate with a comma, only three goals, one main goal in life, and two short-term goals):"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        goals = response["choices"][0]["text"].strip().split(",")
        self.mainGoal = goals[0]
        self.secondaryGoal = goals[1]
        self.tertiaryGoal = goals[2]
    def generateJob(self):
        if self.age == "0-17":
            self.job = "Student"
        else:
            prompt = "Generate a job based on their goals in life. They also live in a small village in a fantasy like world.\nLife goal: " + self.mainGoal + ", Short term goals: " + self.secondaryGoal + ", " + self.tertiaryGoal + "\nJob(only provide job title):"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.9,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.job = response["choices"][0]["text"].strip()
    def getTasks(self, progressAmount=1):
        if self.tasks == []:
            prompt = "Generate tasks for this person based on goals and job (if it has a job).\nLife goal: " + self.mainGoal + ", Short term goals: " + self.secondaryGoal + ", " + self.tertiaryGoal + "\nJob: " + self.job + "\nTasks(seperate with a semicolon, don't list the tasks by numbers. Try to make tasks basic and not really important):"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.9,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            self.tasks = response["choices"][0]["text"].split(";")
        else:
            if self.taskProgress >= 100:
                self.tasks.pop(0)
                self.taskProgress = 0
                if self.tasks == []:
                    self.getTasks()
                self.currentTask = self.tasks[0]
            else:
                self.taskProgress += progressAmount
        self.currentTask = self.tasks[0]
        self.chatHistory[0] = {"role": "system", "content": "You are a NPC talking to the player. You will not disclose that you're a AI or a NPC. Here is some info about you. Personality (based on Myers-Briggs personality types): " + self.personality + ", Race: " + self.race + ", economic class: " + self.econ + ", gender: " + self.gender + ", age: " + self.age + ", life goal: " + self.mainGoal + ", short term goals: " + self.secondaryGoal + ", " + self.tertiaryGoal + ", job: " + self.job + ", current task: " + self.currentTask + ", current task progress: " + str(self.taskProgress) + "%. All player messages will also have a data attached to them based on one number, the amount of days since the start of the game. Do not put Date: (number) right before your message. You may however, tell the user the date in your message. The time measurement you use is called " + timeMeasurement + ". Only say you're response, pretend like you're a real person. If you buy or sell anything (don't sell anything if it isn't you're job), it is not using real money but a in-game currency called " + currencyName + ". You also live in a small village called " + villageName + " in a fantasy like world. If they player asks to go on a quest, then go on the quest with the player no matter what you are doing. If you accpeted the quest and there is no current quest add ;quest:(quest) to the end of your message. If you think a quest is over then put ;endquest at the end of you're message. During a quest, you will do anything the player says, it does not matter what job or goals you have. Here is the current quest (if it is blank, there is no quest): " + currentQuest + ". This is roleplay, do not break out of you're character."}
    def talk(self, message):
        #generate a random sentence based on the NPC's personality
        self.chatHistory.append({"role": "user", "content": "Date: " + str(date) + ", Message:" + message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chatHistory
        )
        message = response['choices'][0]['message']['content'].split(";")
        if len(message) > 1:
            global currentQuest
            if message[1] == "endquest":
                print("Quest Ended")
                currentQuest = ""
                self.getTasks()
                self.taskProgress = 0
            else:
                print("Quest Initiated: " + message[1].split(":")[1])
                currentQuest = message[1].strip()
                self.tasks[0] = currentQuest
                self.currentTask = currentQuest
                self.taskProgress = 0
        print(message[0])
    def GenerateName(self):
        prompt = "Generate a name for this person based on their personality, race, age, economic class, and gender.\n Personality: " + self.personality + "\n Race: " + self.race + "\n Age: " + self.age + "\n Economic Class: " + self.econ + "\nGender: " + self.gender + "\nGoals(seperate with a comma, only three goals, one main goal in life, and two short-term goals):"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
npc = NPC()
npc.generateGoals()
npc.generateJob()
npc.getTasks()
interacting = False
async def Main():
    global date
    global interacting
    while True:
        if not interacting:
            task = asyncio.create_task(Interact())
            interacting = True
        await asyncio.sleep(1)
        date += 0.1
        if currentQuest == "":
            npc.taskProgress += 50
            npc.getTasks()
async def Interact():
    global interacting
    #The game loop will first ask the player what they want to do
    print("What do you want to do?")
    print("1. Talk to a NPC")
    print("2. Quit")
    choice = await aioconsole.ainput()
    if choice == "1":
        npc.talk(await aioconsole.ainput("What do you want to say to the NPC? "))
    elif choice == "2":
        exit(0)
    else:
        print("Invalid choice")
    interacting = False
asyncio.run(Main())