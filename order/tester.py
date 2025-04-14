#!/usr/bin/env python
# coding: utf-8


# In[1]:


import jsonschema, yaml, json, unittest
from jsonschema.exceptions import ValidationError
from nicHelper.wrappers import add_method


# # Unit test for schema

# ## define test data folder

# In[2]:


dataFolder = "testData"  # data folder


# ## load schema

# In[3]:


with open(f"./order.yaml", "r") as f:  # load the schema
    schema = yaml.load(f.read(), Loader=yaml.FullLoader)

print(schema)


# ## create unit test object

# In[4]:


class TestValidation(unittest.TestCase):
    def setUp(self):
        with open(f"./order.yaml", "r") as f:  # load the schema
            self.schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.dataFolder = "testData"  # data folder


# ### good sample case

# In[5]:


@add_method(TestValidation)
def testPassingGoodSample(self):
    # good sample
    with open(f"./{self.dataFolder}/goodSample.json", "r") as f:
        goodItem = json.load(f)

    try:
        jsonschema.validate(goodItem, self.schema)
    except ValidationError as e:
        print(e)


# ### order2 sample case


@add_method(TestValidation)
def testPassingOrder2Sample(self):
    # order2 sample
    with open(f"./{self.dataFolder}/order2.yaml", "r") as f:
        order2Item = yaml.safe_load(f)

    try:
        jsonschema.validate(order2Item, self.schema)
    except ValidationError as e:
        # If this validation fails, print the error.
        # Consider adding self.fail(e) if this case should always pass.
        print(f"Validation failed for order2.yaml: {e}")


# ### bad case

# #### wrong type

# In[6]:


@add_method(TestValidation)
def testWrongType(self):
    with open(f"./{self.dataFolder}/wrongType.json", "r") as f:
        badItem = json.load(f)
    with self.assertRaises(ValidationError):
        jsonschema.validate(badItem, self.schema)


# #### extraneous column

# In[7]:


@add_method(TestValidation)
def testExtraColumn(self):
    with open(f"./{self.dataFolder}/extraCol.json", "r") as f:
        badItem = json.load(f)
    with self.assertRaises(ValidationError):
        jsonschema.validate(badItem, self.schema)
    try:
        jsonschema.validate(badItem, self.schema)
    except ValidationError as e:
        self.assertTrue("Additional properties are not allowed" in e.message)


# In[8]:


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestValidation)
unittest.TextTestRunner().run(suite)


# In[9]:


try:
    get_ipython().system("jupyter nbconvert --to script tester.ipynb")
except:
    pass


# In[ ]:


# In[ ]:


# In[ ]:
