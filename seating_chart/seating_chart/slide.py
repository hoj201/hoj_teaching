from .seats import make_tables, Table, Student
from typing import List

import xml.etree.ElementTree as ET


def make_slides(tables: List[Table]) -> ET.Element:    
    # Create the root <svg> element with its attributes
    svg_attributes = {
        "width": "640",
        "height": "480",
        "xmlns": "http://www.w3.org/2000/svg"
    }
    svg = ET.Element('svg', svg_attributes)
    for index, table in enumerate(tables):
        offset_x = (index % 3) * 200 + 100
        offset_y = (index // 3) * 100 + 100
        # Create the <circle> element as a sub-element of <svg>
        circle = ET.SubElement(svg, 'circle', {
            "cx": str(offset_x),
            "cy": str(offset_y),
            "r": "90",
            "fill": "#ff4136",
            "stroke": "black",
            "stroke-width": "4"
        })

        # Create the <text> element and add it to <svg>
        t1 = ET.SubElement(svg, 'text', {
            "x": str(offset_x),
            "y": str(offset_y + 5),
            "font-family": "Verdana",
            "font-size": "14",
            "fill": "white",
            "text-anchor": "middle",
        })
        t1.text = "Table 1" # Set the text content inside the tag
        for student in table:
            t1_student = ET.SubElement(t1, 'tspan', {
                "x": str(offset_x),
                "dy": "1.2em",
                "font-size": "10",
            })
            t1_student.text = student.name
    return svg


# Convert the XML tree to a string
# The 'encoding' argument makes it human-readable
