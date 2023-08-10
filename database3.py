import aiohttp
from aiodataloader import DataLoader
from aiohttp.client_exceptions import ClientResponseError
import asyncio

# Data loading using the aiohttp and asyncio libraries
#   inspired by hrbolek/uoishelepres

class CouchDBDataLoader(DataLoader):
    def __init__(self, db_url, db_name):
        """
        The function initializes a class instance with a database URL, database name, batch size, and a
        client session.
        
        :param db_url: The `db_url` parameter is the URL or address of the database you want to connect
        to. It should be a string that specifies the location of the database server
        :param db_name: The `db_name` parameter is the name of the database you want to connect to. It
        is used to specify which database you want to interact with when making database queries or
        operations
        """
        super().__init__()
        self.db_url = db_url
        self.db_name = db_name
        self.batch_size = 10  # Set your desired batch size here
        self.session = aiohttp.ClientSession()

    async def fetch_documents(self, keys):
        """
        The function fetches documents from a specified database using a POST request and returns the
        values of the documents.
        
        :param keys: The `keys` parameter is a list of keys that you want to use for fetching documents
        from the database. These keys will be used to filter the documents returned by the view
        specified in the URL
        :return: a list of values from the "value" field of each row in the response data.
        """
        try:
            async with self.session.post(
                f"{self.db_url}/{self.db_name}/_design/my_views/_view/id_view",
                json={"keys": keys},
                headers={"Content-Type": "application/json"},
            ) as response:
                response_data = await response.json()
              #  print(response_data)
                #documents = [{"_id": row["id"], "name": row["value"]} for row in response_data["rows"]]
                #return documents
                return [row["value"] for row in response_data["rows"]]
        except ClientResponseError as e:
            print(f"Error fetching documents: {e}")
            return []

    async def batch_load_fn(self, keys):
        """
        The function `batch_load_fn` asynchronously fetches documents based on a list of keys and
        returns a list of documents in the same order as the input keys.
        
        :param keys: The `keys` parameter is a list of keys that need to be loaded. These keys are used
        to fetch documents from a data source
        :return: a list of documents corresponding to the input keys. If a document is not found for a
        particular key, None is returned in its place.
        """
        print("loading keys", keys)
        datamap = {}
        not_found_keys = set(keys)
        while not_found_keys:
            current_keys = list(not_found_keys)[: self.batch_size]
            not_found_keys -= set(current_keys)

            documents = await self.fetch_documents(current_keys)
            for doc in documents:
                datamap[doc["_id"]] = doc

        result = [datamap.get(id, None) for id in keys]
        print(result)
        return result

    async def close(self):
        """
        The function closes the session.
        """
        await self.session.close()

async def main():
    """
    The main function loads data from a CouchDB database using a batch load function and prints the
    result.
    """
    db_url = "http://admin:password@localhost:5984"
    db_name = "students"

    loader = CouchDBDataLoader(db_url, db_name)
    keys = ["class_id_2", "teacher_id_1", "student_id_3"]
    result = await loader.batch_load_fn(keys)

    results = [loader.load(key) for key in keys] # load se může v různých častech volat v jednotlivých dotazích
    # simulace různých požadavků
    results = await asyncio.gather(*results)
    # všechny awaitables se načtou což vede k jednomu dotazu
    print(result)
    print(results)

    await loader.close()

# The `if __name__ == "__main__"` block is a common Python idiom that allows a script to be executed
# as a standalone program or imported as a module.
if __name__ == "__main__":
    asyncio.run(main())
