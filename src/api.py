"""
FastAPI application for document analysis.
"""

import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException, Path as FastAPIPath
from fastapi.responses import JSONResponse
import logging

from model.analyzer import DocumentAnalyzer
from model.utils import DocumentStore
from model.types import DocumentType, Action

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Smart Document Analyzer API",
    description="API for analyzing and extracting metadata from documents",
    version="1.0.0"
)

# Initialize the document analyzer and document store
analyzer = DocumentAnalyzer()
document_store = DocumentStore()


def generate_mock_actions(document_type: str, document_id: str) -> List[Action]:
    """
    Generate mock actions based on document type.
    
    Args:
        document_type: Type of document
        document_id: Document ID
        
    Returns:
        List of mock actions
    """
    base_date = date.today()
    
    if document_type == DocumentType.CONTRACT.value:
        return [
            Action(
                id=str(uuid.uuid4()),
                title="Review Contract Terms",
                description="Review all terms and conditions in the contract for compliance",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=7)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Legal Approval",
                description="Obtain legal department approval for contract terms",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=14)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Stakeholder Review",
                description="Share contract with relevant stakeholders for review",
                status="pending",
                priority="medium",
                deadline=base_date + timedelta(days=10)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Contract Signing",
                description="Schedule and complete contract signing process",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=21)
            )
        ]
    
    elif document_type == DocumentType.INVOICE.value:
        return [
            Action(
                id=str(uuid.uuid4()),
                title="Verify Invoice Details",
                description="Cross-check invoice amounts, dates, and line items",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=3)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Approve for Payment",
                description="Obtain approval from authorized personnel for payment",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=5)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Process Payment",
                description="Initiate payment processing through accounting system",
                status="pending",
                priority="medium",
                deadline=base_date + timedelta(days=7)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="File for Records",
                description="Archive invoice in document management system",
                status="pending",
                priority="low",
                deadline=base_date + timedelta(days=10)
            )
        ]
    
    elif document_type == DocumentType.EARNINGS_REPORT.value:
        return [
            Action(
                id=str(uuid.uuid4()),
                title="Financial Review",
                description="Review financial metrics and performance indicators",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=5)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Stakeholder Communication",
                description="Prepare and distribute summary to key stakeholders",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=7)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Board Presentation",
                description="Prepare presentation materials for board meeting",
                status="pending",
                priority="medium",
                deadline=base_date + timedelta(days=14)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Regulatory Filing",
                description="Ensure compliance with regulatory reporting requirements",
                status="pending",
                priority="high",
                deadline=base_date + timedelta(days=10)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Market Analysis",
                description="Compare performance against industry benchmarks",
                status="pending",
                priority="medium",
                deadline=base_date + timedelta(days=12)
            )
        ]
    
    else:  # Unknown document type
        return [
            Action(
                id=str(uuid.uuid4()),
                title="Document Review",
                description="Review document content and determine appropriate actions",
                status="pending",
                priority="medium",
                deadline=base_date + timedelta(days=7)
            ),
            Action(
                id=str(uuid.uuid4()),
                title="Classification Review",
                description="Verify document classification and update if necessary",
                status="pending",
                priority="low",
                deadline=base_date + timedelta(days=5)
            )
        ]


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Smart Document Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze_document": "/documents/analyze",
            "get_analysis": "/documents/{document_id}",
            "list_documents": "/documents",
            "delete_analysis": "/documents/{document_id}",
            "storage_stats": "/documents/storage/stats",
            "supported_types": "/documents/supported-types",
            "document_actions": "/documents/{document_id}/actions"
        }
    }


@app.post("/documents/analyze")
async def analyze_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyze a document by classifying it and extracting metadata.
    
    Args:
        file: PDF file uploaded via multipart/form-data
        
    Returns:
        JSON response with analysis results
        
    Raises:
        HTTPException: If file is not a PDF or analysis fails
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a PDF file."
        )
    
    # Check file size (optional: limit to 10MB)
    if file.size and file.size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum size is 10MB."
        )
    
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Analyze the document
            logger.info(f"Analyzing document: {file.filename}")
            result = analyzer.analyze(temp_file_path)
            
            # Add the original filename to the result
            result["original_filename"] = file.filename
            
            # Store the analysis result
            document_id = document_store.store_analysis(result)
            result["document_id"] = document_id
            
            logger.info(f"Analysis completed and stored successfully for: {file.filename} (ID: {document_id})")
            return JSONResponse(content=result, status_code=200)
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {e}")
                
    except Exception as e:
        logger.error(f"Error analyzing document {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing document: {str(e)}"
        )


@app.get("/documents/{document_id}")
async def get_analysis(document_id: str = FastAPIPath(..., description="The document ID to retrieve")):
    """
    Retrieve a stored document analysis result.
    
    Args:
        document_id: The document ID to retrieve
        
    Returns:
        JSON response with the analysis result
        
    Raises:
        HTTPException: If document is not found
    """
    try:
        result = document_store.get_analysis(document_id)
        
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Document analysis not found for ID: {document_id}"
            )
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis for document ID {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document analysis: {str(e)}"
        )


@app.get("/documents")
async def list_documents() -> Dict[str, Any]:
    """
    List all stored document analyses with basic metadata.
    
    Returns:
        JSON response with list of documents and metadata
    """
    try:
        documents = document_store.list_documents()
        stats = document_store.get_storage_stats()
        
        return {
            "documents": documents,
            "total_count": len(documents),
            "storage_stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@app.delete("/documents/{document_id}")
async def delete_analysis(document_id: str = FastAPIPath(..., description="The document ID to delete")):
    """
    Delete a stored document analysis result.
    
    Args:
        document_id: The document ID to delete
        
    Returns:
        JSON response confirming deletion
        
    Raises:
        HTTPException: If document is not found or deletion fails
    """
    try:
        deleted = document_store.delete_analysis(document_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Document analysis not found for ID: {document_id}"
            )
        
        return {
            "message": f"Document analysis deleted successfully",
            "document_id": document_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting analysis for document ID {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document analysis: {str(e)}"
        )


@app.get("/documents/storage/stats")
async def get_storage_stats() -> Dict[str, Any]:
    """
    Get storage statistics for the document store.
    
    Returns:
        JSON response with storage statistics
    """
    try:
        stats = document_store.get_storage_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting storage stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving storage statistics: {str(e)}"
        )


@app.get("/documents/supported-types")
async def get_supported_document_types():
    """
    Get list of supported document types.
    
    Returns:
        JSON response with supported document types
    """
    try:
        supported_types = analyzer.get_supported_document_types()
        return {
            "supported_document_types": supported_types,
            "count": len(supported_types)
        }
    except Exception as e:
        logger.error(f"Error getting supported document types: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving supported document types: {str(e)}"
        )


@app.get("/documents/{document_id}/actions")
async def get_document_actions(document_id: str = FastAPIPath(..., description="The document ID to get actions for")):
    """
    Get actions for a specific document.
    
    Args:
        document_id: The document ID to get actions for
        
    Returns:
        JSON response with list of actions
        
    Raises:
        HTTPException: If document is not found
    """
    try:
        # Get the document analysis to determine its type
        result = document_store.get_analysis(document_id)
        
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Document analysis not found for ID: {document_id}"
            )
        
        # Extract document type from the analysis result
        # The document type is nested under classification.type
        classification = result.get("classification", {})
        document_type = classification.get("type", DocumentType.UNKNOWN.value)
        
        # Map the stored type to DocumentType enum values
        # The analyzer stores types in lowercase, but our enum uses proper case
        type_mapping = {
            "financial": DocumentType.EARNINGS_REPORT.value,
            "contract": DocumentType.CONTRACT.value,
            "invoice": DocumentType.INVOICE.value,
            "unknown": DocumentType.UNKNOWN.value
        }
        
        # Get the proper document type, defaulting to UNKNOWN if not found
        document_type = type_mapping.get(document_type.lower(), DocumentType.UNKNOWN.value)
        
        # Generate mock actions based on document type
        actions = generate_mock_actions(document_type, document_id)
        
        return {
            "document_id": document_id,
            "document_type": document_type,
            "actions": [action.dict() for action in actions],
            "total_actions": len(actions),
            "pending_actions": len([a for a in actions if a.status == "pending"]),
            "completed_actions": len([a for a in actions if a.status == "completed"])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving actions for document ID {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document actions: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 