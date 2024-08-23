from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.ini_collection()
        return instance

    async def ini_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name= index["name"],
                    unique= index["unique"]
                )

    async def create_project(self, project: Project):

        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id

        return project
    
    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id":project_id
        })
        print("******************* 1",record)
        if record is None:
            # create new project
            project = Project(project_id = project_id)
            project = await self.create_project(project=project)
            return project
        
        print("********************4",Project(**record).id)
        return Project(**record) # convert the dictionary to Project model <====> Project(_id=record["id"], project_id=record["project_id"])
    
    async def get_all_projects(self, page: int=1, page_size: int=10):

        # count the number of documents
        total_documents = await self.collection.count_documents({})

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1
        
        cursor = self.collection.find().skip( (page - 1) * page_size ).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )

        return projects, total_pages
