import logging
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

from app.scraper import CendojScraper

logger = logging.getLogger("cendoj_mcp")

# Initialize FastMCP server
mcp = FastMCP("CENDOJ Jurisprudencia")

@mcp.tool(
    name="buscar_jurisprudencia",
    description="Busca resoluciones y sentencias judiciales en el portal del CENDOJ de España usando filtros avanzados."
)
async def buscar_jurisprudencia(
    query: Optional[str] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    jurisdiccion: Optional[List[str]] = None,
    roj: Optional[str] = None,
    ecli: Optional[str] = None,
    n_resolucion: Optional[str] = None,
    n_recurso: Optional[str] = None,
    ponente: Optional[str] = None,
    norma: Optional[str] = None,
    localizacion: Optional[List[str]] = None,
    page: int = 1
) -> str:
    """
    Busca sentencias judiciales en el CENDOJ con filtros detallados.

    Args:
        query: Texto libre para buscar en las sentencias (ej. 'cláusula suelo', 'despido improcedente') (opcional).
        fecha_desde: Fecha de inicio del rango de búsqueda en formato YYYY-MM-DD o DD/MM/AAAA (opcional).
        fecha_hasta: Fecha de fin del rango de búsqueda en formato YYYY-MM-DD o DD/MM/AAAA (opcional).
        jurisdiccion: Lista de jurisdicciones a filtrar. Valores válidos: 'Civil', 'Penal', 'Contencioso-Administrativo', 'Social', 'Militar' (opcional).
        roj: Identificador ROJ de la resolución (ej. 'STS 2849/2026') (opcional).
        ecli: Identificador ECLI de la resolución (ej. 'ES:TS:2026:2849') (opcional).
        n_resolucion: Número de la resolución (ej. '437/2026') (opcional).
        n_recurso: Número del recurso judicial (ej. '4115/2023') (opcional).
        ponente: Nombre del Magistrado ponente (opcional).
        norma: Ley, artículo o norma jurídica de interés (opcional).
        localizacion: Lista de Comunidades Autónomas/localizaciones a filtrar (ej. 'Cataluña', 'Madrid', 'Andalucía') (opcional).
        page: Número de página de resultados a recuperar (por defecto es 1).
    """
    logger.info(f"MCP Tool buscar_jurisprudencia called with query='{query}', roj='{roj}', ecli='{ecli}', page={page}, localizacion={localizacion}")
    try:
        async with CendojScraper() as scraper:
            response = await scraper.search(
                query=query,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
                jurisdiccion=jurisdiccion,
                roj=roj,
                ecli=ecli,
                n_resolucion=n_resolucion,
                n_recurso=n_recurso,
                ponente=ponente,
                norma=norma,
                localizacion=localizacion,
                page_num=page
            )
            return response.model_dump_json(indent=2)
    except Exception as e:
        logger.error(f"Error in buscar_jurisprudencia: {e}", exc_info=True)
        return f"Error al buscar jurisprudencia en CENDOJ: {str(e)}"

@mcp.tool(
    name="obtener_texto_resolucion",
    description="Descarga un PDF de sentencia de CENDOJ y extrae su texto plano."
)
async def obtener_texto_resolucion(pdf_url: str) -> str:
    """
    Descarga y extrae el texto plano de una resolución judicial a partir de su enlace directo PDF del CENDOJ.

    Args:
        pdf_url: El enlace de descarga directa del archivo PDF devuelto por la herramienta de búsqueda.
    """
    logger.info(f"MCP Tool obtener_texto_resolucion called with url='{pdf_url}'")
    try:
        async with CendojScraper() as scraper:
            text = await scraper.download_pdf_text(pdf_url)
            return text
    except Exception as e:
        logger.error(f"Error in obtener_texto_resolucion: {e}", exc_info=True)
        return f"Error al descargar y extraer texto del PDF: {str(e)}"
