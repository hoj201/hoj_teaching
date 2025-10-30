from .seats import Table
from typing import List
from math import sqrt, ceil

import xml.etree.ElementTree as ET


WIDTH = 1920
HEIGHT = 1080
HEADER_SIZE = "54"
FONT_SIZE = "44"
FONT_FAMILY = "Helvetica"
BG_COLOR = "#13005e"
BULLET = "\u2022"

def make_slides(tables: List[Table], announcements: List[str], agenda: List[str], donows: List[str], exam_mode: bool) -> ET.Element:    
    # Create the root <svg> element with its attributes
    svg_attributes = {
        "width": str(WIDTH),
        "height": str(HEIGHT),
        "xmlns": "http://www.w3.org/2000/svg"
    }
    svg = ET.Element('svg', svg_attributes)
    ET.SubElement(svg, 'rect', attrib={
        "width": "100%",
        "height": "100%",
        "fill": BG_COLOR
    })
    insert_tables(tables, svg, exam_mode)
    insert_agenda(agenda, svg)
    insert_announcements(announcements, svg)
    insert_donows(donows, svg)
    return svg

def insert_tables(tables: List[Table], svg: ET.Element, exam_mode: bool):
    width = int(svg.attrib["width"])
    height = int(svg.attrib["height"])-100
    n_rows = ceil(sqrt(len(tables)))
    n_cols = n_rows # we will assume a square arrangement
    dx = min(width,height) // n_cols
    if len(tables) > 36:
        raise ValueError("Slide code assumes fewer than 36 tables")
    if exam_mode:
        front_text = ET.SubElement(svg, 'text',{
            "x": str(width//3),
            "y": "100",
            "font-family": FONT_FAMILY,
            "font-size": HEADER_SIZE,
            "fill": "white",
            "text-anchor": "middle",
        })
        front_text.text = "FRONT"
    for index, table in enumerate(tables):
        offset_x = (index % n_rows) * dx + dx//2
        offset_y = (index // n_cols) * dx + dx//2 + 100 # add 100 to fit text at the top
        # Create the <circle> element as a sub-element of <svg>
        circle = ET.SubElement(svg, 'circle', {
            "cx": str(offset_x),
            "cy": str(offset_y),
            "r": str(dx//2),
            "fill": "#5C0500",
            "stroke": "black",
            "stroke-width": "4"
        })

        # Create the <text> element and add it to <svg>
        t1 = ET.SubElement(svg, 'text', {
            "x": str(offset_x),
            "y": str(offset_y - 50),
            "font-family": FONT_FAMILY,
            "font-size": HEADER_SIZE,
            "fill": "white",
            "text-anchor": "middle",
        })
        if not exam_mode:
            t1.text = f"Table {index+1}" # Set the text content inside the tag
        for student in table:
            t1_student = ET.SubElement(t1, 'tspan', {
                "x": str(offset_x),
                "dy": "1.2em",
                "font-size": FONT_SIZE,
            })
            t1_student.text = student.name

def insert_agenda(agenda_items: List[str], svg: ET.Element):
    width = int(svg.attrib["width"])
    height = int(svg.attrib["height"])
    agenda_x = width-1.9*width//5
    agenda_y = height //10
    agenda = ET.SubElement(svg, 'text', {
        "x": str(agenda_x),
        "y": str(agenda_y),
        "font-family": FONT_FAMILY,
        "font-size": HEADER_SIZE,
        "fill": "white",
        "text-anchor": "left",
    })
    agenda.text = "Agenda"
    insert_tspan_list(agenda, agenda_items)

def insert_announcements(announcements: List[str], svg: ET.Element):
    width = int(svg.attrib["width"])
    height = int(svg.attrib["height"])
    x = width-1.9*width//5
    ann_elem = ET.SubElement(svg, 'text', {
        "x": str(x),
        "y": str(height//3 + 50),
        "font-family": FONT_FAMILY,
        "font-size": HEADER_SIZE,
        "fill": "white",
        "text-anchor": "left",
    })
    ann_elem.text = "Announcements"
    insert_tspan_list(ann_elem, announcements)


def insert_donows(items: List[str], svg: ET.Element):
    width = int(svg.attrib["width"])
    height = int(svg.attrib["height"])
    x = width-1.9*width//5
    donow = ET.SubElement(svg, 'text', {
        "x": str(x),
        "y": str(2*height//3),
        "font-family": FONT_FAMILY,
        "font-size": HEADER_SIZE,
        "fill": "white",
        "text-anchor": "left",
    })
    donow.text = "Do Now"
    insert_tspan_list(donow, items)

def insert_tspan_list(parent: ET.Element, items: List[str]):
    for item in items:
        element = ET.SubElement(parent, 'tspan', {
            "dy": "1.2em",
            "x": parent.attrib["x"],
            "font-size": FONT_SIZE,
        })
        element.text = BULLET + " " + item