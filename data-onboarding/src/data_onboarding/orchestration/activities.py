


from temporalio import activity



@activity.defn
async def process_document_activity(source_system: str, source_id: str) -> str:
    ...
    # return "INGESTED"



