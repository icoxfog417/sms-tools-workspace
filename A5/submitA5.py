### The only things you'll have to edit (unless you're porting this script over to a different language) 
### are at the bottom of this file.
import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys
import pickle
import json
import base64
import numpy as np
import matplotlib
matplotlib.use('pdf')

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
  def write(self, s):
    pass

def submit():   
  print '==\n== Submitting Solutions: Programming Assignment 5\n=='
  
  (login, password) = loginPrompt()
  if not login:
    print '!! Submission Cancelled'
    return
  
  print '\n== Connecting to Coursera ... '

  # Part Identifier
  (partIdx, sid) = partPrompt()

  # Get Challenge
  (login, ch, state, ch_aux) = getChallenge(login, sid) #sid is the "part identifier"
  if((not login) or (not ch) or (not state)):
    # Some error occured, error string in first return element.
    print '\n!! Error: %s\n' % login
    return

  # Attempt Submission with Challenge
  ch_resp = challengeResponse(login, password, ch)
  (result, string) = submitSolution(login, ch_resp, sid, output(partIdx), \
                                  source(partIdx), state, ch_aux)

  print '== %s' % string.strip()


# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  (login, password) = basicPrompt()
  return login, password


def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  login = raw_input('Login (Email address): ')
  password = raw_input('One-time Password (from the assignment page. This is NOT your own account\'s password): ')
  return login, password

def partPrompt():
  print 'Hello! These are the assignment parts that you can submit:'
  counter = 0
  for part in partFriendlyNames:
    counter += 1
    print str(counter) + ') ' + partFriendlyNames[counter - 1]
  partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
  return (partIdx, partIds[partIdx])

def getChallenge(email, sid):
  """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
  url = challenge_url()
  values = {'email_address' : email, 'assignment_part_sid' : sid, 'response_encoding' : 'delim'}
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  text = response.read().strip()

  # text is of the form email|ch|signature
  splits = text.split('|')
  if(len(splits) != 9):
    print 'Badly formatted challenge response: %s' % text
    return None
  return (splits[2], splits[4], splits[6], splits[8])

def challengeResponse(email, passwd, challenge):
  sha1 = hashlib.sha1()
  sha1.update("".join([challenge, passwd])) # hash the first elements
  digest = sha1.hexdigest()
  strAnswer = ''
  for i in range(0, len(digest)):
    strAnswer = strAnswer + digest[i]
  return strAnswer 
  
def challenge_url():
  """Returns the challenge url."""
  return "https://class.coursera.org/" + URL + "/assignment/challenge"

def submit_url():
  """Returns the submission url."""
  return "https://class.coursera.org/" + URL + "/assignment/submit"

def submitSolution(email_address, ch_resp, sid, output, source, state, ch_aux):
  """Submits a solution to the server. Returns (result, string)."""
  source_64_msg = email.message.Message()
  source_64_msg.set_payload(source)
  email.encoders.encode_base64(source_64_msg)

  output_64_msg = email.message.Message()
  output_64_msg.set_payload(output)
  email.encoders.encode_base64(output_64_msg)
  values = { 'assignment_part_sid' : sid, \
             'email_address' : email_address, \
             'submission' : output_64_msg.get_payload(), \
             'submission_aux' : source_64_msg.get_payload(), \
             'challenge_response' : ch_resp, \
             'state' : state \
           }
  url = submit_url()  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  string = response.read().strip()
  result = 0
  return result, string

## This collects the source code (just for logging purposes) 
def source(partIdx):
  # open the file, get all lines
  f = open(sourceFiles[partIdx])
  src = f.read() 
  f.close()
  return src

def convertNpObjToStr(obj):
  """
    if input object is a ndarray it will be converted into a dict holding dtype, shape and the data base64 encoded
    """
  if isinstance(obj, np.ndarray):
    obj = np.ascontiguousarray(obj)# this is a very important step, because many times the np object doesn't have its content in continous memory
    data_b64 = base64.b64encode(obj.data)
    return json.dumps(dict(__ndarray__=data_b64,dtype=str(obj.dtype),shape=obj.shape))
  return json.dumps(obj)

def convertStrToNpObj(dct):
    """
    Decodes a previously encoded numpy ndarray
    with proper shape and dtype
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    dct = json.loads(dct)
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return -1

def wrongOutputTypeError(outType):
  print "The output data type and/or size of your function doesn't match the expected answer data type/size (" + str(outType) + ")."
  print "Submission failed: Please correct and resubmit."
  


############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

from A5Part1 import minFreqEstErr
from A5Part2 import chirpTracker
from A5Part3 import mainlobeTracker
from A5Part4 import selectFlatPhasePeak
from A5Part5 import exploreSineModel

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'audio-001'

# the "Identifier" you used when creating the part
partIds = ['A5-part-1', 'A5-part-2', 'A5-part-3', 'A5-part-4', 'A5-part-5']
# used to generate readable run-time information for students
partFriendlyNames = ['Minimizing the frequency estimation error of a sinusoid', 'Tracking a two component chirp', 'Tracking sinusoids of different amplitudes', 'Tracking sinusoids using the phase spectrum', 'Sinusoidal modeling of a multicomponent signal (optional)'] 
# source files to collect (just for our records)
sourceFiles = ['A5Part1.py', 'A5Part2.py', 'A5Part3.py', 'A5Part4.py', 'A5Part5.py']

def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = ''

  dictInput = pickle.load(open("testInputA5.pkl"))  ## load the dict
  testCases = dictInput['testCases']
  outputType = dictInput['outputType']

  if partIdx == 0: # This is A5-part-1: minFreqEstErr
    for line in testCases['A5-part-1']:
      answer = minFreqEstErr(**line)
      if (outputType['A5-part-1'][0] == type(answer)) and (len(answer) == 3):
        if (str(type(answer[0])).count('float') and str(type(answer[1])).count('int') and str(type(answer[2])).count('int')):
          for ans in answer:  
            outputString += convertNpObjToStr(ans) + '\n'
          outputString += '\n'
        else:
          wrongOutputTypeError('float,int,int')
          sys.exit(1)
      else:
        wrongOutputTypeError(outputType['A5-part-1'][0])
        sys.exit(1)
      
  elif partIdx == 1: # This is A5-part-2: chirpTracker
    for line in testCases['A5-part-2']:
      answer = chirpTracker(**line)
      if (outputType['A5-part-2'][0] == type(answer)) and (len(answer) == 5):
        if (str(type(answer[0])).count('int') and str(type(answer[1])).count('int') and type(answer[2]) == np.ndarray and type(answer[3]) == np.ndarray and type(answer[4]) == np.ndarray):
          for ans in answer:
            outputString += convertNpObjToStr(ans) + '\n'
          outputString += '\n'
        else:
          wrongOutputTypeError('int,int,np.ndarray,np.ndarray,np.ndarray')
          sys.exit(1)
      else:
        wrongOutputTypeError(outputType['A5-part-2'][0])
        sys.exit(1)
      
  elif partIdx == 2: # This is A5-part-3: mainlobeTracker
    for line in testCases['A5-part-3']:
      answer = mainlobeTracker(**line) 
      if (outputType['A5-part-3'][0] == type(answer)) and (len(answer) == 5):
        if (type(answer[0]) == str and str(type(answer[1])).count('float') and type(answer[2]) == np.ndarray and type(answer[3]) == np.ndarray and type(answer[4]) == np.ndarray):  
          outputString = answer[0] + '\n'
          for ansInd in range(len(answer)-1):
            outputString += convertNpObjToStr(answer[ansInd+1]) + '\n'
          outputString += '\n'
        else:
          wrongOutputTypeError('str, float, np.ndarray, np.ndarray, np.ndarray')
          sys.exit(1)
      else:
        wrongOutputTypeError(outputType['A5-part-3'][0])
        sys.exit(1)        
        
  elif partIdx == 3: # This is A5-part-4: selectFlatPhasePeak
    for line in testCases['A5-part-4']:
      answer = selectFlatPhasePeak(**line) 
      if (outputType['A5-part-4'][0] == type(answer)):
        outputString += convertNpObjToStr(answer) + '\n'
      else:
        wrongOutputTypeError(outputType['A5-part-4'][0])
        sys.exit(1)
        
  elif partIdx == 4: # This is A5-part-5: exploreSineModel
    for line in testCases['A5-part-5']:
      answer = exploreSineModel(**line) 
      if (outputType['A5-part-5'][0] == type(answer)):
        outputString += convertNpObjToStr(answer) + '\n'
      else:
        wrongOutputTypeError(outputType['A5-part-5'][0])
        sys.exit(1) 

  return outputString.strip()

submit()
