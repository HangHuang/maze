#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 上午9:48
# @Author  : future
# @File    : GA.py
# @summary :

# -*- coding: utf-8 -*-
import random
import maze as maze_api


def TestRoute(Path,maze_size,maze):
	posX = 0
	posY = 0
	offs = [[0, 1], [1, 0], [-1, 0], [0, -1]]

	for direction in Path:
		t_posX = posX + offs[direction][0]
		t_posY = posY + offs[direction][1]
		if t_posX >= 0 and t_posX < maze_size and t_posY >= 0 and t_posY < maze_size and maze[t_posX][t_posY] != 0:
			posX = t_posX
			posY = t_posY
		else:
			continue

	DiffX = abs(posX - (maze_size - 1))
	DiffY = abs(posY - (maze_size - 1))

	return 1.0/(DiffX + DiffY + 1)

class Genome(object):
	def __init__(self, num_bits): #check num_bits length
		self.Fitness = 0.0
		self.Bits    = []
		for i in range(num_bits):
			self.Bits.append(random.randint(0, 1))   # This loop can be replaced by:       map(lambda _:random.randint(0,1), xrange(num_bits))

	def _show(self):
		print(self.Bits, self.Fitness)

class GaBob(object):
	def __init__(self, cross_rat, mut_rate, pop_size, num_bits, gene_len,maze_size,maze):
		self.Genomes           = []
		self.PopSize           = pop_size
		self.CrossoverRate     = cross_rat
		self.MutationRate      = mut_rate
		self.ChromoLength      = num_bits
		self.GeneLength        = gene_len
		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0
		self.Generation        = 0
		self.Busy              = False
		self.maze_size         = maze_size
		self.maze              = maze
		pass

	def Run(self):
		self.CreateStartPopulation()
		self.Busy = True

	def _showPopulation(self):
		for i in range(self.PopSize):
			print(self.Genomes[i].Bits)

	def CreateStartPopulation(self):
		self.Genomes = []

		for i in range(self.PopSize):
			self.Genomes.append(Genome(self.ChromoLength))

		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0
		self.Generation        = 0
		return

	# 赌轮盘的选择方式:
	# 1. 随机生成一个在0到总适应度之间的值
	# 2. 遍历种群，对每个染色体的适应度进行累加
	# 3. 当遇到第一个大于1中生成的适应度的染色体时，停止累加，返回该染色体
	# 适应度越大的染色体被选中的概率越大
	def RouletteWheelSelection(self):
		fSlice  = random.random() * self.TotalFitnessScore
		cfTotal = 0.0
		SelectedGenome = 0

		for i in range(self.PopSize):
			cfTotal += self.Genomes[i].Fitness
			if cfTotal > fSlice:
				SelectedGenome = i
				break
		return self.Genomes[SelectedGenome]

	def Mutate(self, bits):  #bits is a list
		for i in range(len(bits)):
			if random.random() < self.MutationRate:
				if bits[i] == 0:  #if bitArray, it's more easy to reverse
					bits[i] = 1
				if bits[i] == 1:
					bits[i] = 0
		return bits

	def Crossover(self, mum, dad):
		if random.random() > self.CrossoverRate or mum == dad:
			return mum, dad

		cp = random.randint(0, self.ChromoLength - 1)
		return mum[:cp]+dad[cp:], dad[:cp]+mum[cp:]

	def BinToInt(self, bins):
		val = 0
		multiplier = 1
		for bin in bins[::-1]:
			val += bin * multiplier
			multiplier *= 2
		return val

	def Decode(self, bits):
		directions = []
		for i in range(0, len(bits), self.GeneLength):
			ThisGene = []
			for j in range(self.GeneLength):
				ThisGene.append(bits[i+j])
			directions.append(self.BinToInt(ThisGene))
		return directions

	def UpdateFitnessScores(self):
		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0

		for i in range(self.PopSize):
			directions = self.Decode(self.Genomes[i].Bits)
			self.Genomes[i].Fitness = TestRoute(directions,self.maze_size,self.maze)
			#print directions, self.Genomes[i].Fitness
			self.TotalFitnessScore += self.Genomes[i].Fitness

			if self.Genomes[i].Fitness > self.BestFitnessScore:
				self.BestFitnessScore = self.Genomes[i].Fitness
				self.FittestGenome = i
				if self.Genomes[i].Fitness == 1:
					#we found, stop
					print("Found Path")
					print("The hereditary algebra is ",self.Generation)
					self.Busy = False

		return

	def Epoch(self):
		self.UpdateFitnessScores()
		if not self.Busy:
			return
		NewBabies = 0
		BabyGenomes = []

		while NewBabies < self.PopSize:
			mum = self.RouletteWheelSelection()
			dad = self.RouletteWheelSelection()
			#print mum.Bits, dad.Bits
			baby1 = Genome(0)
			baby2 = Genome(0)
			baby1.Bits, baby2.Bits = self.Crossover(mum.Bits, dad.Bits)
			baby1.Bits = self.Mutate(baby1.Bits)
			baby2.Bits = self.Mutate(baby2.Bits)

			BabyGenomes.append(baby1)
			BabyGenomes.append(baby2)

			NewBabies += 2

		self.Genomes = BabyGenomes
		self.Generation += 1
		return

	def Started(self):
		return self.Busy

	def Stop(self):
		self.Busy = False
		return

	def GetFittestDirection(self):
		return self.Decode(self.Genomes[self.FittestGenome].Bits)



if __name__ == "__main__":
	maze_size = 5  # the length of maze
	wall_num = 7  # the number of wall
	random_init = 666666  # generate different labyrinths by modifying this parameter

	CROSSOVER_RATE = 0.7
	MUTATION_RATE  = 0.015
	POP_SIZE       = 20 # Number of individuals in the population
	CHROMO_LENGTH  = 30 # The length of the individual's genetic sequence
	GENE_LENGTH    = 2 # Number of codons for a single gene

	maze = maze_api.init_maze(size=maze_size, wall_num=wall_num, random_init=random_init)
	block_size = 40
	test_gaBob = GaBob(CROSSOVER_RATE, MUTATION_RATE, POP_SIZE, CHROMO_LENGTH, GENE_LENGTH,maze_size,maze)
	test_gaBob.Run()

	step = 0
	while test_gaBob.Started(): # Keep inheriting until you get out of the maze
		test_gaBob.Epoch()
		step += 1
		if step > 10000:
			print("Hereditary failure and extinction.... You can modify the random number seed to re-evolution")
	offs = [[0, 1], [1, 0], [-1, 0], [0, -1]]
	path = test_gaBob.GetFittestDirection()
	view_path = []
	for item in path:
		view_path.append(offs[item])
	maze_api.draw_path(maze,view_path,block_size,algrithmn_name="GA")

