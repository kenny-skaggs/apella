
from curriculum import html_processing, view_models
from storage import repository


def store_page(page: view_models.Page):
    # TODO: have a way to parse/modify and save the html in the same upsert transaction
    upsert_page = repository.PageRepository.upsert(page)

    parser = html_processing.QuestionParser(page_id=upsert_page.id)
    upsert_page.html = parser.process_html(upsert_page.html)

    last_page_update = repository.PageRepository.upsert(upsert_page)
    return last_page_update.id, parser.id_resolution_map
