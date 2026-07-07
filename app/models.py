from pydantic import BaseModel, Field
from typing import List, Optional

class JurisprudenciaResult(BaseModel):
    id: str = Field(..., description="Identificador único de la resolución (hash/código)")
    titulo: str = Field(..., description="Título o resumen del tipo de sentencia")
    fecha: Optional[str] = Field(None, description="Fecha de la resolución (YYYY-MM-DD)")
    organo: Optional[str] = Field(None, description="Órgano judicial que dicta la resolución")
    sede: Optional[str] = Field(None, description="Sede o municipio del órgano judicial")
    ponente: Optional[str] = Field(None, description="Magistrado ponente")
    n_recurso: Optional[str] = Field(None, description="Número de recurso")
    n_resolucion: Optional[str] = Field(None, description="Número de resolución")
    roj: Optional[str] = Field(None, description="Identificador ROJ")
    ecli: Optional[str] = Field(None, description="Identificador ECLI")
    url_pdf: str = Field(..., description="URL de descarga del PDF en CENDOJ")
    resumen: Optional[str] = Field(None, description="Resumen breve o extracto del contenido")

class SearchQuery(BaseModel):
    query: Optional[str] = Field(None, description="Texto libre para buscar en las sentencias")
    fecha_desde: Optional[str] = Field(None, description="Fecha de inicio (DD/MM/AAAA o YYYY-MM-DD)")
    fecha_hasta: Optional[str] = Field(None, description="Fecha de fin (DD/MM/AAAA o YYYY-MM-DD)")
    jurisdiccion: Optional[List[str]] = Field(None, description="Lista de jurisdicciones a filtrar (Civil, Penal, Contencioso-Administrativo, Social, Militar)")
    roj: Optional[str] = Field(None, description="Identificador ROJ")
    ecli: Optional[str] = Field(None, description="Identificador ECLI")
    n_resolucion: Optional[str] = Field(None, description="Número de resolución")
    n_recurso: Optional[str] = Field(None, description="Número de recurso")
    ponente: Optional[str] = Field(None, description="Magistrado ponente")
    norma: Optional[str] = Field(None, description="Legislación o norma de interés")
    localizacion: Optional[List[str]] = Field(None, description="Lista de comunidades autónomas/localizaciones a filtrar (Andalucía, Madrid, Cataluña, etc.)")
    page: int = Field(1, description="Número de página de resultados")

class SearchResponse(BaseModel):
    total: int = Field(..., description="Número total de resultados encontrados")
    results: List[JurisprudenciaResult] = Field(..., description="Lista de resultados de la búsqueda")
