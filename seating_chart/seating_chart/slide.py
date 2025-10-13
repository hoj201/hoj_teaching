from .seats import Table
from typing import List

import xml.etree.ElementTree as ET


WIDTH = 1920
HEIGHT = 1080
HEADER_SIZE = "54"
FONT_SIZE = "44"
FONT_FAMILY = "Helvetica"
BG_COLOR = "green"


def make_slides(tables: List[Table], announcements: List[str], agenda_items: List[str]) -> ET.Element:    
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
    insert_tables(tables, svg)
    insert_agenda(agenda_items, svg)
    insert_announcements(announcements, svg)
    return svg

def insert_tables(tables: List[Table], svg: ET.Element):
    width = int(svg.attrib["width"])
    dx = width // 5
    if len(tables) > 9:
        raise ValueError("Slide code assumes fewer than 9 tables")
    for index, table in enumerate(tables):
        offset_x = (index % 3) * dx + dx//2
        offset_y = (index // 3) * dx + dx//2
        # Create the <circle> element as a sub-element of <svg>
        circle = ET.SubElement(svg, 'circle', {
            "cx": str(offset_x),
            "cy": str(offset_y),
            "r": str(dx//2),
            "fill": "#ff4136",
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
    for item in agenda_items:
        element = ET.SubElement(agenda, 'tspan', {
            "dy": "1.2em",
            "x": str(agenda_x),
            "font-size": FONT_SIZE,
        })
        element.text = item

def insert_announcements(announcements: List[str], svg: ET.Element):
    width = int(svg.attrib["width"])
    height = int(svg.attrib["height"])
    agenda_x = width-1.9*width//5
    ann_elem = ET.SubElement(svg, 'text', {
        "x": str(agenda_x),
        "y": str(height//2),
        "font-family": FONT_FAMILY,
        "font-size": HEADER_SIZE,
        "fill": "white",
        "text-anchor": "left",
    })
    ann_elem.text = "Announcements"
    for announcement in announcements:
        element = ET.SubElement(ann_elem, 'tspan', {
            "dy": "1.2em",
            "x": str(agenda_x),
            "font-size": FONT_SIZE,
        })
        element.text = announcement