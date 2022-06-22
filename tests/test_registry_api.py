import unittest
from typing import List

import requests

from tno.mmvib_registry.models.modeladapter import ModelAdapter, ModelAdapterState
from tno.mmvib_registry.settings import EnvSettings

base_url = "http://localhost:" + str(EnvSettings.flask_server_port())


class RegistryTest(unittest.TestCase):
    def test1_get_list(self):
        print('get list test')
        response = requests.get(url=base_url + '/registry') # returns a list

        self.assertEqual(response.status_code, 200)
        json = response.json()[0]
        print(json)
        model = ModelAdapter.Schema().load(json)
        print(model)
        self.assertEqual(model.name, "ESSIM")
        print(model.status)

    def test2_post_model(self):
        print("post test")
        m = ModelAdapter(name="Opera", version="2022-06-01", max_workers=1, used_workers=0,
                         status=ModelAdapterState.READY, uri="mqtt://mmvib/opera", owner="Joost van Stralen")
        model_data = ModelAdapter.Schema().dump(m)
        print(model_data)
        response = requests.post(url=base_url + '/registry/', json=model_data)
        print(response.json())
        print(ModelAdapter.Schema().load(response.json()))


    def test3_search(self):
        print("test_search")
        search_data = {'name': 'ESSIM'}
        response = requests.post(url=base_url + '/registry/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        #print(response)
        models = ModelAdapter.Schema().load(response.json(), many=True)
        print(models)

    def test4_search_by_int(self):
        print("test_search with int")
        search_data = {'max_workers': 1}
        response = requests.post(url=base_url + '/registry/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        #print(response)
        models = ModelAdapter.Schema().load(response.json(), many=True)
        print(models)

    def test5_search_by_enum(self):
        print("test_search with enum")
        search_data = {'status': "READY"}
        response = requests.post(url=base_url + '/registry/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        #print(response)
        models = ModelAdapter.Schema().load(response.json(), many=True)
        print(models)

    def test6_get_by_id(self):
        model_id = 'uniqueid'
        response = requests.get(url=base_url + '/registry/'+model_id)  # returns a list
        self.assertEqual(response.status_code, 200)
        model = ModelAdapter.Schema().load(response.json())
        print(model)
        self.assertEqual(model.id, model_id)

    def test7_search_and_delete(self):
        print("test_search_and_delete")
        search_data = {'name': 'Opera'}
        response = requests.post(url=base_url + '/registry/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        models: List[ModelAdapter] = ModelAdapter.Schema().load(response.json(), many=True)
        self.assertGreater(len(models), 0)
        for ma in models:
            response = requests.delete(url=base_url + '/registry/'+ma.id)
            self.assertEqual(response.status_code, 204)
            print('deleted', ma)
        # check if everything is deleted
        response = requests.post(url=base_url + '/registry/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        models: List[ModelAdapter] = ModelAdapter.Schema().load(response.json(), many=True)
        self.assertEqual(len(models), 0)


if __name__ == '__main__':
    unittest.main()
