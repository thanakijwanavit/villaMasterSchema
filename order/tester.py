#!/usr/bin/env python
# coding: utf-8




# In[1]:


import jsonschema, yaml, json, unittest
from jsonschema.exceptions import ValidationError
from nicHelper.wrappers import add_method


# # Unit test for schema

# ## define test data folder

# In[2]:


dataFolder = 'testData' # data folder


# ## load schema

# In[3]:


with open(f'./order.yaml', 'r')as f: # load the schema
    schema = yaml.load(f.read(), Loader=yaml.FullLoader)

print(schema)


# ## create unit test object

# In[4]:


class TestValidation(unittest.TestCase):
    def setUp(self):
        with open(f'./order.yaml', 'r')as f: # load the schema
            self.schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.dataFolder = 'testData' # data folder


# ### good sample case

# In[5]:


@add_method(TestValidation)
def testPassingGoodSample(self):
    # good sample
    with open(f'./{self.dataFolder}/goodSample.json','r')as f:
        goodItem = json.load(f)
    
    try:
        jsonschema.validate(goodItem,self.schema)
    except ValidationError as e:
        self.fail(f'goodSample.json should be valid: {e.message}')


# ### bad case

# #### wrong type

# In[6]:


@add_method(TestValidation)
def testWrongType(self):
    with open(f'./{self.dataFolder}/wrongType.json','r')as f:
        badItem = json.load(f)
    with self.assertRaises(ValidationError):
        jsonschema.validate(badItem,self.schema)
    try:
        jsonschema.validate(badItem,self.schema)
    except ValidationError as e:
        self.assertTrue("1234 is not of type 'string'" in e.message, 
                        f'wrong error message{e.message}, should be 1234 is not type string')


# #### extraneous column

# In[7]:


@add_method(TestValidation)
def testExtraColumn(self):
    # extra top-level keys are allowed: order.yaml keeps
    # "additionalProperties: false" commented out on purpose,
    # so extraCol.json (goodSample.json plus one unknown key) must validate
    with open(f'./{self.dataFolder}/extraCol.json','r')as f:
        extraItem = json.load(f)
    try:
        jsonschema.validate(extraItem,self.schema)
    except ValidationError as e:
        self.fail(f'extraCol.json should be valid, extra top-level keys are allowed: {e.message}')


# In[8]:


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestValidation)
result = unittest.TextTestRunner().run(suite)
if not result.wasSuccessful():
    raise SystemExit(1) # a failed test must fail the CI step


# In[9]:


try:
    get_ipython().system('jupyter nbconvert --to script tester.ipynb')
except:
    pass


# In[ ]:





# In[ ]:





# In[ ]:




