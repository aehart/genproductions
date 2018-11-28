#!/usr/bin/env python
import os

def insertSLHA(outputName, massValue):
	with open(outputName, 'r+') as f:
			for x in range(5):
				f.readline()
			pos = f.tell()
			f_remainder = f.read()
			f.seek(pos)
			with open('slha/Higgsino_%dGeV_Isajet780.slha' % massValue, 'r') as slhaFile:
				f.write(slhaFile.read())
			f.write(f_remainder)

def findMassValue(fileName, particleName):
	inputFile = open(fileName, 'r')
	for line in inputFile:
		if particleName in line:
			return line.split()[1]

baseConfigFile = 'Higgsino_M-XXXGeV_CTau-YYYcm_TuneCP5_13TeV_pythia8_cff.py'
baseParticleFile = 'geant4_higgsino.slha'

c = 299792458.0 * 100.0 # cm/s

# xsecs[mass in GeV] = xsec (pb)
xsecs = {
	100 : 13.53557,
	200 : 1.092653,
	300 : 0.2342024,
	400 : 0.0731865,
	500 : 0.02798925,
	600 : 0.0121587,
	700 : 0.00572751,
	800 : 0.002878806,
	900 : 0.001502429
}

ctaus = [10, 100, 1000, 10000] # cm

for mass in xsecs:
	for ctau in ctaus:
		outputConfigFile = 'test/Higgsino_M-%dGeV_CTau-%dcm_TuneCP5_13TeV_pythia8_cff.py' % (mass, ctau)
		outputParticleFile = 'test/geant4_higgsino_%dGeV_ctau%dcm.slha' % (mass, ctau)

		os.system('sed "s/XXX/' + str(mass) + '/g" ' + baseConfigFile + ' > ' + outputConfigFile)
		os.system('sed -i "s/YYY/' + str(int(ctau * 10.0)) + '/g" ' + outputConfigFile) # mm
		os.system('sed -i "s/ZZZ/' + str(xsecs[mass]) + '/g" ' + outputConfigFile)
		insertSLHA(outputConfigFile, mass)

		mW1ss = findMassValue(outputConfigFile, 'w1ss')
		mZ1ss = findMassValue(outputConfigFile, 'z1ss')

		tau = ctau / c * 1.e9 # ns
		width = (1.97326979e-14 / ctau) # GeV

		os.system('sed "s/_MW1SS/' + str(mW1ss) + '/g" ' + baseParticleFile + ' > ' + outputParticleFile)
		os.system('sed -i "s/_MZ1SS/' + str(mZ1ss) + '/g" ' + outputParticleFile)
		os.system('sed -i "s/_CTAU/' + str(ctau) + '/g" ' + outputParticleFile)
		os.system('sed -i "s/_TAU/' + str(tau) + '/g" ' + outputParticleFile)
		os.system('sed -i "s/_WIDTH/' + str(width) + '/g" ' + outputParticleFile)

print 'Created configuration fragments and particle files in directory: ' + os.getcwd() + '/test/'
