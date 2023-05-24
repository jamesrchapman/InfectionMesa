import random
from mesa import Agent, Model
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

class Person(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.infected = False
    
    def step(self):
        if self.infected:
            neighbors = self.model.grid.get_neighbors(self.pos)
            for neighbor in neighbors:
                if not neighbor.infected:
                    if random.random() < 0.5:
                        neighbor.infected = True

class InfectionModel(Model):
    def __init__(self, num_people):
        self.num_people = num_people
        self.schedule = RandomActivation(self)
        self.grid = NetworkGrid(self.num_people)
        
        for i in range(self.num_people):
            person = Person(i, self)
            self.schedule.add(person)
            self.grid.place_agent(person, i)
        
        patient_zero = random.choice(self.schedule.agents)
        patient_zero.infected = True

    def step(self):
        self.schedule.step()

# Create and run the model
model = InfectionModel(num_people=100)
for i in range(10):
    model.step()
