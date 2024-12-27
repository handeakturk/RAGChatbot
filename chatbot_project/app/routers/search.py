import time
import textwrap
from fastapi import FastAPI
from fastapi import APIRouter
from app.configs.logger.logging import logger
from app.services.chains import get_rag_chain
from app.configs.logger.logger_utils import determine_log_level, add_log
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/search/")
async def search_articles(request: QueryRequest):
    query = request.query
    logger.info(f"Received query: {query}")
    chat_history = []
    status_code = 200

    try:
        rag_chain = get_rag_chain(chat_history, query)
        response = rag_chain.invoke({"input": query, "chat_history": chat_history})

        if isinstance(response, dict):
            answer = response.get("answer", "Yanıt bulunamadı")
        else:
            answer = response

        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": answer})
        
        duration = time.time()
        log_level = determine_log_level(status_code)

        add_log(
            request="POST /search/",
            response=answer,
            duration=duration,
            log_level=log_level,
            query_data=query
        )
        return {"query": query, "answer": textwrap.fill(answer, width=88)}
    except Exception as e:
        logger.error("Error during query execution: %s", e)
        status_code = 500
        duration = 0
        log_level = determine_log_level(status_code)

        add_log(
            request="POST /search/",
            response=f"{status_code} Internal Server Error",
            duration=duration,
            log_level=log_level,
            query_data=query
        )
        return {"error": str(e)}
    
    

