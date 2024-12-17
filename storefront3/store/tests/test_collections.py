#test_collections.py is a module for testing the colections endpoint:
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest
from store.models import Collection
from model_bakery import baker

@pytest.fixture
#here we're creating a fixture for creating a collection inside this module(test_collections.py not in conftest.py) cuz creating collections is very specific to this module
def create_collection(api_client): #we pass the api_client fixture here cuz we need the APIClient to post a request to the server
    def do_create_collection(collection):# we created this inner function cuz if we put "collection " inside the def_collection method with the api_client,pytest will think its a fixture which is not and that'll cause an error
        return api_client.post('/store/collections/', collection)
    return do_create_collection
#now we can apply this fixture to any test method:


@pytest.mark.django_db
class TestCreateCollection: #the name of the class should always start with "Test"
##############################
    '''
#writing a test:
#a test mthod that tests if the user is authenticated when creating collection. if not(meaning if the user is anonymous), it returns a 401 error:
    def test_if_user_is_anonymous_returns_401(self): #always start the method naming with "test" otherwise python will not pick up the test
        
        #now here our test should have 3 forms which we call AAA(Arrange,Act ,Assert):
        #Arrange: for preparing the system under test meaning this is where we create objects or we put out database in an initial state and soon:
            #no need of arrange here for this case so just empty
            
        #Act:this is where we kick off the behaviour we wanna test
            #in this case this is where we wanna send a request to the server        
        client=APIClient() #to send a request to the server
        response=client.post("/store/collections/", {'title':'a'}) #sending a post request to /store/collections/ and the 2nd argument is just including a body into the request object
        
        #Assert:this is where we check to see if the behaviour we expect happens or not:
            #in this case we expect to get a 401 response from the server
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 
        #every test you write no matter what framework or language you use must include this sructure(the AAA structure) 
        '''
        
########################################################
#Fixtures: powerfull feature in pytest used to remove duplication inthe test code:
#e.g: we will use the fixture for regitering the apiclient on the commented fisrt function above by copying it here
#here we will use the reusable function(fixture) in the conftest.py to avoid duplication for this function(method):
    def test_if_user_is_anonymous_returns_401(self,api_client,create_collection): #here we used the api_client and create_collection fixtures by adding them inside the function an a parameter
        #act
        response=create_collection({'title':'a'})  #better(cleaner) than response=api_client.post('/store/collections/',{'title':'a'})
        #assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
#now you can use this fixture to any method downthere:
#######################################
#authenticating the user:
#a test method that tests a user that is authenticated but not admin:
    def test_if_user_is_not_admin_returns_403(self,authenticate,api_client,create_collection):
        #arrange:
        authenticate() #better than api_client.force_authenticate(user={})
        #act
        response=create_collection({'title':'a'})  #better(cleaner) than response=api_client.post('/store/collections/',{'title':'a'})
        #assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
          
#######################################
#single or multiple assertions:somtimes a test may need multiple assertions:
#e.g:
#a test method that that test if a user is authenticated and the current user is admin but the data posted into the server is invalid:
    def test_if_data_is_invalid_returns_400(self,authenticate,api_client,create_collection):
        #arrange:
        authenticate(is_staff=True)# client.force_authenticate(user=User(is_staff=True))
        #act:
        response=create_collection({'title':'a'})  #better(cleaner) than response=api_client.post('/store/collections/',{'title':'a'})
        #assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None 
        #even if using only one assertion per test is the best practice,using the 2 assertions above is okay cuz they are logicaly related (meaning we're testing the response that we get from the server on both assertions )
        
#a test method that that test if a user is authenticated and the current user is admin and this time, the data posted into the server is valid:
    def test_if_data_is_valid_returns_201(self,api_client,create_collection):
        #arrange:
        authenticate(is_staff=True)# client.force_authenticate(user=User(is_staff=True))
        #Act:
        response=create_collection({'title':'a'})  #better(cleaner) than response=api_client.post('/store/collections/',{'title':'a'})
        #assert:
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0 
        
##########################################
#creating model instances:
#let's write a test for retrieving a collection:
@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self,api_client):
        #arrange:
        #here we need to create a collection so we can retirieve it later cuz this shouldn't be dependent on the other tests that create a collection meaning if this test is executed 1st,it'll fail cuz there is no collection in the database
        #there're 2 ways to create a collection:
        # #1)use the api_client to send a post request to the collections endpint:
        # api_client.post('/store/collections') #the problem with this approach is that if there is a bug when creating collection,then this line'll fail
        
        #2)use the collection model:(a better way)
        # #we ca do this using to ways:
        # Collection.objects.create(title='a') #but what if we wanted to create a product?we know that the product model has alot of fields.initializing all those fields overhere will make a bit of noise in this test 
        #so we will use a library called "model_bakery" .on the terminal  ,type pipenv install --dev model_bakery then import it on the top of this module
        collection=baker.make(Collection)#now this model baker will take care of initializing all those fields for us
        #note: we're breaking the "during testing,test the behaviour not the implementation" rule cuz the Collection model is part of the implementation but we don't have a choise so it's okay to break the rule
        
        #ACt:
        response=api_client.get(f'/store/collections/{collection.id}/')
        
        #assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id':collection.id,
            'title': collection.title,
            'products_count': 0
            }