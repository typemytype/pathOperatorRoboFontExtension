from AppKit import *
from vanilla import *

from lib.tools.removeOverlap import removeOverlap, difference, intersection, xor 
from lib.UI.integerEditText import NumberEditText

from mojo.roboFont import CurrentGlyph

class PathOperator(object):
    
    def __init__(self):
        
        self.w = FloatingWindow((256, 110), "Path Operations")
        
        items = [
                 dict(title="Union"), 
                 dict(title="Difference"),
                 dict(title="Intersection"),
                 dict(title="Xor")
                 ]
        _middle = 125
        _buffer = 14
        _y = 7
        self.w.operations = SegmentedButton((12, 7, -10, 22), items, selectionStyle="momentary", callback=self.operationCallback)
        self.w.operations.getNSSegmentedButton().setSegmentStyle_(NSSegmentStyleSmallSquare) 
        
        _y += 35
        
        self.w.roundCoordinatesText = TextBox((10, _y+2, _middle-_buffer, 19), "Round Coordinates:", sizeStyle="small", alignment="right")
        self.w.roundCoordinates = NumberEditText((_middle, _y, 50, 19), sizeStyle="small")
        
        _y += 30
        
        self.w.reverseContourOrder = CheckBox((_middle, _y, -10, 19), "Back to Front", sizeStyle="small")
        
        self.w.open()
    
    def operationCallback(self, sender):
        value = sender.get()
        roundCoordinates = self.w.roundCoordinates.get()
        backToFront = self.w.reverseContourOrder.get()
        
        if roundCoordinates is None:
            roundCoordinates = 0
            
        robofabGlyph = CurrentGlyph()
        
        if robofabGlyph is None:
            return
            
        glyph = robofabGlyph.naked()
        
        selectedContours = glyph.selection.getAllSelectedContours()
        if not selectedContours:
            return 
        
        if backToFront:
            selectedContours.reverse()
        
        subjectContours = selectedContours[:1]
        clipContours = selectedContours[1:]
        
        glyph.prepareUndo("Path Operations")
        
        if value == 0:
            # union
            removeOverlap(glyph, selectedContours, roundCoordinates)
        
        elif value == 1:
            # difference
            difference(glyph, subjectContours, clipContours, roundCoordinates)
                
        elif value == 2:
            # intersection
            intersection(glyph, subjectContours, clipContours, roundCoordinates)

        elif value == 3:
            # Xor
            xor(glyph, subjectContours, clipContours, roundCoordinates)
        
        glyph.performUndo()
        glyph.selection.resetSelection()
    
PathOperator()