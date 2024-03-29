# -*- coding: utf-8 -*-
import os
import numpy as np
from mechanics.python.neperparser import NeperParser


def neper():
	# main function
	# write here input parameters
	# dimensions of the parallelepiped domain
	width = 100
	height = 100
	depth = 1
	# number of grains in neper generated polycrystal
	# note that the number of grains in abaqus could be lower
	# because only the ones intersecting the upper surface are considered
	# for the columnar grain structure
	Ngrains = 10*10

	# execute neper
	# custom neper options can be added to this part of the code
	# grain growth morphology is used here
	os.getcwd()
	comando = "neper -T -n " + str(Ngrains)
	comando = comando + " -dim 2"
	comando = comando + " -domain 'square(" + str(width) + "," + str(height) + ")'"
	comando = comando + " -morpho 'gg'"
	os.system(comando)

	# name of the tess file generated
	# may change in future versions of Neper
	tessfilename = "n" + str(Ngrains) + "-id1"

	# parse neper .tess file
	nepermodel = NeperParser(tessfilename)

	nepermodel.ReadEulerAngles()
	nepermodel.ReadVertices()
	nepermodel.ReadEdges()

	# report parameters to file that will be read by abaqus script
	fparam = open("Parameters.txt", "w")

	fparam.write(str(width) + '\n')
	fparam.write(str(height) + '\n')
	fparam.write(str(depth) + '\n')
	fparam.write(str(Ngrains) + '\n')
	fparam.write(os.getcwd())

	fparam.close()
