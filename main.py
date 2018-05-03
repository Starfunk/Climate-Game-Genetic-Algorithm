#I employ a genetic algorithm to try to find the collective optimal outcome of the climate game. The climate game is based on 
#the paper: "The collective-risk social dilemma and the prevention of simulated dangerous climate change" written by 
#Milinski et al. - http://www.pnas.org/content/105/7/2291. I also drew inspiration from Wang & and Zhang's paper: 
#Agent-Based Modeling and Genetic Algorithm Simulation for the Climate Game Problem 
#- https://www.hindawi.com/journals/mpe/2012/709473/. I hope to be able to rewrite this program in Rust soon - 
#as soon as I get a laptop. 

import random

#Generate a random investment strategy
def generateIndividualStrategy():
	number_of_rounds = 10
	individual_investment = []
	
	for _i in range(number_of_rounds):
		individual_investment.append(investmentAmount());\
		
	total_contribution = calculateContribution(individual_investment)
	individual_investment.append(total_contribution)
	
	#Amount left in agent's account after investing
	account_balance = 40 - total_contribution
	individual_investment.append(account_balance)
	
	return individual_investment

#Generate a random investment amount: $0, $2, or $4	
def investmentAmount():
	rand_num = random.randint(0, 2);
	if rand_num == 0:
		return 0
	if rand_num == 1:
		return 2
	if rand_num == 2:
		return 4

#Generate a group of 6 individuals in an array
def generateInvestmentGroup():
	population = []
	for _i in range(6):
		population.append(generateIndividualStrategy())
	return population

#Group all the investment rounds into an array
def generateInitialPopulation():
	population = []
	for _i in range(10):
			population.append(generateInvestmentGroup())
	return population

#Sums the total contributions made to the climate account for 1 agent
def calculateContribution(individualInvestment):
	contribution = 0
	for i in individualInvestment[0:9]:
		contribution = contribution + i
	return contribution

#Accepts an array of arrays - i.e. an investment round made up of 6 individual investment strategies
def calculateClimateAccountTotal(investment_game):
	climate_account = 0
	for individual_contribution in investment_game:
		climate_account = climate_account + individual_contribution[10]
	return climate_account


#Roll a d10, if the number is 9 or less, the agent loses everything
def punish(investment_game, punish_probability):
	for individual_investment in investment_game:
		punish_roll = random.randint(1, 10)
		if punish_roll <= punish_probability:
			individual_investment[11] = 0
			
#This re-calculates the 11th element in the individual strategy array 
def resetScore(investment_game):
	for individual_investment in investment_game:
		total_contribution = calculateContribution(individual_investment)
		account_balance = 40 - total_contribution
		individual_investment[11] = account_balance
	
#This function sums each agent's account balance and returns the net gains of all the agents in one full game of investing. 
#This also serves as the fitness function for an investment game. I.e. an investment game is considered more fit the higher 
#the net balance after punishment is. 
def publishNetAccountBalance(investment_game):
	net_balance = 0
	for individual_investment in investment_game:
		net_balance = net_balance + individual_investment[11]
	return net_balance

#We use single point crossover to create two children investment games. We then return a tuple of the two lists, 
#which we can unpack outside of the function
def crossover(investment_game1, investment_game2): 
	crossover_point = random.randint(1,5)
	slice1 = investment_game1[0:crossover_point]
	slice2 = investment_game1[crossover_point + 1:6]
	slice3 = investment_game2[0:crossover_point]
	slice4 = investment_game2[crossover_point + 1:6]
	
	child1 = slice1 + slice4
	child2 = slice3 + slice2
	return (child1, child2)

def mutation(child1, child2):
	mutation_roll1 = random.randint(1,10)
	mutation_roll2 = random.randint(1,10)
	
	if mutation_roll1 == 1:
		child1[random.randint(1,6)][random.randint(1,10)] = investmentAmount()
		
	if mutation_roll2 == 1:
		child1[random.randint(1,6)][random.randint(1,10)] = investmentAmount()
		
	return (child1, child2)
	
#Replaces the bottom two worst performing investment games with the children of the most fit investment games
def replaceIndividuals(population, child1, child2):
	
	#The population has already been sorted. So the weakest games take positions 0 and 1.
	population[0] = child1
	population[1] = child2
	return population

#Probability that an agent will lose all their assets if the climate goal is not reached
_punish_probability = 3

#Main program starts here
initial_population = generateInitialPopulation()


for i in initial_population:
	if calculateClimateAccountTotal(i) < 120:
		punish(i, _punish_probability)


init_pop_sorted = sorted(initial_population, key = publishNetAccountBalance)

print(calculateClimateAccountTotal(init_pop_sorted[9]))
print(calculateClimateAccountTotal(init_pop_sorted[8]))
print(calculateClimateAccountTotal(init_pop_sorted[7]))
print(calculateClimateAccountTotal(init_pop_sorted[6]))

#Now reporting the values - CHANGE INDEX IF INDEX ERROR IS POPPING UP
for i in init_pop_sorted:
	counter = 1
	print("Game " + str(counter) + ":")
	print(publishNetAccountBalance(i))

for i in init_pop_sorted:
	init_pop_start = resetScore(i)


most_fit1 = init_pop_sorted[9]
most_fit2 = init_pop_sorted[8]
children = crossover(most_fit1, most_fit2)
children_mutated = (children[0], children[1])

init_pop_morph = replaceIndividuals(init_pop_sorted, children_mutated[0], children_mutated[1])

for i in init_pop_morph:
	if calculateClimateAccountTotal(i) < 120:
		punish(i, _punish_probability)

init_pop_sorted = sorted(init_pop_morph, key = publishNetAccountBalance)

for i in init_pop_sorted:
	counter = 2
	print("Game " + str(counter) + ":")
	print(publishNetAccountBalance(i))
	
counter = 2

#Simulating 1000 rounds of evolution
for i in range(1000):
	
	for i in init_pop_sorted:
		init_pop_start = resetScore(i)

	most_fit1 = init_pop_sorted[9]
	most_fit2 = init_pop_sorted[8]
	children = crossover(most_fit1, most_fit2)
	children_mutated = (children[0], children[1])

	init_pop_morph = replaceIndividuals(init_pop_sorted, children_mutated[0], children_mutated[1])

	for i in init_pop_morph:
		if calculateClimateAccountTotal(i) < 120:
			punish(i, _punish_probability)

	init_pop_sorted = sorted(init_pop_morph, key = publishNetAccountBalance)

	for i in init_pop_sorted:
		
		print("Game " + str(counter) + ":")
		print(publishNetAccountBalance(i))

	counter = counter + 1
