# Header
from Experiment import *

## Define parameters
params = {}

params['mode'] = 'real'

params['categories'] = ('face','house','letter')
# Get filenames of pictures 
inFiles = list()
extension = ".png"
thispath = os.getcwd()
for category in params['categories']:
	searchString = os.path.join(thispath,'stimuli', category, category+'*'+extension) 
	inFiles.append(glob.glob(searchString))
params['stimuli'] = inFiles # a 3 (category) by 100 (n unique pics) list

# Ports and Triggers
try:
	portOut = parallel.PParallelInpOut32(address=0x378); portOut.setData(0)
	portIn = parallel.PParallelInpOut32(address=0x379); portIn.setData(0)
except AttributeError:
	portOut=portIn=None
params['ports'] = [portOut,portIn]

# Create trigger dictionary, handy for indexing with names
params['triggers'] = {
	'practice_long': 91,
	'practice_short': 92,
	'practice_mixed': 93,
	'mixed': 	20,
	'blocked': 	0,
	'long':		20,
	'short':	10,
	'face': 	1,
	'house': 	2,
	'letter': 	3,
	'search':	50,
	'absent': 	0,
	'present': 	1
}

# Where should behavioral data be stored?
params['data_directory'] = 'data'

# subject/session ID
params['subject_id'] = raw_input("Subject ID: ")
# params['session_no'] = raw_input("Session: ")

# Monitor / screen
fS = raw_input("Full screen? Y/N: ")
if any(ans in fS for ans in['n','N']):
	params['fullScreen'] = False
else:
        params['fullScreen'] = True

params['monitor_refRate'] = 120 # 60hz for macbook; 120hz for lab 
params['monitor_width'] = 47.5
params['monitor_viewdist'] = 90
params['screenSize'] = [1680, 1050]

mon = monitors.Monitor(name = 'HP', width = params['monitor_width'], distance = params['monitor_viewdist'])
mon.setSizePix(params['screenSize'])
myWin = visual.Window(params['screenSize'], units = 'deg', monitor = mon, fullscr=params['fullScreen'])
myWin.mouseVisible = False
params['screen'] = myWin

# Trial/stim settings
params['absent_present'] = ('absent','present')
params['short_long'] = ('short','long')
params['cue_stim_size'] = 2 # resize fraction (2 means half size)
params['search_stim_size'] = 4 # quarter of original picture size
params['search_set_size'] = 6
params['search_radius'] = 4.5
params['search_angle'] = 2*pi/params['search_set_size']

# Response
if portIn:
	params['resp_keys'] = [39,71]
else:
	params['resp_keys'] = ['f','j']

# The above parameters are assigned to the corresponding stimuli that need these as settings; this is done in Trial.py
# The actual index of some parameters (e.g. the true/false for present/absent get index 0/1 respectively) is determined in Experiment.py

# Timing
params['timing_ITI_Duration']    = 1.0 # ITI
params['timing_ITI_Jitter']      = 0.5 # set to 0 if no jitter
params['timing_target_Duration'] = .25 # duration of stimulus presentation, in sec
params['timing_ISI_Duration']    = [3,6] #

if (int(params['subject_id']) % 2 == 0): # evend
	block_order = ('short','long','mixed')
else: # odd
	block_order = ('long','short','mixed')
	
#### GO ####

# first a practice block with task instructions and example trials

for b,block in enumerate(block_order):

	# practice block
	params['block_type'] = ('practice_' + block)
	params['ready_text'] = ('stimuli/ready_practice_'  + block + '.txt')
	params['ntrials']    = 12 # needs to be divided by 3 categories
	params['rep_check']  = (12,4) # in chuncks of 12 trials, it is checked whether repetitions of 4 or more occur for absent/present
	params['nblocks']    = 1 
	exp = Experiment(params) 

	if b==0: # show some additional explanation screens if first block
		exp.run_instruction('stimuli/instruct1.txt')
		exp.run_example_trial(['face',inFiles[0][0],'present','examp_short','example'])
		exp.run_instruction('stimuli/instruct2.txt')
		exp.run_example_trial(['house',inFiles[1][10],'absent','examp_long','example'])
		exp.run_instruction('stimuli/instruct3.txt')
	exp.run()
	if b==len(block_order)-1:
		exp.run_instruction('stimuli/finish_practice.txt')

for b,block in enumerate(block_order):

	# experimental block
	params['block_type'] = block
	params['ready_text'] = ('stimuli/ready_' + block + '.txt')
	params['ntrials']    = 168 # needs to be divided by 3 (categories)
	params['nblocks']    = 6
	params['rep_check']  = (params['ntrials']/params['nblocks'],5) # 168 trials are divided up in 8 chuncks of 30 where absent/present is shuffled such that no 5 repetitions are allowed
	exp = Experiment(params) 
	exp.run()
	if exp.finished():
	   exp.store()

	   if b==2:
		   exp.run_instruction('stimuli/finish_exp.txt')

# END #
#################################################

# -- parallel port check -- #
##toggle=True
##while toggle:
##        val=portIn.readData()
##        if not val==7:
##                print(val)
##                toggle=False
##quit()

