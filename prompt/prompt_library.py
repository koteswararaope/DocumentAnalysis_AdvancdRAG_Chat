from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(""" 
                                          you are highly capable assistant trained to analyze and summarize documents.
                                          return only valid JSON matching the exact schema below
                                          {format_instructions}
                                          Ananlyze this document:
                                          {document_text}
                                          """)