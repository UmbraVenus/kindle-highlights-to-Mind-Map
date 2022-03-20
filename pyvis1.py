import streamlit as st
import os
from bs4 import BeautifulSoup
from pyvis import network as net
from IPython.core.display import display, HTML
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import math

def show_graph(net,name):
  net.show(name)
  display(HTML(name))

def form(text):
    lis = text.split(" ")
    linenumber = int(math.sqrt(len(lis)))
    newlis = [" ".join(lis[x*linenumber:(x+1)*linenumber]) for x in range(linenumber)]
    newlis += [" ".join(lis[linenumber*(linenumber):])]
    result = "\n".join(newlis)
    return result

def app():

    st.markdown(
        """
        # Amazon Highlights to Mind Map
        """
    )
    with st.form("pyvis"):
        uploaded_file = st.file_uploader(label="Exported Notes(html) Here ~", type=['html'])
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            with open(os.path.join("/tmp/",uploaded_file.name),"wb") as f:
                f.write((uploaded_file).getbuffer())
            st.success("File Saved")
    try:     
        with open("/tmp/"+ uploaded_file.name) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        
        # st.code(soup.prettify())
        
        # Constructing Nodes
        
        g = net.Network(height="1200px",width="90%")
        
        bookTitle = soup.select_one(".bookTitle").text
        authors = soup.select_one(".authors").text
        citation = form(soup.select_one(".citation").text)
        
        # Main Nodes
        g.add_node("mainNode",
                        label=bookTitle+authors+citation,
                        fixed = True,
                        shape = "box",
                        color="#c7ffd7",
                        size=50, value = 300, labelHighlightBold=True, level=0, x=400,y=400)
        
        # Side Nodes
        noteHeading = soup.select(".noteHeading")
        noteText = soup.select(".noteText")
        num = len(noteHeading)
        
        for x in range(num):
            next_note = noteHeading[x]
            highlight = next_note.next_element.next_element.next_element
        
            chapter = highlight.next_element.text
            
            highlight = highlight.text
        
            chapter = chapter.split("- ")[-1]
            location = "\n"
            if len(chapter.split(" > ")) > 1:
                chapter_name, location = chapter.split(" > ")
            else:
                chapter_name = chapter
            next_text = form(noteText[x].next_element.text)
            location = form(location)
            
            #chapternode
            g.add_node(chapter_name, label=chapter_name, fixed = False,
                        shape = "box", color="#ffcdc7",
                        size=50,  level=1, value=4)
            #noteNode
            g.add_node(chapter,label=next_text+"\n"+location, fixed = False,
                        shape = "box", color = "#fffac7",
                        size=50,  level=2,value=1)
            
            # main to chapter
            g.add_edge("mainNode", chapter_name, value = 5)
            # chapter to note
            g.add_edge(chapter_name,chapter, group=chapter_name, value=2)
            
            
            """
            if chapter_name not in chapters.keys():
                chapters[chapter_name] = []
            obj = {}
            obj["chapter"] = chapter
            obj["name"] = chapter_name
            obj["highlight"] = highlight
            obj["location"] = location
            obj["text"] = next_text.next_element
            chapters[chapter_name].append(obj)
            """
        #g.repulsion(node_distance=320,spring_length=220)
        g.force_atlas_2based(gravity=-200, spring_length=220 , overlap=1)
        g.hrepulsion(node_distance=380)
        g.show("/tmp/g.html")
        HtmlFile = open("/tmp/g.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height=700)
        st.ballons()
    except AttributeError:
        st.write("Waiting for uploaded file :D")