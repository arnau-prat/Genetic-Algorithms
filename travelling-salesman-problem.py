#!/usr/bin/env python

"""
Python implementation of http://www.theprojectspot.com/tutorial-post/creating-a-genetic-algorithm-for-beginners/3
"""

import math
import random
import matplotlib.pyplot as plt

class City:

    # Constructs a city chosen x,y location
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Gets city's x coordinate
    def getX(self):
        return self.x

    # Gets city's y coordinate
    def getY(self):
        return self.y

    # Gets the distances to given city
    def distanceTo(self, city):
        xDistance = abs(self.getX() - city.getX())
        yDistance = abs(self.getY() - city.getY())
        distance = math.sqrt(xDistance*xDistance + yDistance*yDistance)
        return distance

    def toString(self):
        print "("+str(self.getX())+","+str(self.getY())+") "

        return [self.getX(), self.getY()]

class TourManager:

    def __init__(self):
        self.destinationCities = []

    #Adds a destination city
    def addCity(self, city):
        self.destinationCities.append(city)

    # Get a city
    def getCity(self, index):
        return self.destinationCities[index]

    # Get the number of destination cities
    def numberOfCities(self):
        return len(self.destinationCities)  

class Tour:

    # Construct a blank tour
    def __init__(self):
        self.fitness = 0
        self.distance = 0
        self.tour = [None for i in range(tourManager.numberOfCities())]

    #Create a random individual
    def generateIndividual(self):
        # Loop through all our destination cities and add them to our tour
        for cityIndex in range(0, tourManager.numberOfCities()):
            self.setCity(cityIndex, tourManager.getCity(cityIndex))
        # Randomly reorder the tour
        random.shuffle(self.tour)

    # Gets a city from the tour
    def getCity(self, tourPosition):
        return self.tour[tourPosition]

    # Sets a city in a certain position within a tour
    def setCity(self, tourPosition, city):
        self.tour[tourPosition] = city
        self.fitness = 0
        self.distance = 0

    # Gets the tour fitness
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.getDistance())
        return self.fitness

    # Gets the total distance of the tour
    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for cityIndex in range(0, self.tourSize()):
                fromCity = self.getCity(cityIndex)
                if cityIndex+1 < self.tourSize():
                    destinationCity = self.getCity(cityIndex+1)
                else:
                    destinationCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(destinationCity)
            self.distance = tourDistance

        return self.distance

    # Get the number of cities on our tour
    def tourSize(self):
        return len(self.tour)

    # Check if the tour contains a city
    def containsCity(self, city):

        for i in range(0, tourManager.numberOfCities()):
            c = self.getCity(i)
            if c != None:
                if c.getX() == city.getX() and c.getY() == city.getY():
                    return True 
        return False

    def toString(self):

        array = []

        for i in range(0, self.tourSize()):
            array.append(self.getCity(i).toString())

        return array
            


class Population:

    def __init__(self, populationSize, initialise):
        self.tours = [Tour() for i in range(populationSize)]
        # If we need to initialise a population of tours do so
        if initialise:
            # Loop and create individuals
            for i in range(0, populationSize):
                newTour = Tour()
                newTour.generateIndividual()
                self.saveTour(i, newTour)

    # Saves a tour
    def saveTour(self, index, tour):
        self.tours[index] = tour

    # Gets a tour from population
    def getTour(self, index):
        return self.tours[index]

    # Gets the best tour in the population
    def getFittest(self):
        fittest = self.tours[0]
        # Loop through individuals to find fittest
        for i in range(1, self.populationSize()):
            if fittest.getFitness() <= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest

    # Gets population size
    def populationSize(self):
        return len(self.tours)


class GA:

    def __init__(self): 
        self.mutationRate = 0.025
        self.tournamentSize = 5
        self.elitism = True

    # Evolves a population over one generation
    def evolvePopulation(self, pop):
        newPopulation = Population(pop.populationSize(), False)

        # Keep our best individual if elitism is enabled
        elitismOffset = 0
        if self.elitism:
            newPopulation.saveTour(0, pop.getFittest())
            elitismOffset = 1

        #Crossover population
        for i in range(elitismOffset, newPopulation.populationSize()):
            # Select parents
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            # Crossover parents
            child = self.crossover(parent1, parent2)
            # Add child to new population
            newPopulation.saveTour(i, child)

        #Mutate the new population a bit to add some new genetic material
        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getTour(i))

        return newPopulation

    # Applies crossover to a set of parents and creates offset
    def crossover(self, parent1, parent2):
        # Create new child tour
        child = Tour()
        # Get start and end sub tour position for parent's tour
        startPos = random.randint(0, parent1.tourSize())
        endPos = random.randint(0, parent2.tourSize())

        # Loop and add the sub tour from partent1 to our child
        for i in range(0, child.tourSize()):
            # If our start position is less than the end position
            if (startPos < endPos and i > startPos and i < endPos):
                child.setCity(i, parent1.getCity(i))
            # If our start position is larger
            elif startPos > endPos and not (i < startPos and i > endPos):
                child.setCity(i, parent1.getCity(i))

        # Loop through parent2's city tour
        for i in range(0, parent2.tourSize()):
            # If child doesn't have the city add it
            if(not child.containsCity(parent2.getCity(i))):
                # Loop to find a spare position in the child's tour
                for ii in range(0, child.tourSize()):
                    # Spare position found, add city
                    if child.getCity(ii) == None:
                        child.setCity(ii, parent2.getCity(i))
                        break
        return child

    # Mutate a tour using swap mutation
    def mutate(self, tour):
        # Loop through tour cities
        for tourPos1 in range(0, tour.tourSize()):
            # Apply mutation rate
            if random.random() < self.mutationRate:
                # Get a second random position in the tour
                tourPos2 = int(tour.tourSize() * random.random())

                # Get the cities at target position in tour
                city1 = tour.getCity(tourPos1)
                city2 = tour.getCity(tourPos2)

                #Swap them around
                tour.setCity(tourPos2, city1)
                tour.setCity(tourPos1, city2)

    #Select candidate tour for crossover
    def tournamentSelection(self, pop):
        #Create a tournament population
        tournament = Population(self.tournamentSize, False)
        #For each place in the tournament get a random candidate tour and add it
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.populationSize())
            tournament.saveTour(i, pop.getTour(randomId))
        # Get the fittest tour
        fittest = tournament.getFittest()
        return fittest

if __name__ == '__main__':

    tourManager = TourManager()

    ga = GA()

    x = random.sample(xrange(1,200), 40)
    y = random.sample(xrange(1,200), 40)

    for i in range(0, 40):
        city = City(x[i], y[i])
        tourManager.addCity(city)

    """
    city = City(60, 200)
    tourManager.addCity(city)
    city = City(180, 200)
    tourManager.addCity(city)
    city = City(80, 180)
    tourManager.addCity(city)
    city = City(140, 180)
    tourManager.addCity(city)
    city = City(20, 160)
    tourManager.addCity(city)
    city = City(100, 160)
    tourManager.addCity(city)
    city = City(200, 160)
    tourManager.addCity(city)
    city = City(140, 140)
    tourManager.addCity(city)
    city = City(40, 120)
    tourManager.addCity(city)
    city = City(100, 120)
    tourManager.addCity(city)
    city = City(180, 100)
    tourManager.addCity(city)
    city = City(60, 80)
    tourManager.addCity(city)
    city = City(120, 80)
    tourManager.addCity(city)
    city = City(180, 60)
    tourManager.addCity(city)
    city = City(20, 40)
    tourManager.addCity(city)
    city = City(100, 40)
    tourManager.addCity(city)
    city = City(200, 40)
    tourManager.addCity(city)
    city = City(20, 20)
    tourManager.addCity(city)
    city = City(60, 20)
    tourManager.addCity(city)
    city = City(160, 20)
    tourManager.addCity(city)
    """

    pop = Population(50, True)

    print "Initial distance: "+str(pop.getFittest().getDistance())

    pop = ga.evolvePopulation(pop)
    for i in range(0, 500):
        pop = ga.evolvePopulation(pop)
        print "Final distance: "+str(pop.getFittest().getDistance())

    all_data = pop.getFittest().toString()
    for i in range(0,len(all_data)-1):
        plt.plot([all_data[(i)%tourManager.numberOfCities()][0], all_data[(i+1)%tourManager.numberOfCities()][0]],
                 [all_data[(i)%tourManager.numberOfCities()][1], all_data[(i+1)%tourManager.numberOfCities()][1]], 
                 color = 'brown', marker = 'o')

    plt.show()









