
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

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
  def write(self, s):
    pass

def submit():   
  print '==\n== Submitting Solutions for Programming Assignment 4 \n=='
  
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

def wrongOutputTypeError(outType):
  print "The output data type of your function doesn't match the expected data type (" + str(outType) + ")."
  print "Submission failed: Please correct and resubmit."


############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

from A4Part1 import extractMainLobe
from A4Part2 import computeSNR
from A4Part3 import computeEngEnv
from A4Part4 import computeODF

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'audio-001'

# the "Identifier" you used when creating the part
partIds = ['A4-part-1', 'A4-part-2', 'A4-part-3', 'A4-part-4']
# used to generate readable run-time information for students
partFriendlyNames = [ 'Extracting the main lobe of the spectrum of a window', 
                      'Measuring noise in the reconstructed signal using STFT model',
                      'Computing band-wise energy envelopes of a signal',
                      'Computing onset detection function'] 
# source files to collect (just for our records)
sourceFiles = ['A4Part1.py', 'A4Part2.py', 'A4Part3.py', 'A4Part4.py']

def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = ''
  dictInput = pickle.load(open("testInputA4.pkl"))  ## load the dictionary containing output types and test cases
  testCases = dictInput['testCases']
  outputType = dictInput['outputType']
  
  if partIdx == 0: # This is A4-part-1: extractMainLobe
    for line in testCases['A4-part-1']:
      answer = extractMainLobe(**line)
      if outputType['A4-part-1'][0] == type(answer):
        outputString += convertNpObjToStr(answer) + '\n'
      else:
        wrongOutputTypeError(outputType['A4-part-1'][0])
        sys.exit(1)
  
  elif partIdx == 1: # This is A4-part-2: computeSNR
    for line in testCases['A4-part-2']:
      answer = computeSNR(**line)
      if outputType['A4-part-2'][0] == type(answer):
        if len(answer)==2:
          outputString += convertNpObjToStr(np.array([answer[0], answer[1]])) + '\n'
        else:
          print "The output python tuple should contain only 2 elements (SNR1, SNR2)"
          sys.exit(1)
      else:
        wrongOutputTypeError(outputType['A4-part-2'][0])
        sys.exit(1)      
      
  elif partIdx == 2: # This is A4-part-3: computeEngEnv
    for line in testCases['A4-part-3']:
      answer = computeEngEnv(**line)
      if outputType['A4-part-3'][0] == type(answer):
        outputString += convertNpObjToStr(answer) + '\n'
      else:
        wrongOutputTypeError(outputType['A4-part-3'][0])
        sys.exit(1)         
      
  elif partIdx == 3: # This is A2-part-4: computeODF
    for line in testCases['A4-part-4']:
      answer = computeODF(**line)
      if outputType['A4-part-4'][0] == type(answer):
        outputString += convertNpObjToStr(answer) + '\n'
      else:
        wrongOutputTypeError(outputType['A4-part-4'][0])
        sys.exit(1)       

  return outputString.strip()

submit()
