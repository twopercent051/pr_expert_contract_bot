import os
from datetime import datetime

import docx
from num2words import num2words


def replace_text_in_paragraph(paragraph, key, value):
    if key in paragraph.text:
        inline = paragraph.runs

        for item in inline:
            print(item.text)
            if key in item.text:
                # print(key)
                item.text = item.text.replace(key, value)


def render_docx(render_dict: dict):
    template = render_dict["template"]
    # partner = render_dict["partner"]
    template_document = docx.Document(f"{os.getcwd()}/templates/{template}_ooo.docx")
    variables = render_dict["data"]
    for variable_key, variable_value in variables.items():
        for paragraph in template_document.paragraphs:
            replace_text_in_paragraph(paragraph, variable_key, variable_value)

        for table in template_document.tables:
            for col in table.columns:
                for cell in col.cells:
                    for paragraph in cell.paragraphs:
                        replace_text_in_paragraph(paragraph, variable_key, variable_value)

        section = template_document.sections[0]
        header = section.footer
        header_para = header.paragraphs
        for paragraph in header_para:
            print(paragraph.text)
            replace_text_in_paragraph(paragraph, variable_key, variable_value)

    template_document.save('result.docx')


def row_value(row: str) -> str:
    if len(row.split("||")) == 2:
        return str(row.split("||")[1].strip())
    else:
        return ""


def data_to_json(template: str, data_str: str) -> dict:
    months = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }
    rows = data_str.split("\n")
    day = str(datetime.today().day) if datetime.today().day > 9 else f"0{datetime.today().day}"
    year = str(datetime.today().year)
    price_int = row_value(rows[8])
    price_text = num2words(price_int, lang='ru')
    price = f"{price_int} ({price_text}"
    data_dict = dict(
        NUM_DEAL=row_value(rows[0]),
        DAY=day,
        MONTH=months[datetime.today().month],
        YEAR=year,
        COMPANY=row_value(rows[1]),
        DIR_NAME=row_value(rows[2]),
        SHORT_NAME=row_value(rows[3]),
        SITE=row_value(rows[4]),
        CONTACT=row_value(rows[5]),
        PHONE=row_value(rows[6]),
        EMAIL=row_value(rows[7]),
        PRICE=price,
        OFF_ADDRESS=row_value(rows[9]),
        POST_ADDRESS=row_value(rows[10]),
        INN=row_value(rows[11]),
        KPP=row_value(rows[12]),
        BANK_COUNT=row_value(rows[13]),
        BANK_NAME=row_value(rows[14]),
        COR_COUNT=row_value(rows[15]),
        BANK_ID=row_value(rows[16]),
    )
    render_dict = dict(
        template=template,
        # partner=partner,
        data=data_dict
    )
    render_docx(render_dict=render_dict)
