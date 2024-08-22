from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):

        result = await self.collection.insert_one(project.model_dump())
        project._id = result.inserted_id

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
            print("*****************0",project._id)

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
